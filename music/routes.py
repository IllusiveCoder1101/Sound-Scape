from flask import render_template,request,session,redirect
from music import app,db,tables
import matplotlib.pyplot as plt


# FUNCTIONS



def song_delete(song_id):
    q=tables.AlbumSongs.query.filter(tables.AlbumSongs.song_id == song_id).all()
    q1=tables.PlaylistSongs.query.filter(tables.PlaylistSongs.song_id == song_id).all()
    q2=tables.Song.query.filter(tables.Song.song_id == song_id).first()
    for i in q:
        db.session.delete(i)
    db.session.commit()
    for j in q1:
        db.session.delete(j)
    db.session.commit()
    db.session.delete(q2)
    db.session.commit()

def album_delete(album_id):
    q=tables.AlbumSongs.query.filter(tables.AlbumSongs.album_id == album_id).all()
    q1=tables.Album.query.filter(tables.Album.album_id == album_id).first()

    for i in q:
        db.session.delete(i)
    db.session.commit()

    db.session.delete(q1)
    db.session.commit()

def playlist_delete(playlist_id):
    q=tables.PlaylistSongs.query.filter(tables.PlaylistSongs.playlist_id == playlist_id).all()
    q1=tables.Playlist.query.filter(tables.Playlist.playlist_id == playlist_id).first()

    for i in q:
        db.session.delete(i)
    db.session.commit()

    db.session.delete(q1)
    db.session.commit()


'''#####################
   #####################
   ####### USER ########
   #####################
   #####################'''

@app.route("/")

def index():
    return render_template("landing.html")

@app.route("/user_login",methods=["POST","GET"])

def user_login():
    if request.method == "POST":
        email=request.form["email"]
        password=request.form["password"]
        q=tables.Users.query.filter(tables.Users.email == email,tables.Users.password == password).first()
        if q:
            session["email"]=email
            return redirect("/user_dashboard")
        else:
            return render_template("login.html",error="Invalid Email or Password.")
    return render_template("login.html" ,error="")

@app.route("/user_register",methods=["POST","GET"])

def user_register():
    if request.method == "POST":
        username=request.form["username"]
        email=request.form["email"]
        password=request.form["password"]
        confirm_password=request.form["confirm_password"]
        q1=tables.Users.query.filter(tables.Users.user_name == username).first()
        q=tables.Users.query.filter(tables.Users.email == email).first()
        if q1:
            return render_template("register.html",error="Name Already Exists")
        if q:
            return render_template("register.html",error="Email Already Exists")
        if password != confirm_password:
            return render_template("register.html",error="Password Does Not Match.")
        new_User=tables.Users(user_name=username,email=email,password=password)
        db.session.add(new_User)
        db.session.commit()
        return redirect("/user_login")
    return render_template("register.html",error="")

@app.route("/user_dashboard",methods=["GET","POST"])

