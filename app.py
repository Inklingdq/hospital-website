### Right now we only suppost csv.
import io
import os
import glob
import numpy as np
import pandas as pd
import json
import model
from flask import Flask, request, jsonify, render_template, send_file, Response,session
import flask
import csv
import json
from flask_session import Session


app = Flask(__name__)
app.config['subdomain_matching'] = 'covidseverity.com/hospitalization'
app.config['SEVER_NAME'] = 'covidseverity.com/hospitalization'
app.secret_key = os.urandom(24)
### Get format of input file.
def format(filename):	
	if '.' not in filename:
		return '',''
	else:
		return filename.rsplit('.',1)[1].lower(),filename.rsplit('.',1)[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():    
    def writename(name):
        text_file = open("name.txt","w")
        n = text_file.write(name)
        text_file.close()
    file = request.files['file']
    ### Check if there's input before processing.
    if not(file.filename):
    	flash('No selected file.')
    	return redirect(request.url)
    f,name = format(file.filename)	
    if not(f):
    	flash('Wrong file format.')
    	return redirect(request.url)
    data = pd.read_csv(file).dropna()
    var = data.columns[1]
    ## Get prediction results
    fig, prediction, prediction_interval = model.predict(data, 14, var)
    ## Prepare dataframe to write
    prediction.append(round(sum(prediction),1))
    prediction_interval.append((round(sum([x[0] for x in prediction_interval],1)), 
                                round(sum([x[1] for x in prediction_interval],1))))
    dic = {'Date': [i+1 for i in range(14)] +['sum'],
            data.columns[1]+' prediction': prediction,
            'prediction interval':prediction_interval}
    df = pd.DataFrame(dic, columns = ['Date',data.columns[1]+' prediction','prediction interval'])
    ## Write dataframe to file and save the file name in name.txt
    name = name + '_prediction.csv'
    df.round(1).to_csv(name,index=False)
    text_file = open("name.txt", "w")
    n = text_file.write(name)
    return render_template("predict.html", plotcode = fig)


@app.route('/download',methods=['POST'])
def download():
    f = open("name.txt", "r")
    return send_file(f.readline(), as_attachment = True)
    
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0')

