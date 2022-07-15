# importing packages
from pytube import YouTube
from pytube import Playlist
from pydub import AudioSegment
import os

def mp3_download(url, destination):
    # extract audio
    try:
        video = url.streams.filter(only_audio=True).first()
        # download
        print(f"Downloading video: '{url.title}'...")
        out_file = video.download(output_path=destination)

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp4'
        os.rename(out_file, new_file)

        # converting the file to mp3
        given_audio = AudioSegment.from_file(out_file, format="mp4")
        given_audio.export(out_file, format="mp3")

        # rename the file
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

    except:
        print(f"Error! video: '{url.title} ({url})' failed, check failed.txt")
        with open('failed.txt', 'a+') as f:
            f.write(f'{url.title} ({url})\n')

def single_download():
    # url input from user
    url = YouTube(str(input("Enter the URL of the video you want to download: \n>> ")))

    # check for destination to save file
    print("Enter the destination (leave blank for current directory)")
    destination = str(input(">> ")) or '.'

    mp3_download(url=url, destination=destination)

def playlist_download():
    # url input from user
    playlist_url = Playlist(str(input("Enter the URL of the playlist you want to download: \n>> ")))
    print("Enter Destination path (leave blank for current directory)")
    destination = input('>> ') or f'./{playlist_url.title}'
    print(playlist_url.title)
    for video in playlist_url.videos:
        mp3_download(video, destination)

def bulk_playlist_download():
    file = open('playlists.txt')

    for line in file:
        playlist_url = Playlist(str(line))
        print("Enter Destination path (leave blank for current directory)")
        destination = f'{playlist_url.title}'
        print(f'Now downloading playlist: {playlist_url.title}')
        for video in playlist_url.videos:
            mp3_download(video, destination)

while True:
    print('''
        Select option:
        [1] Download video as mp3
        [2] Download playlist as mp3
        [3] Bulk download playlists from playlists.txt
        [0] Exit
        ''')
    n = int(input(">> "))
    if n == 1: single_download()
    if n == 2: playlist_download()
    if n == 3: bulk_playlist_download()
    if n == 0: break
