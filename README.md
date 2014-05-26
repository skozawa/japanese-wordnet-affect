japanese-wordnet-affect
=======================

Create Japanese WordNet-Affect from WordNet(1.6, 3.0), WordNet-Affect and Japanese WordNet.


Requirements
-------------

- python
- [sqlite3](http://www.sqlite.org/download.html)
- [WordNet-Affect](http://wndomains.fbk.eu/wnaffect.html)
  - download and move to `resources/wn-affect-1.1`


Set up
-------

```
pip install -r requirements.txt
sh setup.sh
```


Create Japanese-WordNet-Affect
------------------------------

The command outputs `jpn-asynset.xml`.

```
python create_jp_wn_affect.py
```

Example
```
<noun-syn-list>
  <noun-syn categ="loyalty" offset="07546389" synset="loyalty.n.02">
    <jpn-word lemma="忠魂" pos="n" wordid="211296"/>
    <jpn-word lemma="忠誠" pos="n" wordid="226847"/>
    <jpn-word lemma="忠心" pos="n" wordid="238518"/>
  </noun-syn>
  ...
</noun-syn-list>
<adv-syn-list>
  <adv-syn categ="favor" caus-stat="stat" noun-synset="favor.n.04" offset="00230444" synset="favorably.r.01">
    <jpn-word lemma="好意的に" pos="r" wordid="164889"/>
    <jpn-word lemma="好ましい" pos="a" wordid="166551"/>
    <jpn-word lemma="色良い" pos="a" wordid="167291"/>
    ...
  </adv-syn>
  ...
</adv-syn-list>
```

- (noun|adv|adj|verb)-syn
  - `offset` is offset for WordNet-3.0
  - `synset` is synset for WordNet-3.0
  - `noun-synset` is offset of noun
  - `categ` is category on WordNet-Affect
- jpn-word
  - `wordid` is wordid for word table in Japanese WordNet (sqlite)
  - `lemma` is japanese lemma
  - `pos` is part-of-speech

