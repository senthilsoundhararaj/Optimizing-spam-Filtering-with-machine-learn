#from crypt import methods
from os import stat
import flask
from flask import Flask, current_app, render_template, request,session
import pickle
from entity.sms_spam_classifier import SMSSPAMClassifier
import sys  
import nltk
sys.path.insert(0, './entity/sms_spam_classifier.py')


nltk.download('stopwords')



app = Flask(__name__)
app.secret_key = "mlmodel"


    
def load_classifier() -> SMSSPAMClassifier:
    sms_classifier = None
    with open('../Training/smsspamclassifer.pkl','rb') as picker_reader:
        sms_classifier = pickle.load(picker_reader)
    return sms_classifier


ctx = app.app_context()
flask.model = load_classifier()
ctx.push()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/spam", methods=['GET','POST'])
def index():
    message_status = None
    if request.method == "POST":
        message_status = "Ham"


        status = flask.model.predict(request.form.get('review_msg'))
        
        if status[0] == 1:
            message_status = "Spam"

        #eturn status

    return render_template('index.html',message_status=message_status)



if __name__ == "__main__":
    app.run(debug=True)
   