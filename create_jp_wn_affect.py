# coding: utf-8
import os
os.environ["NLTK_DATA"] = os.getcwd()

# load Wordnet-Affect synsets
def load_asynsets(corpus):
    import xml.etree.ElementTree as ET
    tree = ET.parse(corpus)
    root = tree.getroot()

    asynsets = {}
    for pos in ["noun", "adj", "verb", "adv"]:
        asynsets[pos] = {}
        for elem in root.findall(".//%s-syn-list//%s-syn" % (pos, pos)):
            (p, offset) = elem.get("id").split("#")
            if not offset: continue

            asynsets[pos][offset] = { "offset16": offset, "pos": pos };
            if elem.get("categ"):
                asynsets[pos][offset]["categ"] = elem.get("categ")
            if elem.get("noun-id"):
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
    for pos in asynsets.keys():
        for offset in asynsets[pos].keys():
            # Get WordNet-1.6 synset
            synset_16 = wn16._synset_from_pos_and_offset(pos_map[pos], int(offset))
            if not synset_16: continue
            asynsets[pos][offset]["synset16"] = synset_16.name

            synset_30 = _wn30_synsets_from_wn16_synset(synset_16, wn30)
            if not synset_30:
                asynsets[pos][offset]["missing"] = 1
            else:
                asynsets[pos][offset]["synset30"] = synset_30.name
                asynsets[pos][offset]["offset30"] = synset_30.offset

    return asynsets

# Get WordNet-3.0 synset
# Similarity is calculated by wup_similarity
def _wn30_synsets_from_wn16_synset(synset, wn):
    (term, p, index) = synset.name.split(".")
    # ADJ_SAT -> ADJ: DO NOT EXIST wordnet.POS_LIST
    if p == 's': p = 'a'
    synsets = wn.synsets(term, p)
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


if __name__ == '__main__':
    asynsets = load_asynsets("resources/wn-affect-1.1/a-synsets.xml")
    merge_asynset_with_wn(asynsets)