def user_dashboard():
    if session.get("email"):
        q1=tables.Playlist.query.filter().all()
        q3=tables.Users.query.filter(tables.Users.email == session["email"]).first()
        q4=tables.Playlist.query.filter(tables.Playlist.playlist_creator==q3.user_name).all()
        q5=tables.Creator.query.filter(tables.Creator.blacklist == "False").all()
        songs=[]
        albums=[]
        song_tags=[]
        album_tags=[]
        for i in q5:
            q=tables.Song.query.filter(tables.Song.creator_id_registered == i.creator_id).all()
            q2=tables.Album.query.filter(tables.Album.album_creator == i.creator_name).all()
            songs.append(q)
            albums.append(q2)
            for j in q:
                tmp=j.keywords.split(" ")
                for k in tmp:
                    if k not in song_tags and k !="":
                        song_tags.append(k)
            for l in q2:
                tmp1=l.album_keywords.split(" ")
                for m in tmp1:
                    if m not in album_tags and m!="":
                        album_tags.append(m)

        followed=[]
        notfollowed=[]
        for i in q5:
            q6=tables.Follower.query.filter(tables.Follower.creator_id == i.creator_id,tables.Follower.user_id == q3.user_id).first()
            if q6:
                followed.append(i)
            else:
                notfollowed.append(i)
        if request.method == "POST":
            song=request.form.get("search_song") or False
            album=request.form.get("search_album") or False
            if song:
                song_collection=[]
                final=[]
                for i in songs:
                    for j in i:
                        if song.lower() in j.song_name.lower() or song.lower() in j.creator_name_registered.lower() or song.lower() in j.keywords:
                            song_collection.append(j)
                final.append(song_collection)
                if len(song_collection)>0:
                    return render_template("dashboard.html",song=final,playlist=q1,album=albums,your_playlist=q4,name=q3.user_name,followed_creator=followed,unfollowed_creator=notfollowed,user_id=q3.user_id,song_tags=song_tags,album_tags=album_tags,error="")
                else:
                    return render_template("dashboard.html",song=songs,playlist=q1,album=albums,your_playlist=q4,name=q3.user_name,followed_creator=followed,unfollowed_creator=notfollowed,user_id=q3.user_id,song_tags=song_tags,album_tags=album_tags,error="song")
            if album:
                album_collection=[]
                final1=[]
                for i in albums:
                    for j in i:
                        if album.lower() in j.album_name.lower() or album.lower() in j.album_creator.lower() or album.lower() in j.album_keywords:
                            album_collection.append(j)
                final1.append(album_collection)
                if len(album_collection)>0:
                    return render_template("dashboard.html",song=songs,playlist=q1,album=final1,your_playlist=q4,name=q3.user_name,followed_creator=followed,unfollowed_creator=notfollowed,user_id=q3.user_id,song_tags=song_tags,album_tags=album_tags,error="")
                else:
                    return render_template("dashboard.html",song=songs,playlist=q1,album=albums,your_playlist=q4,name=q3.user_name,followed_creator=followed,unfollowed_creator=notfollowed,user_id=q3.user_id,song_tags=song_tags,album_tags=album_tags,error="album")
            

        return render_template("dashboard.html",song=songs,playlist=q1,album=albums,your_playlist=q4,name=q3.user_name,followed_creator=followed,unfollowed_creator=notfollowed,user_id=q3.user_id,song_tags=song_tags,album_tags=album_tags,error="")
    return redirect("/user_login")
    
@app.route("/follow/<user_id>/<creator_id>")

def follow(user_id,creator_id):
   if session.get("email"):
        q=tables.Creator.query.filter(tables.Creator.creator_id == creator_id).first()
        q.no_of_follower = int(q.no_of_follower)+1
        db.session.commit()

        new_follower=tables.Follower(user_id=user_id,creator_id=creator_id)
        db.session.add(new_follower)
        db.session.commit() 
        return redirect("/user_dashboard")
   return redirect("/user_login")

@app.route("/unfollow/<user_id>/<creator_id>")

def unfollow(user_id,creator_id):
    if session.get("email"):
        q=tables.Creator.query.filter(tables.Creator.creator_id == creator_id).first()
        if q.no_of_follower >0:
            q.no_of_follower = int(q.no_of_follower)-1
        db.session.commit()

        delete_follower=tables.Follower.query.filter(tables.Follower.user_id == user_id,tables.Follower.creator_id == creator_id).first()
        db.session.delete(delete_follower)
        db.session.commit() 
        return redirect("/user_dashboard")
    return redirect("/user_login")

@app.route("/user_profile",methods=["GET","POST"])

def user_profile():
    if session.get("email") :
        q=tables.Users.query.filter(tables.Users.email == session["email"]).first()
        q1=tables.Playlist.query.filter(tables.Playlist.playlist_creator == q.user_name).first()
        if request.method == "POST":
            name=request.form["username"]
            email=request.form["email"]
            password=request.form["password"]
            pic=request.form["upload-pic"]
            q3=tables.Users.query.filter(tables.Users.user_name == name , tables.Users.user_id != q.user_id).first()
            q2=tables.Users.query.filter(tables.Users.email == email, tables.Users.user_id != q.user_id).first()
            if q3:
               return render_template("profile.html",data=q,error="Name already taken.")
            if q2:
                return render_template("profile.html",data=q,error="Email already taken.")
            q.user_name=name or q.user_name
            q.email=email or q.email
            q.password=password or q.password
            
            q.profile_pic=pic or  q.profile_pic
            q1.playlist_creator = name or q1.playlist_creator
            db.session.commit()

            return redirect("/user_profile")
        return render_template("profile.html",data=q,error="")
    return redirect("/user_login")


@app.route("/song/user/<song_id>")

