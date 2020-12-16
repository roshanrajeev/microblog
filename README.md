  <p align="center">
    <h2 align="center">Flask Microblog Application</h2>
    <p align="center">
      Hear what people have to say
      <br>
      <a href="https://roshan-flask-microblog.herokuapp.com/">View App</a>
    </p>
  </p>
  
  
 ## About The Project

Microblog is a web application created using Flask and Jinja2 templates.Demo version of this application is deployed on Heroku and is available at [roshan-flask-microblog.herokuapp.com](https://roshan-flask-microblog.herokuapp.com/). Posts are publicly visible to all registered users and can follow other users to see their post in their home page.

Database defaults to sqlite if no specific database is configured. Database is managed using Flask-SQLAlchemy ORM and migrations are created using Flask-Migrate. Live notifications are enabled making use of Flask-SocketIO. 

 ## Features
 
 Some of the features of the application includes

- Public Posting
- Private Messaging
- Live Notifications


## Demo Deployment

Clone the repo
```
git clone git@github.com:roshanrajeev/microblog.git
cd microblog
```

Setting virtual env
```
python3 -v venv env
source env/bin/activate
```

Install and run server
```
pip install -r requirements.txt
flask run
```
To configure database, create a .env file and add DATABASE_URL environment variable. See
[SQLAlchemy Engine Config](https://docs.sqlalchemy.org/en/13/core/engines.html) for learn more about configuring database. 

```flask run``` doesn't load the sockets and so, live notification won't be available.
Run ```python microblog.py``` to start local server with live notifications enabled.

## Testing

Run unit tests 
```
python tests.py
```
