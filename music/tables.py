from music import db

class Users(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name=db.Column(db.String,nullable=False,unique=True)
    email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    profile_pic=db.Column(db.String,nullable=False,default="creator_default_profile.webp")


class Creator(db.Model):
    __tablename__="creator"
    creator_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    creator_name=db.Column(db.String,nullable=False,unique=True)
    creator_email=db.Column(db.String,nullable=False,unique=True)
    creator_about=db.Column(db.String)
    creator_password=db.Column(db.String,nullable=False)
    creator_pic=db.Column(db.String,nullable=False,default="creator_default_profile.webp")
    user_id_registered=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    no_of_follower=db.Column(db.Integer,nullable=False,default=0)
    blacklist=db.Column(db.String,nullable=False,default="False")

class Follower(db.Model):
    __tablename__="follower"
    user_creator_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    creator_id=db.Column(db.Integer,db.ForeignKey("creator.creator_id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)


class Song(db.Model):
    __tablename__="song"
    song_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    song_name=db.Column(db.String,nullable=False)
    song_cover=db.Column(db.String,nullable=False)
    song_lyrics=db.Column(db.String,nullable=False,unique=True)
    song_audio=db.Column(db.String,nullable=False)
    creator_id_registered=db.Column(db.Integer,db.ForeignKey("creator.creator_id"),nullable=False)
    creator_name_registered=db.Column(db.String,db.ForeignKey("creator.creator_name"),nullable=False)
    no_of_likes=db.Column(db.Integer,nullable=False,default=0)
    keywords=db.Column(db.String,nullable=False)

class SongLikes(db.Model):
    __tablename__="songlikes"
    song_like_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.user_id"),nullable=False)
    song_id=db.Column(db.Integer,db.ForeignKey("song.song_id"),nullable=False)

class Playlist(db.Model):
    __tablename__="playlist"
    playlist_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    playlist_name=db.Column(db.String,nullable=False)
    playlist_cover=db.Column(db.String,nullable=False)
    playlist_creator=db.Column(db.String,db.ForeignKey("user.user_name"),nullable=False)

class PlaylistSongs(db.Model):
    __tablename__="playlistsongs"
    song_playlist_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    playlist_id=db.Column(db.Integer,db.ForeignKey("playlist.playlist_id"),nullable=False)
    song_id=db.Column(db.Integer,db.ForeignKey("song.song_id"),nullable=False)


class Album(db.Model):
    __tablename__="album"
    album_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    album_name=db.Column(db.String,nullable=False,unique=True)
    album_cover=db.Column(db.String,nullable=False)
    album_creator=db.Column(db.String,db.ForeignKey("creator.creator_name"),nullable=False)
    album_keywords=db.Column(db.String,nullable=False)

class AlbumSongs(db.Model):
    __tablename__="albumsongs"
    song_album_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    album_id=db.Column(db.Integer,db.ForeignKey("album.album_id"),nullable=False)
    song_id=db.Column(db.Integer,db.ForeignKey("song.song_id"),nullable=False)
       

class Admin(db.Model):
    __tablename__="admin"
    admin_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    