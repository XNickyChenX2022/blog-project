# blog-project
# I. Introduction
Welcome to my Blog Web Application.
This project uses Flask, Javascript(jQuery, Fetch API), PostgreSQL.
This project includes the following features:
  * Uses Flask-Login for login and registration purposes
  * Uses Flask-SQLAlchemy to create models for PostgreSQL database.
  * Enables users the ability to make posts, search for posts, look for posts they have made, like and dislike posts/comments, edit/delete/make/reply to comments
  * Uses Fetch-API to dynamically insert/update/ delete comments, likes, dislikes, and posts
# II. Using the Application
1.clone the repo (open in vscode)
```
https://github.com/XNickyChenX2022/blog-project.git
```
2.Install Libraries
```
$ pip install -r requirements.txt
```
3.Create Postgresql database (install postgresql and use pgAdmin4)
	create a server in pgadmin. Then in pgadmin create database (mine was called blog_database, remember this for later). Use the following below for initializing the server.
   * Hostname/address: localhost
   * Port:5432
   * Username:Postgres
   * Password:Your Password
4. In Configuration.py (in the app folder, under templates folder) change the SQLALCHEMY_DATABASE_URI to connect to your database locally.
   See Example Below
   ```
   class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/blog_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```
   Fill in the placeholders shown in Config.py
5. go to the terminal and type the following commands to install the database.
```
python
from app import db, app
app.app_context().push()
db.create_all()
exit()
```
6. Now in the terminal type:
```
python ./run.py
```
7. Run the application on
```
http://127.0.0.1:5000
```
