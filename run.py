#!/usr/bin/env python3
import os.path
from os import path
import json

import bibtexparser
import markovify
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS


def loadBibtexAndWriteTitles():
	if os.path.isfile("titles.txt"):
		return
	print("Loading bibtex...")
	with open('top12000.bib') as f:
		b = bibtexparser.load(f)

	print("Writing files...")
	with open("titles.txt","w") as f:	
		for entry in b.entries:
			title = entry['title'].replace('\n',' ').title() + ". "
			f.write(title)

def generateMarkovSentences():
	print("Reading titles...")
	text = open("titles.txt","r").read()
	print("Generating Markov chain...")
	text_model = markovify.Text(text)
	print("Generating Markov sentences...")
	markov = []	
	for i in range(20000):
		try:
			markov.append(text_model.make_sentence()[:-1])
		except:
			pass
	with open("markov.json","w") as f:
		f.write(json.dumps(markov))

def makeWordCloud():
	print("Generating word cloud...")
	# Load in the titles
	d = path.dirname(__file__)
	text = open(path.join(d, 'titles.txt')).read()

	# read the mask image
	mask = np.array(Image.open(path.join(d, "flask_mask.png")))

	stopwords = set(STOPWORDS)
	stopwords.add("said")

	wc = WordCloud(width=800, height=400, background_color="white", max_words=2000, mask=mask,
	               stopwords=stopwords)

	# generate word cloud
	wc.generate(text)

	# store to file
	wc.to_file(path.join(d, "flask_words.png"))

if __name__ == "__main__":
	loadBibtexAndWriteTitles()
	generateMarkovSentences()
	makeWordCloud()
	print("Now run \n\npython3 -m http.server \n\nand open your browser to http://127.0.0.1:8000")
