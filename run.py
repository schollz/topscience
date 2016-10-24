#!/usr/bin/env python3
import os.path
from os import path
import json
import base64

import bibtexparser
import markovify
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS

researchAreas = ['economics','biology','computerscience','math','astronomy','chemistry','psychology','medicine','physics']

def getArea(area):
    area = area.lower()
    if 'biology' in area or 'biochemistry' in area or 'genetics' in area:
        return 'biology'
    if 'computer' in area:
        return 'computerscience'
    if 'astronomy' in area or 'physics' in area:
        return 'physics'
    if 'math' in area or 'probability' in area:
        return 'math'
    if 'chemistry' in area:
        return 'chemistry'
    if 'economics' in area or 'business' in area:
        return 'economics'
    if 'psychology' in area or 'sociology' in area:
        return "psychology"
    if 'health' in area or 'pediatric' in area or 'oncology' in area or 'virology' in area or 'psychiatry' in area or 'medicine' in area or 'virology' in area:
        return 'medicine'
    else:
        return 'other'

def loadBibtexAndWriteTitles():
    print("Loading bibtex...")
    with open('top12000.bib') as f:
        b = bibtexparser.load(f)

    print("Writing files...")
    for entry in b.entries:
        try:
            area = getArea(entry['web-of-science-categories'])
        except:
            continue
        title = entry['title'].strip().replace('\n',' ').title() + ". "
        with open(area+"_titles.txt","a") as f:
            f.write(title)
        try:
            abstract = entry['abstract'].strip().replace('\n',' ') + " "
            with open(area+"_abstracts.txt","a") as f:
                f.write(abstract)
        except:
            pass


def generateMarkovSentences():
    for area in researchAreas:
        print("Reading titles for %s..." % area)
        try:
            text = open(area+"_titles.txt","r").read()
        except:
            continue
        print("Generating Markov chain for titles from %s..." % area)
        text_model = markovify.Text(text)
        print("Generating Markov sentences...")
        markov = []    
        for i in range(1767):  # want to ensure 50% probability of seeing two names randomly after 50 attempts, so X = ((1/2 - 50)^2 - 1/4)/(2*ln(2)). See Birthday Paradox
            try:
                markov.append(text_model.make_sentence()[:-1])
            except:
                pass
        with open(area+"_title_markov.json","w") as f:
            f.write(json.dumps(markov,indent=2))
        print("Reading abstracts for %s..." % area)
        text = open(area+"_abstracts.txt","r").read()
        print("Generating Markov chain for abstracts from %s..." % area)
        text_model = markovify.Text(text)
        print("Generating Markov sentences...")
        markov = []    
        for i in range(1767):  # want to ensure 50% probability of seeing two names randomly after 50 attempts, so X = ((1/2 - 50)^2 - 1/4)/(2*ln(2)). See Birthday Paradox
            try:
                paragraph = " "
                for i in range(5):
                    paragraph += text_model.make_sentence().strip()+" "
                markov.append(paragraph.strip())
            except:
                pass
        with open(area+"_abstract_markov.json","w") as f:
            f.write(json.dumps(markov,indent=2))

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
    # loadBibtexAndWriteTitles()
    generateMarkovSentences()
    # makeWordCloud()
    # print("Now run \n\npython3 -m http.server \n\nand open your browser to http://127.0.0.1:8000")
