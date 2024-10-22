# What is in a *science paper* name? [Demo](https://topscience.schollz.com)

[Generate titles/abstracts from a Markov chain](https://topscience.schollz.com) determined from the most popular science papers of all time.  The dataset was generated by extracting the titles and abstracts from the 18,000 most cited science articles according to the <a href="https://apps.webofknowledge.com">Web of Science</a>. The titles and abstracts for a given subject were then fed into <a href="https://github.com/jsvine/markovify">jsvine's Markov chain generator</a>.

I also created a word cloud from these titles (which shows it pays to be a cell biologist who studies expression of human protein receptors).

<center><img src="/flask_words.png" width=400px></img></center>

Look no further for a name for your next Science/Nature paper. 

If you'd like to run the code yourself:

```
git clone https://github.com/schollz/topscience.git
cd topscience
python3 -m pip install bibtexparser markovify Pillow numpy
python3 run.py     # get a cup of coffee while you wait for this...
python3 -m http.server 
# Now open your browser to http://localhost:8000
```
