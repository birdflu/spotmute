import dbus
import datetime


def get_spotify_track_metadata():
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")

    return metadata


def log(metadata):
    minutes = int((metadata['mpris:length'] / 1000000) // 60)
    seconds = int((metadata['mpris:length'] / 1000000) % 60)
    length = "" + str(minutes) + ":" + str(seconds)
    
    file_output = open("/tmp/output.txt", "a")
    print(datetime.datetime.today().strftime("%H:%M:%S"),
          metadata['xesam:autoRating'],
          metadata['xesam:discNumber'],
          metadata['xesam:trackNumber'],
          metadata['xesam:title'],
          metadata['mpris:length'],
          length, file=file_output)
    file_output.close()

def run(count):
    while count > 0:
        log(get_spotify_track_metadata())
        count -= 1  

run(3)