def song_user(song_id):
    if session.get("email"):
        q=tables.Song.query.filter(tables.Song.song_id == song_id).first()
        q1=tables.Users.query.filter(tables.Users.email == session.get("email")).first()
        q2=tables.SongLikes.query.filter(tables.SongLikes.song_id== song_id,tables.SongLikes.user_id == q1.user_id).first()
        if q2:
            like=True
        else:
            like=False
        return render_template("song.html",song=q,context="user",user_id=q1.user_id,likes=like)
    else:
        return redirect("/user_login")

@app.route("/song/like/<user_id>/<song_id>")

def like(user_id,song_id):
    if session.get("email"):
        q=tables.Song.query.filter(tables.Song.song_id == song_id).first()
        q.no_of_likes=int(q.no_of_likes)+1
        db.session.commit()
        new_like=tables.SongLikes(user_id=user_id,song_id=song_id)
        db.session.add(new_like)
        db.session.commit()
        return redirect(f"/song/user/{song_id}")
    return redirect("/user_login")

@app.route("/song/dislike/<user_id>/<song_id>")

def dislike(user_id,song_id):
    if session.get("email"):
        q=tables.Song.query.filter(tables.Song.song_id == song_id).first()
        if q.no_of_likes>0:
            q.no_of_likes=int(q.no_of_likes)-1
        db.session.commit()
        delete_like=tables.SongLikes.query.filter(tables.SongLikes.user_id==user_id,tables.SongLikes.song_id==song_id).first()
        db.session.delete(delete_like)
        db.session.commit()
        return redirect(f"/song/user/{song_id}")
    return redirect("/user_login")


@app.route("/user_createplaylist",methods=["GET","POST"])

def user_createplaylist():
    
    if session.get("email"):
        q=tables.Song.query.filter().all()
        if request.method == "POST":
            playlist_name=request.form["playlist_name"]
            playlist_cover=request.form["playlist_cover"]
            playlist_songs=request.form.getlist("song")
            q0=tables.Playlist.query.filter(tables.Playlist.playlist_name == playlist_name).first()
            if q0:
                return render_template("playlist.html",song=q,error="Playlist name not available.")
            q2=tables.Users.query.filter(tables.Users.email == session["email"]).first()
            new_playlist=tables.Playlist(playlist_name = playlist_name,playlist_cover=playlist_cover,playlist_creator=q2.user_name)
            db.session.add(new_playlist)
            db.session.commit()
            q1=tables.Playlist.query.filter(tables.Playlist.playlist_name == playlist_name).first()
            new_playlist_song=[]
            for i in playlist_songs:
                new_playlist_song.append(tables.PlaylistSongs(playlist_id=q1.playlist_id,song_id=i))
            db.session.add_all(new_playlist_song)
            db.session.commit()
            return redirect("/user_dashboard")
                
        return render_template("playlist.html",song=q,error="")
    else:
        return redirect("/user_login")

@app.route("/playlist/update/<playlist_id>",methods=["GET","POST"])

def user_update_playlist(playlist_id):
    if session.get("email"):
        q=tables.Playlist.query.filter(tables.Playlist.playlist_id == playlist_id).first()
        q1=tables.PlaylistSongs.query.filter(tables.PlaylistSongs.playlist_id == playlist_id).all()
        q2=tables.Song.query.filter().all()
      
        if request.method == "POST":
            playlist_name=request.form["playlist_name"]
            playlist_cover=request.form["playlist_cover"]
            playlist_songs=request.form.getlist("song")

            q3=tables.Playlist.query.filter(tables.Playlist.playlist_name == playlist_name,tables.Playlist.playlist_id != q.playlist_id).first()

            if q3:
                return render_template("playlist_update.html",song=q2,playlist_data=q,error="Playlist name not available.")

            q.playlist_name=playlist_name or q.playlist_name
            q.playlist_cover = playlist_cover or q.playlist_cover
            db.session.commit()
            if len(playlist_songs)>0:
                for i in q1:
                    db.session.delete(i)
                db.session.commit()
                data=[]
                for i in playlist_songs:
                    data.append(tables.PlaylistSongs(playlist_id=playlist_id,song_id=i))
                db.session.add_all(data)
                db.session.commit()
            return redirect("/user_dashboard")
        
        return render_template("playlist_update.html",song=q2,playlist_data=q,error="")
    else:
        return redirect("/user_login")


@app.route("/playlist/delete/<playlist_id>")

