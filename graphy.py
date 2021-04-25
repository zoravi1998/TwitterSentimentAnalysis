import matplotlib.pyplot as plt 
import pandas as pd
from flask import Flask, request, render_template 
# df=pd.read_csv("ele.csv")
# li1 = df['sentiment'].values.tolist()
# li2 = df['value'].values.tolist()
# li3 = [ {'x':x1,'y':y1} for x1,y1 in zip(li1,li2)]
# print(li3)
app = Flask( __name__ )
@app.route('/')
def home():
    data=[20,30,40]
    df = pd.read_csv("test/ele.csv")
    df.loc[(df.sentiment == 'pos'),'sentiment']=1
    df.loc[(df.sentiment == 'neu'),'sentiment']=2
    df.loc[(df.sentiment == 'neg'),'sentiment']=3
    li1 = df['index'].values.tolist()
    li2 = df['value'].values.tolist()
    li3 = zip(li1,li2)
    dftweet = pd.read_csv('test/tweets.csv')
    return render_template("second.html",values=data,scatter_data=li3,ptweets=dftweet.positive,ntweets=dftweet.negative,neutweets=dftweet.neutral)
if __name__ == "__main__":
    app.run(debug=True)
