# blog-project
# I. Introduction
Welcome to my Blog Web Application.
To see a demo, watch this youtube video displaying the project(https://youtu.be/Zb_7Ufm5yqs).
This project uses Flask, Javascript(jQuery, Fetch API), PostgreSQL.
This project includes the following features:
  * Uses Flask-Login for login and registration purposes
  * Uses Flask-SQLAlchemy to create models for PostgreSQL database.
  * Enables users the ability to make posts, search for posts, look for posts they have made, like and dislike posts/comments, edit/delete/make/reply to comments
  * Uses Fetch-API to dynamically insert/update/ delete comments, likes, dislikes, and posts
# II. Using the Application
1. clone the repo (open in vscode)
```
https://github.com/XNickyChenX2022/blog-project.git
```
2. Install Libraries
```
$ pip install -r requirements.txt
```
3. Setup and Activate virual environment. In the terminal, type the following commands for pc (see https://flask.palletsprojects.com/en/2.3.x/installation/ for mac instructions)
```
py -3 -m venv .venv
.venv\Scripts\activate
```
4. Create Postgresql database (install postgresql and use pgAdmin4) 
create a server in pgadmin. Then in pgadmin create database (mine was called blog_database, remember this for later). Use the following below for initializing the server.
* Hostname/address: localhost
* Port:5432
* Username:Postgres
* Password:Your Password
5. In Configuration.py (in the app folder, under templates folder) change the SQLALCHEMY_DATABASE_URI to connect to your database locally.Fill in the placeholders shown in Config.py. See Example Below
```
class Config:
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/blog_database'
SQLALCHEMY_TRACK_MODIFICATIONS = False
```

6. go to the terminal and type the following commands to install the database.
```
python
from app import db, app
app.app_context().push()
db.create_all()
exit()
```
7. Now in the terminal type:
```
python ./run.py
```
8. Run the application on
```
http://127.0.0.1:5000
```
For any issues, email me at nickychen2022@gmail.com