def user_delete_playlist(playlist_id):
    if session.get("email"):
        playlist_delete(playlist_id)
        return redirect("/user_dashboard")
    else:
        return redirect("/user_login")

@app.route("/playlist/<playlist_id>")

def playlist(playlist_id):
    if session.get("email"):
        q=tables.PlaylistSongs.query.filter(tables.PlaylistSongs.playlist_id == playlist_id).all()
        q1=tables.Playlist.query.filter(tables.Playlist.playlist_id == playlist_id).first()
        songs=[]
        for i in q:
            songs.append(tables.Song.query.filter(tables.Song.song_id == i.song_id).first())
        return render_template("playlist_view.html",song=songs,playlist=q1)
    else:
        return redirect("/user_login")

@app.route("/album/user/<album_id>")

def album_user(album_id):
    if session.get("email"):
        q=tables.AlbumSongs.query.filter(tables.AlbumSongs.album_id == album_id).all()
        q1=tables.Album.query.filter(tables.Album.album_id == album_id).first()
        songs=[]
        for i in q:
            songs.append(tables.Song.query.filter(tables.Song.song_id == i.song_id).first())
        return render_template("album_view.html",song=songs,album=q1,context="user")
    else:
        return redirect("/user_login")
  


@app.route("/user_logout")

def user_logout():
    if session.get("email"):
        session.pop("email")
        return redirect("/")
    else:
        return redirect("/user_login")

'''#####################
   #####################
   ##### CREATOR #######
   #####################
   #####################'''

@app.route("/creator_account")

def creator_account():
    if session.get("email"):
        q1=tables.Users.query.filter(tables.Users.email == session["email"]).first()
        q=tables.Creator.query.filter(tables.Creator.user_id_registered == q1.user_id).first()
        if q:
            return redirect("/creator_dashboard")
        else:
            return redirect("/creator_register")
    else:
        return redirect("/user_login")
    


@app.route("/creator_register",methods=["POST","GET"])

def creator_register():
    q2=tables.Users.query.filter(tables.Users.email == session["email"]).first()
    q3=tables.Creator.query.filter(tables.Creator.user_id_registered == q2.user_id).first()
    if  q3:
        return redirect("/creator_dashboard")
    if session.get("email") :
        if request.method == "POST":
            username=request.form["username"]
            email=request.form["email"]
            password=request.form["password"]
            confirm_password=request.form["confirm_password"]
            q1=tables.Users.query.filter(tables.Users.email == session["email"]).first()
            q=tables.Creator.query.filter(tables.Creator.creator_email == email).first()
            q2=tables.Creator.query.filter(tables.Creator.creator_name == username).first()

            if q2:
                return render_template("creator_register.html",error="Name is already taken.")
            if q:
                return render_template("creator_register.html",error="Email is already taken.")
            if password != confirm_password:
                return render_template("creator_register.html",error="Passwords does not match.")
            
            new_Creator=tables.Creator(creator_name=username,creator_email=email,creator_password=password,user_id_registered=q1.user_id)
            db.session.add(new_Creator)
            db.session.commit()
            return redirect("/creator_dashboard")
        return render_template("creator_register.html",error="")
    else:
        return redirect("/user_login")
    




@app.route("/creator_dashboard",methods=["GET","POST"])

def creator_dashboard():
    if session.get("email"):
        q=tables.Users.query.filter(tables.Users.email == session["email"]).first()
        q1=tables.Creator.query.filter(tables.Creator.user_id_registered == q.user_id).first()
        q2=tables.Song.query.filter(tables.Song.creator_id_registered == q1.creator_id).all()
        q3=tables.Album.query.filter(tables.Album.album_creator == q1.creator_name).all()
        q4=tables.Follower.query.filter(tables.Follower.creator_id == q1.creator_id).all()
        return render_template("creator_dashboard.html",song=q2,album=q3,name=q1.creator_name,no_of_songs=len(q2),no_of_albums=len(q3),no_of_followers=len(q4),blacklist=q1.blacklist)
    else:
        if not session.get("email"):
            return redirect("/user_login")
        

@app.route("/creator_profile",methods=["GET","POST"])

