import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

app = Flask(__name__)



app.config['SECRET_KEY']='secretkey'

currdir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(currdir,"./database/song.sqlite3")



db= SQLAlchemy()
db.init_app(app)


with app.app_context():
    db.create_all()

from music import routes

from music.api import AlbumApi,SongApi,PlaylistApi

api=Api(app)
api.add_resource(SongApi,"/api/song","/api/song/<int:song_id>")  
api.add_resource(PlaylistApi,"/api/playlist","/api/playlist/<int:playlist_id>") 
api.add_resource(AlbumApi,"/api/album","/api/album/<int:album_id>")
