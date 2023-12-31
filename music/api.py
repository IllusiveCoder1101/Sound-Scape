from music import db
from music.tables import Song,Playlist,Album,PlaylistSongs,AlbumSongs,Creator
from music.validation import NotFoundError,ValidationError
from flask_restful import  Resource,marshal_with,fields,reqparse


song_output={
    "song_id":fields.Integer,
    "creator_id_registered":fields.Integer,
    "song_name":fields.String,
    "creator_name_registered": fields.String,
    "likes":fields.Integer,
}

playlist_output={
    "playlist_id":fields.Integer,
    "playlist_name":fields.String,
    "playlist_cover":fields.String,
    "playlist_creator": fields.String,
}

album_output={
    "album_id":fields.Integer,
    "album_name":fields.String,
    "album_cover":fields.String,
    "album_creator":fields.String, 
}

create_song_parser=reqparse.RequestParser()

create_song_parser.add_argument("song_name")
create_song_parser.add_argument("song_cover")
create_song_parser.add_argument("song_lyrics")
create_song_parser.add_argument("song_audio")
create_song_parser.add_argument("song_creator_id")
create_song_parser.add_argument("song_keywords")

update_song_parser=reqparse.RequestParser()


update_song_parser.add_argument("song_name")
update_song_parser.add_argument("song_cover")
update_song_parser.add_argument("song_lyrics")
update_song_parser.add_argument("song_audio")
update_song_parser.add_argument("song_keywords")

create_playlist_parser=reqparse.RequestParser()

create_playlist_parser.add_argument("playlist_name")
create_playlist_parser.add_argument("playlist_cover")
create_playlist_parser.add_argument("playlist_creator")

update_playlist_parser=reqparse.RequestParser()

update_playlist_parser.add_argument("playlist_name")
update_playlist_parser.add_argument("playlist_cover")


create_album_parser=reqparse.RequestParser()

create_album_parser.add_argument("album_name")
create_album_parser.add_argument("album_cover")
create_album_parser.add_argument("album_creator")
create_album_parser.add_argument("album_keywords")


update_album_parser=reqparse.RequestParser()

update_album_parser.add_argument("album_name")
update_album_parser.add_argument("album_cover")
update_album_parser.add_argument("album_keywords")





class SongApi(Resource):

    @marshal_with(song_output)
    def get(self,song_id):

        q=Song.query.filter(Song.song_id == song_id).first()

        if q:
            return q
        else:
            raise NotFoundError(status_code=404)
        
    
  
    def put(self,song_id):
        args=update_song_parser.parse_args()

        song_name=args.get("song_name",None)
        song_cover=args.get("song_cover",None)
        song_lyrics=args.get("song_lyrics",None)
        song_audio=args.get("song_audio",None)
        song_keywords=args.get("song_keywords",None)

        q1=Song.query.filter(Song.song_id == song_id).first()
        if q1:
            q1.song_name=song_name or q1.song_name
            q1.song_cover=song_cover or q1.song_cover
            q1.song_lyrics=song_lyrics or q1.song_lyrics
            q1.song_audio=song_audio or q1.song_audio
            q1.keywords=song_keywords or q1.keywords

            db.session.add(q1)
            db.session.commit()

            return "Successfully Updated",200
        raise NotFoundError(status_code=404)

    def delete(self,song_id):
        q1=Song.query.filter(Song.song_id==song_id).first()
        q2=AlbumSongs.query.filter(AlbumSongs.song_id == song_id).all()
        q3=PlaylistSongs.query.filter(PlaylistSongs.song_id == song_id).all()
        if q1:
            for i in q2:
                db.session.delete(i)
            db.session.commit()
            
            for i in q3:
                db.session.delete(i)
            db.session.commit()

            db.session.delete(q1)
            db.session.commit()
            return "Successfully deleted", 200
        else:
            raise NotFoundError(status_code=404)
    

    def post(self):
        args=create_song_parser.parse_args()

        song_name=args.get("song_name",None)
        song_cover=args.get("song_cover",None)
        song_lyrics=args.get("song_lyrics",None)
        song_audio=args.get("song_audio",None)
        song_keywords=args.get("song_keywords",None)
        song_creator_id=args.get("song_creator_id",None)
        
        
        if not song_creator_id :
            raise ValidationError(error_code="SONG001",error_message="Song Creator Id is required",status_code=400)
        if not song_name or not song_cover or not song_lyrics or not song_audio or not song_keywords :
            raise ValidationError(error_code="SONG002",error_message="Song details are missing",status_code=404)
        
        q1 = Creator.query.filter(Creator.creator_id == int(song_creator_id)).first()
        q2 = Song.query.filter(Song.song_lyrics == song_lyrics).first()
        if not q1:
            raise NotFoundError(status_code=404)
        if q2:
            raise NotFoundError(status_code=409)

        new_song=Song(song_name=song_name,song_cover=song_cover,song_lyrics=song_lyrics,song_audio=song_audio,creator_id_registered = song_creator_id,creator_name_registered=q1.creator_name,keywords=song_keywords)
        db.session.add(new_song)
        db.session.commit()
        return "Successfully Created", 201
    