def creator_profile():
    if session.get("email") :
        q=tables.Users.query.filter(tables.Users.email == session["email"]).first()
        q1=tables.Creator.query.filter(tables.Creator.user_id_registered == q.user_id).first()
        q2=tables.Album.query.filter(tables.Album.album_creator == q1.creator_name).first()
        if request.method == "POST":
            name=request.form["creator_name"]
            email=request.form["creator_email"]
            password=request.form["password"]
            pic=request.form["upload-pic"]
            about=request.form["creator_about"]
            q4=tables.Creator.query.filter(tables.Creator.creator_email == email,tables.Creator.creator_id != q1.creator_id).first()
            q3=tables.Creator.query.filter(tables.Creator.creator_name == name,tables.Creator.creator_id != q1.creator_id).first()
            if q3:
               return render_template("creator_profile.html",data=q1,error="Name is Already Taken.")
            if q4:
                return render_template("creator_profile.html",data=q1,error="Email is already taken.")
            q1.creator_name=name or q1.creator_name
            q1.creator_email=email or q1.creator_email
            q1.creator_password=password or q1.creator_password
            q1.creator_about=about or q1.creator_about
            q1.creator_pic=pic or  q1.creator_pic
            if q2:
                q2.album_creator=name or q2.album_creator
            db.session.commit()

            return redirect("/creator_profile")
        return render_template("creator_profile.html",data=q1,error="")
    return redirect("/user_login")
        

@app.route("/creator_addsong",methods=["GET","POST"])

def creator_addsong():
    if request.method == "POST":
        song_name=request.form["song_name"]
        song_lyrics=request.form["song_lyrics"]
        song_cover=request.form["song_cover"]
        song_audio=request.form["song_audio"]
        song_keywords=request.form["song_keywords"]
        q1=tables.Users.query.filter(tables.Users.email == session["email"]).first()
        q2=tables.Creator.query.filter(tables.Creator.user_id_registered == q1.user_id).first()
        q=tables.Song.query.filter(tables.Song.song_lyrics == song_lyrics).first()

        if q:
            return render_template("add_song.html",error="Song lyrics already exists.")
        newSong=tables.Song(song_name=song_name,song_lyrics=song_lyrics,song_cover=song_cover,song_audio=song_audio,creator_id_registered=q2.creator_id,creator_name_registered=q2.creator_name,keywords=song_keywords)
        db.session.add(newSong)
        db.session.commit()
        return redirect("/creator_dashboard")
    return render_template("add_song.html",error="")

@app.route("/song/creator/<song_id>")

def song_creator(song_id):
    if session.get("email"):
        q=tables.Song.query.filter(tables.Song.song_id == song_id).first()
        
        return render_template("song.html",song=q,context="creator")
    else:
        return redirect("/user_login")

@app.route("/song/creator/delete/<song_id>")

def creator_song_delete(song_id):
    if session.get("email"):
        song_delete(song_id)
        return redirect("/creator_dashboard")
    else:
        return redirect("/user_login")

@app.route("/song/update/<song_id>",methods=["GET","POST"])

def update_song(song_id):
    if session.get("email"):
        q=tables.Song.query.filter(tables.Song.song_id == song_id).first()
        if request.method == "POST":
            song_name=request.form["song_name"]
            song_cover=request.form["song_cover"]
            song_audio=request.form["song_audio"]
            song_lyrics=request.form["song_lyrics"]
            song_keywords=request.form["song_keywords"]
            q1=tables.Song.query.filter(tables.Song.song_lyrics == song_lyrics,tables.Song.song_id != q.song_id).first()

            if q1:
               return render_template("update_song.html",data=q,error="Song lyrics already exists.")
            q.song_name=song_name or q.song_name
            q.song_cover=song_cover or q.song_cover
            q.song_audio=song_audio or q.song_audio
            q.song_lyrics = song_lyrics or q.song_lyrics
            q.keywords=song_keywords or q.keywords
            db.session.commit()
            return redirect("/creator_dashboard")

        return render_template("update_song.html",data=q,error="")
    else:
        return redirect("/user_login")
    

@app.route("/creator_addalbum",methods=["GET","POST"])

