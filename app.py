from flask import Flask, render_template, redirect, url_for, request, flash
from google.cloud import storage
import os
import tkinter as tk
from tkinter import filedialog
import logging
import sqlite3

from gcstorage_interaction import delete_blob, upload_blob
from imagemetadata import get_image_info
from generateurl import generateurl


logging.basicConfig(level=logging.DEBUG)

credential_path = "credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path



app = Flask(__name__)
app.secret_key = 'some key'

@app.route("/", methods=['GET', 'POST'])
def homescreen():
    return render_template('index.j2')


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user_email = '"'+request.form["email"]+'"'
        user_password = '"'+request.form["password"]+'"'
        print(user_email,user_password)

        connection = sqlite3.connect("sqlite/users.db")
        cursor = connection.cursor()

        query = 'SELECT COUNT(email) FROM UserInfo WHERE email = {} and password = {}'.format(user_email,user_password)
        userexists = cursor.execute(query).fetchall()
        cursor.close()

        if userexists[0][0] == 1:
            print("userexists",userexists)

            return redirect(url_for('albums', message=user_email))   #we login via this path

        else:
            flash('Incorrect password or username')
            print("not a registered user")
            return redirect("/login")
        
    return render_template('index.j2')

@app.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        user_email = '"'+request.form["email"]+'"'
        user_password = '"'+request.form["password"]+'"'
        print(user_email,user_password)

        connection = sqlite3.connect("sqlite/users.db")
        cursor = connection.cursor()

        query = 'SELECT COUNT(email) FROM UserInfo WHERE email = {}'.format(user_email)
        userexists = cursor.execute(query).fetchall()
        print("userexists",userexists)

        if userexists[0][0]==1:
            print("user already exists") # need to do something else
            flash('User already registered')
            return redirect("/login")


        else:
            newUserQuery = '''Insert Into UserInfo(email,password) Values({},{})'''.format(user_email,user_password)
            count = cursor.execute(newUserQuery)
            connection.commit()
            cursor.close()
            print(count)
            print("user-registered")

            return redirect(url_for('albums', message=user_email))
            
    return render_template("register.html")

@app.route("/albums", methods=['GET', 'POST'])
def albums():

    if request.method == 'GET':
        user_email = request.args.get('message')

        connection = sqlite3.connect("sqlite/mytest.db")
        cursor = connection.cursor()
        query = 'SELECT imagelink, imagetitle, imagedescription, associatedalbum from UserTreePictures Where email = {} and albumcover = True'.format(user_email)
        print(query)
        albumdata = cursor.execute(query).fetchall()

    if request.method == 'POST':
        user_email = request.args.get('message')
        connection = sqlite3.connect("sqlite/mytest.db")
        cursor = connection.cursor()
        query = 'SELECT imagelink, imagetitle, imagedescription, associatedalbum from UserTreePictures Where email = {} and albumcover = True'.format(user_email)
        print(query)
        albumdata = cursor.execute(query).fetchall()
        

    return render_template("albums.j2", albumdata=albumdata,user_email=user_email)

@app.route("/otheralbums", methods=['GET', 'POST'])
def otheralbums():
    # print(request.form)
    # other_email = request.form["other_email"]
    # other_email='"'+other_email+'"'
    user_email = request.args.get('message')

    if request.method == 'POST':
        print(request.form)
        other_email = request.form["other_email"]
        other_email='"'+other_email+'"'
        print("inside_method",other_email)

    else:
        other_email = request.args.get('other_email')
        other_email='"'+other_email+'"'
   
    connection = sqlite3.connect("sqlite/mytest.db")
    cursor = connection.cursor()
    query = 'SELECT imagelink, imagetitle, imagedescription, associatedalbum from UserTreePictures Where email = {} and albumcover = True'.format(other_email)
    print(query)
    albumdata = cursor.execute(query).fetchall()

  


    return render_template("otheralbums.j2", albumdata=albumdata,other_email=other_email,user_email=user_email)


@app.route("/browseusers", methods=['GET', 'POST'])
def browseusers():
    user_email = request.args.get('message')
  

    connection = sqlite3.connect("sqlite/users.db")
    cursor = connection.cursor()
    query = 'SELECT email FROM UserInfo ORDER BY email'
    users= cursor.execute(query).fetchall()

   

    return render_template("browseusers.j2", users=users, user_email=user_email)

@app.route("/deletealbum", methods=['GET', 'POST'])
def deletealbum():
    print("in delete album")

    associatedalbum = request.form["associatedalbum"]
    print("associatedalbum",associatedalbum)
    associatedalbum = '"' + associatedalbum + '"'
    user_email = request.args.get('message')

    
    connection = sqlite3.connect("sqlite/mytest.db")
    cursor = connection.cursor()
    print(associatedalbum)

    deleteImagesQuery = '''SELECT imagelink from UserTreePictures where associatedalbum = {}'''.format(associatedalbum)
    print(deleteImagesQuery)

    imagelinks = cursor.execute(deleteImagesQuery).fetchall()
    print(imagelinks)

    deleteDatabaseEntries = '''DELETE FROM UserTreePictures Where associatedalbum = {}'''.format(associatedalbum)
    deleteEntries = cursor.execute(deleteDatabaseEntries)

    for link in imagelinks:
        dellink = "rcrowland15/"+link[0]
        print(dellink)
        delete_blob('treephotos',dellink)

    connection.commit()
    cursor.close()

    return redirect(url_for('albums', message=user_email))


