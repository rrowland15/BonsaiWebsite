import sqlite3

connection = sqlite3.connect("sqlite/mytest.db")
cursor = connection.cursor()

# rows = cursor.execute("SELECT * from UserAlbums").fetchall()
# print(rows)


#CREATE TABLE UserTreePictures (email varchar(255), imagelink varchar(255), albumcover Bool, associatedalbum varchar(255), imagetitle  varchar(255), imagedescription varchar(1000), picturedate datetime);

query1 = 'Insert Into UserTreePictures Values ("album@gmail.com", "shishi.jpg", True, "Shishigashira", "Shishigashira", "Acquired Summer 2023 from Mount Vernon", "1/1/2025")'
query2 = 'Insert Into UserTreePictures Values ("album@gmail.com", "elm.jpg", True, "Siberian Elm", "Grown from seed from Indiana", "1/1/2019")'
query3 = 'Insert Into UserTreePictures Values ("album@gmail.com", "satsuki.jpg", True, "Satsuki Azalea", "Gifted by deep-sea diver", "1/1/2025")'
query4 = 'Insert Into UserTreePictures Values ("album@gmail.com", "jbp.jpg", True, "Japanese Black Pine", "Acquired Summer 2023", "1/1/2025")'
query5 = 'Insert Into UserTreePictures Values ("album@gmail.com", "redjm.jpg", True, "Japanese Maple #1", "Grown from seed collected 2020", "1/1/2025")'
query6 = 'Insert Into UserTreePictures Values ("album@gmail.com", "goldjun.jpg", True, "Golden Juniper Chinensis", "Acquired Spring 2020 as nursery stock", "1/1/2025")'


queries = [query1,query2,query3,query4,query5,query6]

for query in queries:

    count = cursor.execute(query)
    connection.commit()
    print("Executed")

cursor.close()