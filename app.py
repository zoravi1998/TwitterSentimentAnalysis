from flask import Flask, request, render_template 
import tweety
 
app = Flask(__name__)
tweeterhandle=''
@app.route('/', methods = ['GET','POST'])
def index():
    global tweeterhandle
    if request.method == 'POST':
        tweeterhandle = request.form.get("handle")
        tweety.main(tweeterhandle)
        print(tweeterhandle)

    return render_template("index.html")

if __name__ == "__main__":
    app.run( debug=True)