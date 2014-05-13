# coding: utf-8
import os
os.environ["NLTK_DATA"] = os.getcwd()

# load Wordnet-Affect synsets
# corpus: a-synset.xml
# return: {
#   'noun': {
#     '05586574': { 'categ': 'electricity', 'pos': 'noun', 'offset16': '05586574' }
#   }, ...
# }
def load_asynsets(corpus):
    import xml.etree.ElementTree as ET
    tree = ET.parse(corpus)
    root = tree.getroot()

    asynsets = {}
    for pos in ["noun", "adj", "verb", "adv"]:
        asynsets[pos] = {}
        for elem in root.findall(".//%s-syn-list//%s-syn" % (pos, pos)):
            # n#05588321 -> (n, 05588321)
            (p, offset) = elem.get("id").split("#")
            if not offset: continue

            asynsets[pos][offset] = { "offset16": offset, "pos": pos };
            if elem.get("categ"):
                asynsets[pos][offset]["categ"] = elem.get("categ")
            if elem.get("noun-id"):
                # n#05588321 -> 05588321
                noun_offset = elem.get("noun-id").replace("n#", "", 1)
                asynsets[pos][offset]["noun-offset"] = noun_offset
                asynsets[pos][offset]["categ"] = asynsets["noun"][noun_offset]["categ"]
            if elem.get("caus-stat"):
                asynsets[pos][offset]["caus-stat"] = elem.get("caus-stat")

    return asynsets

# Merge WordNet-Affect synsets with WordNet-3.0 synsets
def merge_asynset_with_wn(asynsets):
    import nltk
    from nltk.corpus import WordNetCorpusReader

    wn16 = WordNetCorpusReader(nltk.data.find('resources/wordnet-1.6/dict'))
    wn30 = WordNetCorpusReader(nltk.data.find('resources/WordNet-3.0/dict'))

    pos_map = { "noun": "n", "adj": "a", "verb": "v", "adv": "r" }
    # start from "noun"
    for pos in ["noun", "adj", "verb", "adv"]:
        for offset in asynsets[pos].keys():
            # Get WordNet-1.6 synset
            synset_16 = wn16._synset_from_pos_and_offset(pos_map[pos], int(offset))
            if not synset_16: continue

            synset_30 = _wn30_synsets_from_wn16_synset(synset_16, wn30)
            if not synset_30:
                asynsets[pos][offset]["missing"] = 1
            else:
                (word, p, index) = synset_30.name.split(".")
                asynsets[pos][offset]["word"] = word
                asynsets[pos][offset]["synset"] = synset_30.name
                # db-synset is used to query the japanese wordnet (sqlite)
                asynsets[pos][offset]["db-synset"] = str("%08d-%s" % (synset_30.offset, p))
                asynsets[pos][offset]["offset"] = str("%08d" % (synset_30.offset))
                if "noun-offset" in asynsets[pos][offset]:
                    noffset = asynsets[pos][offset]["noun-offset"]
                    asynsets[pos][offset]["noun-synset"] = asynsets["noun"][noffset]["synset"]

    return asynsets

# Get WordNet-3.0 synset
# Similarity is calculated by wup_similarity
def _wn30_synsets_from_wn16_synset(synset, wn):
    (word, p, index) = synset.name.split(".")
    # ADJ_SAT -> ADJ: DO NOT EXIST ADJ_SAT in wordnet.POS_LIST
    if p == 's': p = 'a'
    synsets = wn.synsets(word, p)
    if len(synsets) == 0: return

    synset_sims = {}
    for i in range(len(synsets)):
        try:
            synset_sims[i] = synset.wup_similarity(synsets[i])
        except (RuntimeError, TypeError, NameError):
            # Set similarity to 0 in case of RuntimeError
            synset_sims[i] = 0
    # Most similar synset index
    index = sorted(synset_sims.items(), key=lambda x:x[1], reverse=True)[0][0]

    return synsets[index]

# Merge asynsets with Japanese WordNet
def merge_asynset_with_wnjpn(asynsets):
    for pos in asynsets.keys():
        for offset in asynsets[pos].keys():
            if not "db-synset" in asynsets[pos][offset]: continue
            word = _get_jpnword_from_synsets([asynsets[pos][offset]["db-synset"]])
            if word: asynsets[pos][offset]["jpnwordid"] = str(word.wordid)

    return asynsets

# Get japanese word from japanese wordnet
def _get_jpnword_from_synsets(synsets):
    from sqlalchemy import *
    db = create_engine('sqlite:///resources/wnjpn.db')
    metadata = MetaData(db, reflect=True)

    jpnwords = []
    sense = Table('sense', metadata)
    sense_rows = db.execute(sense.select(and_(
        sense.c.lang == 'jpn',
        sense.c.synset.in_(synsets)
    ))).fetchall()
    if len(sense_rows) == 0: return

    word = Table('word', metadata)
    word_row = db.execute(word.select(and_(
        word.c.wordid.in_([ row.wordid for row in sense_rows ])
    ))).fetchone()

    return word_row

# Output japanese wordnet affect
def output_jpn_asynset(asynsets):
    from xml.dom import minidom
    from xml.etree.ElementTree import *

    root = Element('syn-list')
    for pos in asynsets.keys():
        pos_node = SubElement(root, "%s-syn-list" % (pos))
        for offset in asynsets[pos].keys():
            node = SubElement(pos_node, "%s-syn" % (pos))
            for attr in ["offset", "synset", "caus-stat", "noun-synset", "jpnword", "jpnwordid"]:
                if attr in asynsets[pos][offset]:
                    node.set(attr, asynsets[pos][offset][attr])

    file = open("jpn-asynset.xml", "w")
    file.write(minidom.parseString(tostring(root)).toprettyxml())
    file.close()


if __name__ == '__main__':
    asynsets_16 = load_asynsets("resources/wn-affect-1.1/a-synsets.xml")
    asynsets_30 = merge_asynset_with_wn(asynsets_16)
    asynsets_with_jpn = merge_asynset_with_wnjpn(asynsets_30)
    output_jpn_asynset(asynsets_with_jpn)

