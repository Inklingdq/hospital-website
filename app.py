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
    data = pd.read_csv(file)
    var = data.columns[1:]
    output = model.predict(data, var)
    [x.append(sum(x)) for x in output]
    name = name + '_prediction.csv'
    labels = [str(x) for x in range(1,8)] + ['sum']
    pd.DataFrame(data = np.array([labels] + output).T,columns=data.columns).to_csv(name,index=False)
    text_file = open("name.txt", "w")
    n = text_file.write(name)
    session['output'] = output[0][:-1]
    session['values'] = data.iloc[:,1].tolist()
    session['legends'] = var[0]
    session['labels'] = data.iloc[:,0].tolist()
    return render_template("predict.html")

@app.route('/get_data')
def get_data():
    output = session.get('output', None)
    values = session.get('values', None)
    legends = session.get('legends', None)
    labels = session.get('labels', None)
    return jsonify({'values':values, 'labels':labels + ['+'+str(x) for x in range(1,8)], 
                                               'legends':legends,'predicts': output})

@app.route("/tables")
def show_tables():
    f = open("name.txt", "r")
    data = pd.read_csv(f.readline())
    data.set_index(['Name'], inplace=True)
    data.index.name=None
    return render_template('predict.html',tables=[data.to_html],titles=data.columns.values)


@app.route('/download',methods=['POST'])
def download():
    f = open("name.txt", "r")
    return send_file(f.readline(), as_attachment = True)
    
if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0')

