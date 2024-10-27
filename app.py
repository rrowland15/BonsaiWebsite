from flask import Flask, render_template, redirect, url_for, request
from google.cloud import storage
import os
import tkinter as tk
from tkinter import filedialog
import logging
import sqlite3

from gcstorage_interaction import delete_blob, upload_blob


logging.basicConfig(level=logging.DEBUG)

credential_path = "credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    connection = sqlite3.connect("sqlite/mytest.db")
    cursor = connection.cursor()
    query = 'SELECT imagelink, albumtitle, imagedescription from UserTreePictures Where email = "album@gmail.com" and albumcover = True'
    albumdata = cursor.execute(query).fetchall()
    if request.method == 'POST':
        pass

    
    return render_template("index.j2", albumdata=albumdata)

@app.route("/deletealbum/<albumtitle>", methods=['GET', 'POST'])
def deletealbum(albumtitle):
    albumtitle = '"' + albumtitle + '"'
    
    connection = sqlite3.connect("sqlite/mytest.db")
    cursor = connection.cursor()
    print(albumtitle)

    deleteImagesQuery = '''SELECT imagelink from UserTreePictures where albumtitle = {}'''.format(albumtitle)
    print(deleteImagesQuery)

    imagelinks = cursor.execute(deleteImagesQuery).fetchall()
    print(imagelinks)

    deleteDatabaseEntries = '''DELETE FROM UserTreePictures Where albumtitle = {}'''.format(albumtitle)
    deleteEntries = cursor.execute(deleteDatabaseEntries)

    for link in imagelinks:
        dellink = "rcrowland15/"+link[0]
        print(dellink)
        delete_blob('treephotos',dellink)

    connection.commit()
    cursor.close()

    return redirect("/")


@app.route("/createalbum", methods=['GET', 'POST'])
def createalbum():
    print("here",request.method)
    if request.method == 'POST':
        print(request.form)
        print(request.files)

        #
        username = "album@gmail.com"    #this should be the same as blob location in final
        blob_location = "treephotos/rcrowland15"

        # album cover
        imageupload = request.files['imageUpload']
        albumname = request.form["albumname"]
        albumcontents = request.form["albumcontents-input"]

        print(type(imageupload))

        # journal entry
        imageupload2 = request.files['imageUpload2']
        journalname = request.form["journal-name-input"]
        journalcontent = request.form["journal-content-input"]

        
        # this could be a microservice
        bucket_name = "treephotos"
        strippedalbumname = albumname.replace(" ","").lower()
        print(strippedalbumname)
        destination_blob_name = "rcrowland15/"+strippedalbumname+".jpg"
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename
        blob.upload_from_file(imageupload)

        print(f"File {imageupload} uploaded to {destination_blob_name}.")

        # add stuff to database
        connection = sqlite3.connect("sqlite/mytest.db")
        cursor = connection.cursor()
        tempname = '"'+strippedalbumname+'.jpg"'
        tempalbumname = '"'+albumname+'"'
        tempalbumcontents = '"'+albumcontents+'"'
        query = '''Insert Into UserTreePictures Values ("album@gmail.com", {}, True, {}, {}, "1/1/2025")'''.format(tempname,tempalbumname,tempalbumcontents)
        count = cursor.execute(query)
        connection.commit()
        print("Executed")
        cursor.close()
        



        

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
    