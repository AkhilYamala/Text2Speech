from flask import Flask, flash, request, redirect, url_for, render_template
import pandas as pd
from copy import deepcopy

original_df = None

def allowed_file(filename):
    if filename.split('.')[1] == 'csv':
        return True
    return False

def feature_selection():
    flash(list(original_df.columns))
    

app = Flask(__name__)

# to display features on screen
@app.route('/handle_data/', methods=['POST'])
def handle_data():
    temp = list(map(int, request.form.getlist('index')))
    df = original_df.iloc[:250,temp]
    data = []
    header = df.columns
    for i in range(len(df)):
        data.append(df.iloc[i,:])
    return render_template('process.html',data=data,header=header)

# feature selection
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == None:
            return '''
                <h1>No file selected</h1>
            '''
        if file and allowed_file(file.filename):
            global original_df
            original_df = pd.read_csv(file)
            feature_selection()    
        else:
            return render_template('wrongFile.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'super key'
    app.run(debug=True)