class PlaylistApi(Resource):
    @marshal_with(playlist_output)
    def get(self,playlist_id):
        q=Playlist.query.filter(Playlist.playlist_id == playlist_id).first()

        if q:
            return q
        else:
            raise NotFoundError(status_code=404)
        
    def put(self,playlist_id):
        args=update_playlist_parser.parse_args()
        playlist_name=args.get("playlist_name",None)
        playlist_cover=args.get("playlist_cover",None)
      

        
        q1=Playlist.query.filter(Playlist.playlist_id == playlist_id).first()
        if q1:
            q1.playlist_name=playlist_name or q1.playlist_name
            q1.playlist_cover=playlist_cover or q1.playlist_cover
        
            db.session.add(q1)
            db.session.commit()
            return "Successfully Updated", 200
        
        raise NotFoundError(status_code=404)

    
    def delete(self,playlist_id):
        q1=Playlist.query.filter(Playlist.playlist_id== playlist_id).first()
        
        if q1:
            q2=PlaylistSongs.query.filter(PlaylistSongs.playlist_id == playlist_id).all()
            if len(q2)>0:
                for i in q2:
                    db.session.delete(i)
                db.session.commit()

            db.session.delete(q1)
            db.session.commit()
            return "Successfully deleted", 200
        else:
            raise NotFoundError(status_code=404)
    
    
    def post(self):
        args=create_playlist_parser.parse_args()
        playlist_name=args.get("playlist_name",None)
        playlist_cover=args.get("playlist_cover",None)
        playlist_creator=args.get("playlist_creator",None)

        if not playlist_creator  :
            raise ValidationError(error_code="PLAYLIST001",error_message="Playlist Creator Name is required",status_code=400)
        if not playlist_name or not playlist_cover :
            raise ValidationError(error_code="PLAYLIST002",error_message="Playlist details are missing",status_code=400)
        
        q=Playlist.query.filter(Playlist.playlist_creator == playlist_creator).first()

        if not q:
            raise NotFoundError(status_code=404)
  

        new_playlist=Playlist(playlist_name=playlist_name,playlist_cover=playlist_cover,playlist_creator=playlist_creator)
        db.session.add(new_playlist)
        db.session.commit()

        return "Successfully Created",201



class AlbumApi(Resource):
    @marshal_with(album_output)
    def get(self,album_id):
        q=Album.query.filter(Album.album_id == album_id).first()

        if q:
            return q
        else:
            raise NotFoundError(status_code=404)

    def put(self,album_id):
        args=update_album_parser.parse_args()
        album_name=args.get("album_name",None)
        album_cover=args.get("album_cover",None)
      

        
        q1=Album.query.filter(Album.album_id == album_id).first()
        if q1:
            q1.album_name=album_name or q1.album_name
            q1.album_cover=album_cover or q1.album_cover
        
            db.session.add(q1)
            db.session.commit()
            return "Successfully updated",200
        
        raise NotFoundError(status_code=404)

    
    def delete(self,album_id):
        q1=Album.query.filter(Album.album_id== album_id).first()
        
        if q1:
            q2=AlbumSongs.query.filter(AlbumSongs.album_id == album_id).all()
            if len(q2)>0:
                for i in q2:
                    db.session.delete(i)
                db.session.commit()

            db.session.delete(q1)
            db.session.commit()
            return "Successfully deleted", 200
        else:
            raise NotFoundError(status_code=404)
    
    
    def post(self):
        args=create_album_parser.parse_args()
        album_name=args.get("album_name",None)
        album_cover=args.get("album_cover",None)
        album_creator=args.get("album_creator",None)
        album_keywords=args.get("album_keywords",None)
        if not album_creator  :
            raise ValidationError(error_code="ALBUM001",error_message="Album Creator Name is required",status_code=400)
        if not album_name or not album_cover or not album_keywords :
            raise ValidationError(error_code="ALBUM002",error_message="Album details are missing",status_code=400)
        
        q=Creator.query.filter(Creator.creator_name == album_creator).first()

        if not q:
            raise NotFoundError(status_code=404)
        q1=Album.query.filter(Album.album_name == album_name).first()

        if q1:
            raise NotFoundError(status_code=409)

        new_album=Album(album_name=album_name,album_cover=album_cover,album_creator=album_creator,album_keywords=album_keywords)
        db.session.add(new_album)
        db.session.commit()

        return "Successfully Created",201
