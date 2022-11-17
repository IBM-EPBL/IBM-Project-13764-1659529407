import numpy as np
from flask import Flask, redirect, url_for, render_template, request, redirect, jsonify
from markupsafe import escape
import pickle
import inputScript   #inputScript file - to analyze the URL

app = Flask(__name__)

model = pickle.load(open("phishing_website.pkl","rb"))

# user-inputs the URL in this page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/aboutpage')
def aboutpage():
    return render_template('aboutpage.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/sign-up-page')
def sign_up_page():
    return render_template('sign_up_page.html')

@app.route('/prediction_page')
def predict():
    return redirect(url_for('y_predict'))
#  fetches given URL and passes to inputScript

@app.route('/predict',methods=['GET','POST'])
def y_predict():
    if request.method=='POST':
        url = request.form['url']
        check_predic = inputScript.main(url)
        predic = model.predict(check_predic)
        pred=" "
        # print(check_predic)
        # print (predic)
        # result = predic[0]
        
        if(predic==-1):
            return render_template("predict.html", pred_text = "is safe", url = url)
        elif(predic==1):
            return render_template("predict.html", pred_text = "is phishing", url = url)
        else:
            return render_template("predict.html", pred_text = "is suspicious", url = url)
    else:
        return render_template("predict.html")

#  takes ip parameters from URL by inputScript and returns the predictions
@app.route('/predict_api', methods = ['POST'])
def predict_api():

    data = request.get_json(force = True)
    predic = model.y_predict([np.array(list(data.values()))])
    result = predic[0]
    return jsonify(result)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', debug=True)