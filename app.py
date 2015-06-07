from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response
from functools import wraps
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import sys
import operator
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import tempfile
from alchemyapi import AlchemyAPI as alcapi
ALCAPI = alcapi() 

# Variables that contains the user credentials to access Twitter API 
access_token = "2227514784-PjNqLJUg9XpIT5uK23kV3dpfmLukw6SSngWc8Hw"
access_token_secret = "bI4p291ESFX1JvnfFMbHQQ9ZucW1IpIe2W7Gr4vPkwWA1"
consumer_key = "CAZcVS4kqiJfejb7CtimhBjqI"
consumer_secret = "rxluqu7wZT5lWAEVRJbYlhGOsrcqyVKVAiR0yMyQwOh9Izmcl8"

# Create the application object
app = Flask(__name__)

# Need a secret key for sessions to work properly
app.secret_key = "my precious"

# login required decorator
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

# Ssing decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
	
	tweets = {}
	keyword = "(empty input)"
	bins=np.histogram(np.hstack((-1,1)), bins=20)[1]
	tweet_hash={}

	if request.method == 'POST':
		# Setting up API authentication
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = API(auth)

		# Requests HTML user input and performs search
		keyword = query = request.form['keyword'] 
		query2 = request.form['fetchcount']
		tweets = api.search(q=str(query), count=int(query2))
		
		# Initialize some variables to be used later 
		tweet_hash={}
		scores = []
		sentiscore = {}
		cleanHashTags = []

		# Initialize matplot
		fig = plt.figure(dpi=200)
		axes = fig.add_subplot(1,1,1)

		for tweet in tweets:
			# Data exchange with the NLP engine
			sentiment = ALCAPI.sentiment('text', tweet.text)
			try:
				scores.append(sentiment['docSentiment']['score'])
				sentiscore[sentiment['docSentiment']['score']] = tweet.text
				axes.hist(map(float, scores), bins=bins, alpha=.3)
			except KeyError:
				pass

			# Mining hashtags
			for ht in tweet.entities['hashtags']:       
				if (ht != None):
					if ht["text"].encode("utf-8") in tweet_hash.keys(): 
						tweet_hash[ht["text"].encode("utf-8")] += 1
					else:
					  tweet_hash[ht["text"].encode("utf-8")] = 1
		 
			sortedHashTags = dict(sorted(tweet_hash.items(), reverse=True)[:10]) 

		# Lock x-range, scale y by 5% padding
		axes.set_xlim(-1, 1)
		ymin, ymax = axes.set_ylim()
		axes.set_ylim(ymin, 1.05*ymax)

		# Add legend, labels
		plt.legend(['Sentiment'], loc='best', ncol=1, fontsize=15)    
		axes.set_title("(0=neutral, -1=bad, 1=good)")
		axes.set_xlabel("Sentiment Score")
		axes.set_ylabel("Occurences")

		# Designating a temp directory to store grpah as PNG
		f = tempfile.NamedTemporaryFile(dir='static/temp', suffix='.png',delete=False)
		plt.savefig(f)
		f.close()
		plotPng = f.name.split('/')[-1]

		# Finalizes figures and statistics to be rendered on HTML
		cleanHashTags = sorted(sortedHashTags.items(), key=lambda kv: (kv[1],kv[0]),reverse=True)		
		tweet_content = [dict(text=tweet.text, date = tweet.created_at) for tweet in tweets]
		positive_score = max(sentiscore.keys())
		positive_tweet = sentiscore[positive_score]
		negative_score = max([x for x in sentiscore.keys() if float(x)<0])
		negative_tweet = sentiscore[negative_score]

		return render_template('index.html', tweet_content = tweet_content, keyword=keyword, \
			 plotPng=plotPng, positive_score=positive_score, negative_score=negative_score, \
			positive_tweet=positive_tweet, negative_tweet=negative_tweet, cleanHashTags=cleanHashTags)
	else:
		plotPng = 'graph_empty.png'
		return render_template('index.html', keyword=keyword, plotPng=plotPng)

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

# By default flask assumes a GET request
@app.route('/login', methods=['GET', 'POST']) 
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'tint':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			return redirect(url_for('home'))
	return render_template('login.html',error=error)

# Logout screen - needed to be logged in to display, looks for a session token, else reroutes
@app.route('/logout')
@login_required
def logout():
	# Checks for session token
	session.pop('logged_in', None)
	flash('You were just logged out.')
	return redirect(url_for('welcome'))


if __name__ == '__main__':
	app.run(debug=True)