def creator_addalbum():
    
    if session.get("email") :
        q3=tables.Users.query.filter(tables.Users.email == session["email"]).first()
        q4=tables.Creator.query.filter(tables.Creator.user_id_registered == q3.user_id).first()
        q=tables.Song.query.filter(tables.Song.creator_id_registered == q4.creator_id).all()
        if request.method == "POST":
            
            album_name=request.form["album_name"]
            album_cover=request.form["album_cover"]
            album_songs=request.form.getlist("song")
            album_keywords=request.form["album_keywords"]
            q2=tables.Album.query.filter(tables.Album.album_name == album_name).first()
            if q2:
                return render_template("album.html",song=q,error="Album Name already taken.")
            
            new_album=tables.Album(album_name = album_name,album_cover=album_cover,album_creator=q4.creator_name,album_keywords=album_keywords)
            db.session.add(new_album)
            db.session.commit()
            q1=tables.Album.query.filter(tables.Album.album_name == album_name).first()
            new_album_song=[]
            for i in album_songs:
                new_album_song.append(tables.AlbumSongs(album_id=q1.album_id,song_id=i))
            db.session.add_all(new_album_song)
            db.session.commit()
            return redirect("/creator_dashboard")

        return render_template("album.html",song=q,error="")
    else:
        if not session.get("email"):
            return redirect("/user_login")

@app.route("/album/update/<album_id>",methods=["GET","POST"])

def creator_update_album(album_id):
    if session.get("email"):
        q=tables.Album.query.filter(tables.Album.album_id == album_id).first()
        q1=tables.AlbumSongs.query.filter(tables.AlbumSongs.album_id == album_id).all()
        q3=tables.Users.query.filter(tables.Users.email == session.get("email")).first()
        q4=tables.Creator.query.filter(tables.Creator.user_id_registered == q3.user_id).first()
        q2=tables.Song.query.filter(tables.Song.creator_id_registered == q4.creator_id).all()
        
        if request.method == "POST":
            album_name=request.form["album_name"]
            album_cover=request.form["album_cover"]
            album_songs=request.form.getlist("song")
            album_keywords=request.form["album_keywords"]
            q5=tables.Album.query.filter(tables.Album.album_name == album_name,tables.Album.album_id != q.album_id).first()
            if q5:
                return render_template("update_album.html",song=q2,album_data=q,error="Album name already taken.")
            q.album_name=album_name or q.album_name
            q.album_cover = album_cover or q.album_cover
            q.album_keywords=album_keywords or q.album_keywords
            db.session.commit()
            if len(album_songs)>0:
                for i in q1:
                    db.session.delete(i)
                db.session.commit()
                data=[]
                for i in album_songs:
                    data.append(tables.AlbumSongs(album_id=album_id,song_id=i))
                db.session.add_all(data)
                db.session.commit()
            return redirect("/creator_dashboard")
        return render_template("update_album.html",song=q2,album_data=q,error="")
    else:
        return redirect("/user_login")


@app.route("/album/creator/delete/<album_id>")

def creator_album_delete(album_id):
    if session.get("email"):
        album_delete(album_id)
        return redirect("/creator_dashboard")
    else:
        return redirect("/user_login")

    

@app.route("/album/creator/<album_id>")

def album_creator(album_id):
    if session.get("email"):
        q=tables.AlbumSongs.query.filter(tables.AlbumSongs.album_id == album_id).all()
        q1=tables.Album.query.filter(tables.Album.album_id == album_id).first()
        songs=[]
        for i in q:
            songs.append(tables.Song.query.filter(tables.Song.song_id == i.song_id).first())
        return render_template("album_view.html",song=songs,album=q1,context="creator")
    else:
        return redirect("/user_login")
  

@app.route("/creator_logout")

def creator_logout():
    if session.get("email") :
  
        return redirect("/user_dashboard")
    else:
        if not session.get("email"):
            return redirect("/user_login")


'''#####################
   #####################
   ##### ADMIN #########
   #####################
   #####################'''



@app.route("/admin_login",methods=["POST","GET"])

def admin_login():
    if request.method == "POST":
        email=request.form["email"]
        password=request.form["password"]
        q=tables.Admin.query.filter(tables.Admin.email == email,tables.Admin.password == password).first()
        if q:
            session["admin_email"]=email
            return redirect("/admin_dashboard")
        else:
            return render_template("adminLogin.html",error="Invalid Email or Password.")
    return render_template("adminLogin.html",error="")

@app.route("/admin_dashboard",methods=["GET","POST"])

