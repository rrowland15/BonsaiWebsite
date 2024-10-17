from flask import Flask, render_template, redirect, url_for, request
from google.cloud import storage
import os
import tkinter as tk
from tkinter import filedialog
import logging

logging.basicConfig(level=logging.DEBUG)

credential_path = "credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    return render_template("index.html")

@app.route("/createalbum", methods=['GET', 'POST'])
def createalbum():
     return render_template("createalbum.html")


@app.route('/upload', methods=['GET','POST'])
def upload():
    print("Here")
    print(request.form["test5"])

    treepic = request.form["imagefile"]

    


    bucket_name = "treephotos"
    destination_blob_name = "somenewname"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename

    # with open(treepic,"rb") as f:
    #     file_data = f.read()
    blob.upload_from_string(treepic)

    print(f"File {treepic} uploaded to {destination_blob_name}.")
    #print(response)
    #root = tk.Tk()
    #root.withdraw()  # Hide the main window

    # file_path = filedialog.askopenfilename()

    # if file_path:
    #     print("Selected file:", file_path)
    # app.logger.info('Hello-world applog')
    # print("here")
    # if 'file' not in request.files:
    #     print('No file part')

    # file = request.files['file']
    # if file.filename == '':
    #     print('No selected file')

    # # Process the uploaded file here (e.g., save it to a directory)
    # # file.save(file.filename)
    # elif file.filename != '':
    #     print(file.filename)

    return 'File uploaded successfully'

if __name__ == '__main__':
    #app.run(port=5656,debug=True)
    print('starting to run here', flush=True)
    app.run(debug=True)
    