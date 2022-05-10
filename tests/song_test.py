"""Tests the songs"""
import pytest
from app.db.models import db, Song, User
@pytest.fixture()
def write_test_csv():
     # write a dummy csv file for testing
    header = ['Name', 'Artist', 'Year', 'Genre']
    data = [
        ['Move (Keep Walkin’)', "TobyMac", '2015', 'Christian'],
        ['Edge Of My Seat', "TobyMac", '2018', 'Christian'],
    ]

    with open('music.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)



@pytest.fixture()
def add_user_to_db():
    user = User('gnb5@gmail.com', '12345678', 0)
    db.session.add(user)
    db.session.commit()

def test_adding_songs(application, add_user_to_db):
    """Test adding songs"""
    with application.app_context():
        user = User.query.filter_by(email="gnb5@gmail.com").first()
        # prepare songs to insert
        user.songs = [Song("title0", "artist0", "2022", "Pop"), Song("title2", "artist2", "2019", "Rap")]
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='title0').first()
        assert song1.title == "title0"

def test_deleting_song(application, add_user_to_db):
    """Test deleting the song"""
    user = User.query.filter_by(email="gnb5@gmail.com").first()
    # prepare songs to insert
    user.songs = [Song("title0", "artist0", "2022", "Pop")]
    db.session.commit()
    song = Song.query.filter_by(title='title0').first()
    # delete the song
    db.session.delete(song)
    #assert db.session.query(Song).count() == 0

def test_updating_songs(application, add_user_to_db):
    """Test updating song"""
    with application.app_context():
        user = User.query.filter_by(email="gnb5@gmail.com").first()
        # prepare songs to insert
        user.songs = [Song("title0", "artist0", "2022", "Pop")]
        db.session.commit()
        # changing the title of the song
        song = Song.query.filter_by(title='title0').first()
        song.title = "New Song"
        db.session.commit()
        updated_song = Song.query.filter_by(title='New Song').first()
        assert updated_song.title == "New Song"