def admin_dashboard():
    if session.get("admin_email"):
        q=tables.Users.query.all()
        q1=tables.Creator.query.filter().order_by(tables.Creator.no_of_follower).all()
        q2=tables.Song.query.filter().order_by(tables.Song.no_of_likes).all()
        q3=tables.Album.query.all()
        q4=tables.Playlist.query.all()

        song_name=[]
        song_like=[]
        ctr=0
        for i in range (len(q2)-1,-1,-1):
            song_name.append(q2[i].song_name)
            song_like.append(q2[i].no_of_likes)
            ctr+=1
            if ctr == 5:
                break

        creator_name=[]
        creator_follower=[]
        ctr1=0
        for i in range(len(q1)-1,-1,-1):
            creator_name.append(q1[i].creator_name)
            creator_follower.append(q1[i].no_of_follower)
            ctr1+=1
            if ctr1 ==5:
                break
      
        plt.figure(figsize=(7.5,5))
        plt.subplot(111)
        plt.bar(creator_name,creator_follower)
        plt.xlabel("Creator Names")
        plt.ylabel("creator followers")
        
        plt.savefig("./music/static/images/creator_follower.png")
        
        plt.figure(figsize=(7.5,5))
        plt.subplot(111)
        plt.bar(song_name,song_like)
        plt.xlabel("Song Names")
        plt.ylabel("Song Likes")
    
        plt.savefig("./music/static/images/song.png")
        if request.method == "POST":
            choice=request.form["graph_choice"]
            return render_template("admin_dashboard.html",data=[len(q),len(q1),len(q2),len(q3),len(q4)],ch=choice)

        return render_template("admin_dashboard.html",data=[len(q),len(q1),len(q2),len(q3),len(q4)],ch="song")
    else:
        return redirect("/admin_login")

@app.route("/admin_song")

def admin_song():
    if session.get("admin_email"):
        q=tables.Song.query.filter().all()
        return render_template("admin_song.html",data=q)
    else:
        return redirect("/admin_login")

@app.route("/song/admin/delete/<song_id>")

def admin_song_delete(song_id):
    if session.get("admin_email"):
        song_delete(song_id)
        return redirect("/admin_song")
    else:
        return redirect("/admin_login")


@app.route("/admin_creator")

def admin_creator():
    if session.get("admin_email"):
        q=tables.Creator.query.filter().all()
        creator_data=[]
        tmp={}
        for i in q:
            q1=tables.Song.query.filter(tables.Song.creator_id_registered == i.creator_id).all()
            q2=tables.Album.query.filter(tables.Album.album_creator == i.creator_name).all()
            tmp={"creator_name":i.creator_name,"creator_pic":i.creator_pic,"creator_email":i.creator_email,"creator_about":i.creator_about,"creator_songs":q1,"creator_album":q2,"blacklist":i.blacklist,"creator_id":i.creator_id}
            creator_data.append(tmp)
        return render_template("admin_creator.html",data=creator_data)
    else:
        return redirect("admin_login")

@app.route("/admin_album")

def admin_album():
    if session.get("admin_email"):
        q=tables.Album.query.filter().all()
        album_data=[]
        tmp={}
        for i in q:
            q1=tables.AlbumSongs.query.filter(tables.AlbumSongs.album_id == i.album_id).all()
            tmp1=[]
            for j in q1:
                q2=tables.Song.query.filter(tables.Song.song_id == j.song_id).first()
                tmp1.append(q2)
            tmp={"album_creator":i.album_creator,"album_cover":i.album_cover,"album_name":i.album_name,"album_songs":tmp1,"album_id":i.album_id}
            album_data.append(tmp)
        return render_template("admin_album.html",data=album_data)
    else:
        return redirect("/admin_login")

@app.route("/album/admin/delete/<album_id>")

def admin_album_delete(album_id):
    if session.get("admin_email"):
        album_delete(album_id)
        return redirect("/admin_album")
    else:
        return redirect("/admin_login")

@app.route("/blacklist/<creator_id>")

def blacklist(creator_id):
    if session.get("admin_email"):
        q=tables.Creator.query.filter(tables.Creator.creator_id == creator_id).first()
        q.blacklist="True"
        db.session.commit()
        return redirect("/admin_creator")
    else:
        return redirect("/admin_login")

@app.route("/whitelist/<creator_id>")

def whitelist(creator_id):
    if session.get("admin_email"):
        q=tables.Creator.query.filter(tables.Creator.creator_id == creator_id).first()
        q.blacklist="False"
        db.session.commit()
        return redirect("/admin_creator")
    else:
        return redirect("/admin_login")

@app.route("/admin_logout")

def admin_logout():
    if session.get("admin_email"):
        session.pop("admin_email")
    return redirect("/admin_login")
  