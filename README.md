## TweeTINT! 
A project for TINT, the no.1 company in listening to users' feedback and needs

- **Author**: Jason Lin
- **Languages used**: Python, HTML/CSS, Javascript 
- **Website**: tweetweb.herokuapp.com

###Code Organization###

**Directory structure**

---

	> static
		> temp
			> graph_empty.png
		> bootstrap.min.css
		> jquery-1.7.1.min.js
		> jquery.easytabs.js
		> jquery.hashchange.js
		> tabs.css
		> loader.gif
	> templates 
		> index.html
		> login.html
		> welcome.html
		> base.html
	> Procfile 
	> requirements.txt
	> alchemyapi.py
	> api_key.txt
	> **app.py**

**Frameworks & Libraries**

Because the app involves extracting large amounts of data from Twitter and processing them through an external NLP engine, I've written the backbones of the webapp in Python and port it to an HTML via Heroku using a Python framework called Flask. 

To build the web app, a local python app was built first. All features and functionalities, including graphing a chart, were tested locally in the native python environment. To help mine data from Twitter, I've imported the **Tweepy** library for python. The graphing part involved libraries **Pandas** & **Matplotlib**. Last but not least, my sentiment analysis feature is based on **AlchemyAPI**'s wonderful natural language processing engine. Credits to them for granting me a student account that allows me to process extra queries per day.

###Backend###

---

	> app.py
	> *textsearch.txt
	> alchemyapi.py
	> api_key.txt

#####Twitter Mining####
Using the REST API

***Streaming*** 
- I have initially built my app off streaming live data from Twitter pertinent to keyword query using the *filter( )* function. While the data are very recent and rather relevant, the app has to be on for a long time listening to new feeds, and it was hard to terminate the process because if we give it a threshold of how many tweets to extract before termination, it might take hours to stop if the query is very uncommon. Therefore I've decided to go with the searching method instead. 

***Searching***
- Searching is much faster and more powerful than streaming, given that we don't require the latest, on-the-go data. With Tweepy's built in support for searching, I could specify how many tweets to search (in our case default = 200), which country to search from, etc. It is easier to manipulate and maintain than its streaming counterpart.

#####Matplotlib#####
Matplotlib is a MATLAB-like graphplotting library that allows me to plot different kinds of graphs (in our case a histogram) and export it as a PNG so I could render it on HTML webpages. There are actually other fancier ways to implement an interactive graph rendition through other libraries, but due to time constraint I've left it in the exploration section. 

#####AlchemyAPI#####
AlchemyAPI is a very powerful cloud Artifical Intelligence engine that supports both Natural Language Processing and Computer Vision analytics. It is owned by IBM, and could conduct a wide range of feature analyses of any text document or graphics. I've set it up in my app so that it will send in all tweets found through Twitter's REST API into AlchemyAPI and evaluate their sentiment aspects.

###Frontend###

---

	> templates
		> index.htm 
		> login.html
		> welcome.html
		> base.html
	> static
		> bootstrap.min.js 
		> jquery-1.7.1.min.js
		> jquery.easytabs.js
		> tabs.css
		> loader.gif

#####Flask#####
Flask is a Python framework that encapsulates the processes and procedures for hosting HTML content from python programs as well as making HTML requests that respond with feedback. It is the primary framework I used to port the app online.

A popular alternative to Flask is **Django** which has been used industry wide for its performance and design. I did not go with it however because Django demands the user to stick with its fundamental template design, which could sometimes result in a steeper learning curve. Flask gives you a lot more freedom and although the performance may not be as good as Django's for a webapp like TweeTINT it is more than enough. 

#####Heroku#####
Instead of using AWS, I've decided to go with Flask because of its easy-to-use and dedicated user experience.  It is also more cost efficient and saves a lot of hassle for setting up a new server, making it ideal for TweeTINT.

#####Easytabs#####
Easytabs provides a quick template to achieving a tab-style paging effect that allows different pages of content to be displayed on one single page. I attempted to incorporated that in TweeTINT so that different kinds of content are separated from each other and the page won't scroll down for too long.

###Bugs & Prospects###

#####Easytabs#####
There are problems with my javascript implementation so that currently clicking on tabs would bring the user to the corresponding section of the page, instead of switching across contents of different tab containers (hiding current and showing next)

#####Interactive Graphs#####
With more time, I could have used TweeTINT to plot interactive graphs that users can play around and interact with instead of static PNGs. Supported features are zooming in, highlighting curve, etc. Could also prompt user for an option of what kind of graph to display (Bar, Pie, Line, Dot) 

#####Increased functionalities#####

- Jump to top of page
- Advanced sentiment analysis using data analytics algorithms
- More statistical comparisons (i.e. Most popular language, location of Tweets, etc.)
- User defined search conditions (e.g. where to search from, language)
