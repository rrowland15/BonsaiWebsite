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


@app.route("/entrytemplate", methods=['GET', 'POST'])
def entrytemplate():

    return render_template("entrytemplate.html")


@app.route('/upload', methods=['GET','POST'])
def upload():
    print("Here")
    print(request.form["test5"])

    treepic = request.form["imagefile"]

    # this could be a microservice
    bucket_name = "treephotos"
    destination_blob_name = "somenewname"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename
    blob.upload_from_string(treepic)

    print(f"File {treepic} uploaded to {destination_blob_name}.")

    return 'File uploaded successfully'

if __name__ == '__main__':
    #app.run(port=5656,debug=True)
    print('starting to run here', flush=True)
    app.run(debug=True)
    