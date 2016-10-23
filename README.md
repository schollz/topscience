# README

What's in a title? I extracted 12,000 articles with the most citations in the journals Science and Nature (using expression `SO=(SCIENCE OR NATURE)` and exported into the Bibtex file `top12000.bib`).

From these I created a word cloud of the top words and generated a little website to view some Markov-chain related article names. Look no further for a name for your next article.

# Setup

```
python3 -m pip install bibtexparser markovify Pillow numpy
```

# Run

```
python3 run.py
```
