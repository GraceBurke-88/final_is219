import csv
import logging
import os

from flask import Blueprint, render_template, abort, url_for, current_app, jsonify, flash
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound

from app.songs.forms import song_edit_form
from app.db import db
from app.db.models import Song
from app.songs.forms import csv_upload
from werkzeug.utils import secure_filename, redirect

songs = Blueprint('songs', __name__, template_folder='templates')

@songs.route('/songs', methods=['GET'], defaults={"page": 1})
@songs.route('/songs/<int:page>', methods=['GET'])
def songs_browse(page):
    page = page
    per_page = 1000
    pagination = Song.query.paginate(page, per_page, error_out=False)
    data = pagination.items
    edit_url = ('songs.edit_song', [('song_id' , ':id')])
    try:
        return render_template('browse_songs.html', record_type="Songs", Song=Song, data=data,pagination=pagination, edit_url=edit_url)
    except TemplateNotFound:
        abort(404)

@songs.route('/songs_datatables/', methods=['GET'])
def browse_songs_datatables():
    data = Location.query.all()
    try:
        return render_template('browse_songs_datatables.html')
    except TemplateNotFound:
        abort(404)

@songs.route('/songs/<int:song_id>/edit', methods=['POST', 'GET'])
@login_required
def edit_song(song_id):
    song = Song.query.get(song_id)
    form = song_edit_form(obj=song)
    if form.validate_on_submit():
        song.title = form.title.data
        #user.is_admin = int(form.is_admin.data)
        db.session.add(song)
        db.session.commit()
        flash('Song Edited Successfully', 'success')
        current_app.logger.info("edited a song")
        return redirect(url_for('songs.songs_browse'))
    return render_template('song_edit.html', form=form)

@songs.route('/songs/upload', methods=['POST', 'GET'])
@login_required
def songs_upload():
    form = csv_upload()
    if form.validate_on_submit():
        log = logging.getLogger("myApp")

        filename = secure_filename(form.file.data.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        form.file.data.save(filepath)
        #user = current_user
        list_of_songs = []
        with open(filepath) as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                list_of_songs.append(Song(row['Name'],row['Artist'], row['Year'],row['Genre']))

        current_user.songs = list_of_songs
        db.session.commit()

        return redirect(url_for('songs.songs_browse'))

    try:
        return render_template('upload.html', form=form)
    except TemplateNotFound:
        abort(404)
'''

@songs.route('/api/song/<int:song_id>', methods=['GET'])
@login_required
def retrieve_song(song_id):
    spotify_api_key = current_app.config.get('SPOTIFY_API_KEY')
    song = Song.query.get(song_id)
    song_name = song.title.replace(" ", "%20")
    song_artist = song.artist.replace(" ", "%20")
    return render_template('song_view.html', song=song, song_id=song_id, song_name=song_name, song_artist=song_artist, spotify_api_key=spotify_api_key)



@songs.route('/api/song/<int:song_id>')
@login_required
def retrieve_song(song_id):
    spotify_api_key = current_app.config.get('SPOTIFY_API_KEY')
    song = Song.query.get(song_id)
    song_name = song.title.replace(" ", "%20")
    song_artist = song.artist.replace(" ", "%20")
    return render_template('display_songs.html', song=song, song_id=song_id, song_name=song_name, song_artist=song_artist, spotify_api_key=spotify_api_key)

'''
@songs.route('/songs/uploads', methods=['GET'])
def songs_display():
    spotify_api_key = current_app.config.get('SPOTIFY_API_KEY')
    try:
        return render_template('display_songs.html',spotify_api_key=spotify_api_key)
    except TemplateNotFound:
        abort(404)


@songs.route('/api/songs/', methods=['GET'])
def api_songs():
    data = Song.query.all()
    try:
        return jsonify(data=[song.serialize() for song in data])
    except TemplateNotFound:
        abort(404)

