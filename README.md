japanese-wordnet-affect
=======================

Create Japanese WordNet-Affect from WordNet(1.6, 3.0), WordNet-Affect and Japanese WordNet.


Requirements
-------------

- python
- [sqlite3](http://www.sqlite.org/download.html)
- [WordNet-Affect](http://wndomains.fbk.eu/wnaffect.html)


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
  <noun-syn jpnwordid="163121" offset="07507912" synset="confusion.n.03"/>
  ...
</noun-syn-list>
<adv-syn-list>
  <adv-syn caus-stat="stat" jpnwordid="191589" noun-synset="peace.n.03" offset="00418712" synset="peaceably.r.01"/>
  ...
</adv-syn-list>
```

`offset` is offset for WordNet-3.0

`synset` is synset for WordNet-3.0

`jpnwordid` is wordid for word table in Japanese WordNet (sqlite)