@app.route("/createalbum", methods=['GET', 'POST'])
def createalbum():
    print("here",request.method)
    print(request)
    user_email = request.args.get('message')
    # user_email='"'+user_email+'"'
    print("createalbum is here",user_email)

    if request.method == 'POST':
        print(request.form)
        print(request.files)

        urlcreatedforalbum = generateurl()
    
        username = "album@gmail.com"    #this should be the same as blob location in final
        blob_location = "treephotos/rcrowland15"

        # album cover
        imageupload = request.files['imageAlbumUpload']
        print("check",[imageupload])
        albumname = request.form["albumname"]
        albumcontents = request.form["albumcontents-input"]


        # get_image_info(imageupload)

        # journal entry
        # imageupload2 = request.files['imageUpload2']
        # journalname = request.form["journal-name-input0"]
        # journalcontent = request.form["journal-content-input0"]


        journalimages = []
        journalnames = []
        journalcontents = []

        for key,val in request.files.items():
            if key!= "imageAlbumUpload":
                journalimages.append(val)

        count = 3
        for key,val in request.form.items():
            if key!= "albumname" and key!= "albumcontents":

                if count%2: journalcontents.append(val)
                else: journalnames.append(val)
                count+=1

        
        print("here check",journalimages)
        print("journalnames",journalnames)
        print("journalcontents", journalcontents)
        
        #store album info in blob
        bucket_name = "treephotos"
        strippedalbumname = albumname.replace(" ","").lower().replace("#","1")
        print(strippedalbumname)
        destination_blob_name = "rcrowland15/"+urlcreatedforalbum+".jpg"
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename
        blob.upload_from_file(imageupload)

        print(f"File {imageupload} uploaded to {destination_blob_name}.")

        # store album info in database
        connection = sqlite3.connect("sqlite/mytest.db")
        cursor = connection.cursor()
        # tempname = '"'+strippedalbumname+'.jpg"'
        tempname = '"'+urlcreatedforalbum+'.jpg"'
        tempalbumname = '"'+albumname+'"'
        tempalbumcontents = '"'+albumcontents+'"'
        tempstrippedalbumname = '"'+strippedalbumname+'"'
        query = '''Insert Into UserTreePictures Values ({}, {}, True,{}, {}, {}, "1/1/2025")'''.format(user_email,tempname,tempstrippedalbumname,tempalbumname,tempalbumcontents)
        count = cursor.execute(query)
        connection.commit()
        print("Executed")
        cursor.close()

        for i in range(len(journalimages)):
            journalimage = journalimages[i]
            journalname = journalnames[i]
            journalcontent = journalcontents[i]
            urlcreatedforjournalentry = generateurl()

            # store journal entry in blob
            bucket_name = "treephotos"
            strippedjournalname = journalname.replace(" ","").lower().replace("#","1")
            print(strippedjournalname)
            destination_blob_name = "rcrowland15/"+urlcreatedforjournalentry+".jpg"
            storage_client = storage.Client()
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename
            blob.upload_from_file(journalimage)


            # store journal entry in database (I think i need an extra field for associated album)
            connection = sqlite3.connect("sqlite/mytest.db")
            cursor = connection.cursor()
            # tempname2 = '"'+strippedjournalname+'.jpg"'
            tempname2 = '"'+urlcreatedforjournalentry+'.jpg"'
            tempjournalname = '"'+journalname+'"'
            tempjournalcontents = '"'+journalcontent+'"'
            query = '''Insert Into UserTreePictures Values ({}, {}, False,{}, {}, {}, "1/1/2025")'''.format(user_email, tempname2,tempstrippedalbumname,tempjournalname,tempjournalcontents)
            print(query)
            count = cursor.execute(query)
            connection.commit()
            print("Executed")
            cursor.close()
        


    return render_template("createalbum.j2",user_email=user_email)


@app.route("/entrytemplate", methods=['GET', 'POST'])
def entrytemplate():

    user_email = request.args.get('message')
   
    print(request.form)
    associatedalbum = request.form["associatedalbum"]

    associatedalbum = '"'+associatedalbum+'"'

    connection = sqlite3.connect("sqlite/mytest.db")
    cursor = connection.cursor()
    query = '''SELECT imagelink, imagetitle, imagedescription, associatedalbum from UserTreePictures Where associatedalbum = {} and albumcover = False'''.format(associatedalbum)
    journaldata = cursor.execute(query).fetchall()

    query2 = '''SELECT imagelink, imagetitle, imagedescription, associatedalbum from UserTreePictures Where associatedalbum = {} and albumcover = True'''.format(associatedalbum)
    albumdata = cursor.execute(query2).fetchall()
    # if request.method == 'POST':
    #     pass

    
    return render_template("entrytemplate.j2", journaldata=journaldata,albumdata=albumdata,user_email=user_email)


# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     print("Here")
#     print(request.form["test5"])

#     treepic = request.form["imagefile"]

#     # this could be a microservice
#     bucket_name = "treephotos"
#     destination_blob_name = "somenewname"
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name) # destination blob name can have a folder created by document/newfilename
#     blob.upload_from_string(treepic)

#     print(f"File {treepic} uploaded to {destination_blob_name}.")

#     return 'File uploaded successfully'

if __name__ == '__main__':
    #app.run(port=5656,debug=True)
    print('starting to run here', flush=True)
    app.run(debug=True)
    