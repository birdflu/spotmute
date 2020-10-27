import dbus
import datetime
import time
import os
from argparse import ArgumentParser

def get_spotify_track_metadata():
    session_bus = dbus.SessionBus()
    spotify_bus = session_bus.get_object("org.mpris.MediaPlayer2.spotify",
                                         "/org/mpris/MediaPlayer2")
    spotify_properties = dbus.Interface(spotify_bus,
                                        "org.freedesktop.DBus.Properties")
    metadata = spotify_properties.Get("org.mpris.MediaPlayer2.Player", "Metadata")
    
    return metadata


def log(log_file_name, metadata, delay):
    minutes = int((metadata['mpris:length'] / 1000000) // 60)
    seconds = int((metadata['mpris:length'] / 1000000) % 60)
    length = "" + str(minutes) + ":" + str(seconds)

    file_output = open(log_file_name, "a")
    print(datetime.datetime.today().strftime("%H:%M:%S"),
          metadata['xesam:autoRating'],
          metadata['xesam:discNumber'],
          metadata['xesam:trackNumber'],
          metadata['xesam:title'],
          metadata['mpris:length'],
          length,
          delay,
          file=file_output)
    file_output.close()

def log_header(log_file_name):    
    file_output = open(log_file_name, "w")
    print('sysdate',
          'autoRating',
          'discNumber',
          'trackNumber',
          'title',
          'length(ms)',
          'length(mi:ss)',
          'delay',
          file=file_output)
    file_output.close()
 

def run():

    parser = ArgumentParser()
    parser.add_argument('-o', "--out", action="store", dest="log_file_name", default='advmute.log', type=str, help='log file')
    args = parser.parse_args()

    log_header(args.log_file_name)
   
    currentTrack = ''
    delay = 1;
    while True:
        metadata = get_spotify_track_metadata()
        if metadata['xesam:title'] == 'Advertisement':
            os.system("amixer -D pulse sset Master mute")
            time.sleep(31)
            os.system("amixer -D pulse sset Master unmute")
        else:
            if currentTrack == metadata['xesam:title']:
                delay = delay // pow(metadata['mpris:length'] / 1000000, (1/8))
            else:
                if currentTrack != '' :
                    delay = int(metadata['mpris:length'] / 1000000) // 2 
                currentTrack = metadata['xesam:title']
        if delay < 1:
            delay = 1
        log(args.log_file_name, metadata, delay)
        time.sleep(delay)

run()
