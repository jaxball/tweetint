from flask import Flask, render_template, redirect, url_for, request, session, flash, g, make_response
from functools import wraps
import sqlite3
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
import sys
import StringIO
import time
import datetime
import operator
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpld3
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import tempfile
# import random
import json
#Alchemy API
import os
cwd = os.getcwd()
os.chdir('/Users/jasonlin/Desktop/alchemyapi_python/')
from alchemyapi import AlchemyAPI as alcapi

ALCAPI = alcapi() 
os.chdir(cwd)

#Variables that contains the user credentials to access Twitter API 
access_token = "2227514784-PjNqLJUg9XpIT5uK23kV3dpfmLukw6SSngWc8Hw"
access_token_secret = "bI4p291ESFX1JvnfFMbHQQ9ZucW1IpIe2W7Gr4vPkwWA1"
consumer_key = "CAZcVS4kqiJfejb7CtimhBjqI"
consumer_secret = "rxluqu7wZT5lWAEVRJbYlhGOsrcqyVKVAiR0yMyQwOh9Izmcl8"

#create the application object
app = Flask(__name__)

#need a secret key for sessions to work properly
app.secret_key = "my precious"
app.database = "sample.db"

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

#using decorators to link the function to a url
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
	# return "TweeTINT - A twitter sentiment analysis webapp"
	# g is an object specific to flask that resets after each request
	g.db = connect_db()
	cur = g.db.execute('select * from posts')
	posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
	# flash(type(row))
	g.db.close()
	tweets = {}
	keyword = ""
	bins=np.histogram(np.hstack((-1,1)), bins=20)[1]
	json01=None
	tweet_hash={}
	if request.method == 'POST':
		query = request.form['keyword'] 
		keyword = query
		auth = OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		api = API(auth)
		#This line filter Twitter Streams to capture data input by user
		tweets = api.search(q=str(query), count=50)
		# tweet_content = []
		tweet_hash={}
		# output = open("search_results.txt", "w")
		scores = []
		#set up matplot
		fig = plt.figure(dpi=100)
 		axes = fig.add_subplot(1,1,1)
		for tweet in tweets:
			sentiment = ALCAPI.sentiment('text', tweet.text)
			try:
				# scores.append(-.5)
				# scores.append(1)
				# scores.append(0.75)
				scores.append(sentiment['docSentiment']['score'])
				axes.hist(map(float, scores), bins=bins, alpha=.3)
				# tweet_content.append( dict(text=str(tweet.text), mood=sentiment['docSentiment']) )
			except KeyError:
				pass
			#mining hashtags
			flash(tweet.entities['hashtags'])
			hashtags = tweet.entities['hashtags']

	        for ht in tweet.entities['hashtags']:                          
	            if ht != None:
	                flash(ht[u'text'].encode("utf-8"))
	                if ht["text"].encode("utf-8") in tweet_hash.keys(): 
	                    tweet_hash[ht["text"].encode("utf-8")] += 1
	                else:
	                  tweet_hash[ht["text"].encode("utf-8")] = 1
	     
	        sortedHashTags = dict(sorted(tweet_hash.items(), key=operator.itemgetter(1), reverse=True)[:10]) 
	        hash_frequency = sorted(sortedHashTags.items(), key=lambda kv: (kv[1],kv[0]),reverse=True)

		# Lock x-range, scale y by 5% padding
		axes.set_xlim(-1, 1)
		ymin, ymax = axes.set_ylim()
		axes.set_ylim(ymin, 1.05*ymax)

		# Add legend, labels
		plt.legend(['Sentiment'], loc='best', ncol=1, fontsize=15)    

		axes.set_title("Distribution of sentiment (0=neutral, -1=bad, 1=good)")
		axes.set_xlabel("Score")
		axes.set_ylabel("Occurences")
		f = tempfile.NamedTemporaryFile(dir='static/temp', suffix='.png',delete=False)
		plt.savefig(f)
		f.close()
		plotPng = f.name.split('/')[-1]
		# make the temporary file
 	# 	f = tempfile.NamedTemporaryFile(dir='static/temp', suffix='.png',delete=False)
		# plt.savefig(g)
		# f.close()
		# plotPng = f.name.split('/')[-1]
		# mpld3.show()
		# figure = plt.figure(1)
		# graph = mpld3.fig_to_html(plt.figure(1))
		json01 = json.dumps(mpld3.fig_to_dict(plt.figure(1)))
		# hash_frequency = [dict(word=key.decode("utf-8"), count=value) for key,value in sortedHashTags]
		tweet_content = [dict(text=tweet.text, date = tweet.created_at) for tweet in tweets]
		return render_template('index.html', tweet_content = tweet_content, keyword=keyword, json01=json01, hash_frequency=hash_frequency, plotPng=plotPng)
	else:
		plotPng = 'graph_empty.png'
		return render_template('index.html', keyword=keyword, json01=json01, plotPng=plotPng)

"""# This takes care of the graph display
		# Lock x-range, scale y by 5% padding
		plt.xlim(-1, 1)
		ymin, ymax = plt.ylim()	
		plt.ylim(ymin, 1.05*ymax)

		# Add legend, labels
		plt.legend(['Sentiment'], loc='best', ncol=1, fontsize=15)    

		# Add a vertical line
		ymax = plt.ylim()[1]
		plt.vlines(0, 0, ymax, lw=4, linestyle='--')

		plt.title("Distribution of sentiment (0=neutral, -1=bad, 1=good)")
		plt.xlabel("Score")
		plt.ylabel("Occurences");
		plt.show()
		# return render_template('search.html')
	# return render_template('index.html', posts=posts)
	"""

# @app.route('/plot.png')
# def home():
#     fig = Figure()
#     axis = fig.add_subplot(1, 1, 1)
 
#     xs = range(100)
#     ys = [random.randint(1, 50) for x in xs]
 
#     axis.plot(xs, ys)
#     canvas = FigureCanvas(fig)
#     output = StringIO.StringIO()
#     canvas.print_png(output)
#     response = make_response(output.getvalue())
#     response.mimetype = 'image/png'
#     return response

@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
	# this is junk code
	if request.method == 'POST':
			flash('Testing search!')
			query = request.form['keyword'] 
			# l = StdOutListener()
			# auth = OAuthHandler(consumer_key, consumer_secret)
			# auth.set_access_token(access_token, access_token_secret)
			# stream = Stream(auth, l)
			# #This line filter Twitter Streams to capture data input by user
			# stream.filter(track=[str(query)])
	return render_template('search.html')

@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

#by default flask assumes a GET request
@app.route('/login', methods=['GET', 'POST']) 
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'tint':
			error = 'Invalid credentials. Please try again.'
		else:
			session['logged_in'] = True
			flash('Login successful!')
			return redirect(url_for('home'))
	return render_template('login.html',error=error)

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You were just logged out.')
	return redirect(url_for('welcome'))

def connect_db():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run(debug=True)