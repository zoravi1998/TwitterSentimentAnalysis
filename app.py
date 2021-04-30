from flask import Flask, request, render_template
import tweety as ty
import pandas as pd
import numpy as np
pstweets=''
ngtweets=''
neutweets=''
scatterdata=''
bardata=''
app = Flask(__name__)
def initliaze(tweeterhandle):
    global pstweets, ngtweets, neutweets,scatterdata,bardata
    # creating object of TwitterClient Class
    api = ty.TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query=tweeterhandle, count=100)

    #scatter plot data points
    ele_y = [int(100*x) for x in api.scatter_y]
    ele_x = [ i for i in range(len(ele_y))]
    scatterdata=np.column_stack((ele_x,ele_y))

    #bar graph data
    bardata = api.bar_y
    # picking positive,negative,neutral tweets from tweets
    pstweets = [tweet['text'] for tweet in tweets if tweet['sentiment'] == 'positive']

    ngtweets = [tweet['text'] for tweet in tweets if tweet['sentiment'] == 'negative']

    neutweets = [tweet['text'] for tweet in tweets if tweet['sentiment'] == 'neutral']

    # percentage of tweets
    # psper = (100*len(pstweets))/len(tweets)
    # negper = (100*len(ngtweets))/len(tweets)
    # neuper = 100*len(100*len(neutweets))/len(tweets)

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in pstweets[:10]:
        print(tweet)

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ngtweets[:10]:
        print(tweet)


@app.route('/', methods=['GET', 'POST'])
def index():
    global tweeterhandle
    if request.method == 'POST':
        tweeterhandle = request.form.get("handle")
        print(tweeterhandle)
        if(tweeterhandle == ''):
            print("no handle")
        else:
            initliaze(tweeterhandle)


    return render_template("index.html")


@app.route('/result')
def home():
    global pstweets,neutweets,ngtweets,scatterdata,bardata

    return render_template("second.html", bargraphdata=bardata, scatter_data=scatterdata, ptweets=pstweets, ntweets=ngtweets, neutweets=neutweets)

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/additionals')
def additional():
    return render_template("additionals.html")
@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
