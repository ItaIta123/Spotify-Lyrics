import os
import sys
import time
import json
import spotipy
import webbrowser
import Lyrics_Player
import spotipy.util as util
import Spotify_keys
from json.decoder import JSONDecodeError

"""
The program started as a solution to the absence of good lyrics on Spotify's app/web (at the time of writing this 
program there was no adequate lyrics on Spotify's app/web). 

How to run the program:

1. The first phase would be to create an "APP" on Spotify's Developers website:
 (https://developer.spotify.com/dashboard/applications)

2. After creating the 'APP' go to EDIT SETTINGS and paste whatever link into the Redirect URI section.
 I've used https://www.google.com/

3. Open the terminal and run the following three lines:
    export SPOTIPY_CLIENT_ID=''  'Your_Client_ID' (obtained from the APP's page on Spotify's Dashboard)
    export SPOTIPY_CLIENT_SECRET=''         'Your_SECRET_Client_ID' (obtained from the APP's page on Spotify's Dashboard)
    export SPOTIPY_REDIRECT_URI='https://www.google.com/'    'Whatever link you chose to the redirect URI.

4. Write the 'Installation code' below and save the file.

5. Remember to change directory (cd) to the python file's directory

6. Run the program in your terminal in the following way: python3 'Your file name'.py 'Your Spotify user name'

7. Your browser will open. Click OK and copy the URl to the terminal and run it.
"""

# Running from the Terminal:
# username = sys.argv[1]
# scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-read-private ' \
#         'playlist-read-collaborative user-top-read user-read-recently-played'
# # Try to assign to "token" the permission token:(Basically the first login)
# try:
#     token = util.prompt_for_user_token(username,
#                                        scope,
#                                        client_id=Spotify_keys.client_id(),
#                                        client_secret=Spotify_keys.client_secret(),
#                                        redirect_uri='https://www.google.com/')
# except:
#     # os.remove(f".cache-{username}")
#     token = util.prompt_for_user_token(username, scope)

username = 'itamarfayler'
#
# the specific permissions requests:
scope = 'user-read-private user-read-playback-state user-modify-playback-state playlist-read-private ' \
        'playlist-read-collaborative user-top-read user-read-recently-played'
token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id= Spotify_keys.client_id(),
                                   client_secret= Spotify_keys.client_secret(),
                                   redirect_uri='https://www.google.com/')

# Create the Spotify object (this The object we are going to work with for everything in thr library):

spotify_object = spotipy.Spotify(auth=token)

# Evert time we want to extract new data from the Spotify's API we need to use:
# spotify_object.'the_builtin_module'('parameters'). examples fpr all the modules can be found at
# https://spotipy.readthedocs.io/en/2.12.0/#examples
# The logged-in user information:

user = spotify_object.current_user()
# print(json.dumps(user, sort_keys=True, indent=4)) # Used to print the information in a more readable way
display_name = user['display_name']


# *********************************************************************************************************************

def play(song_uri=None, artist_name=None, song_name=None, list_of_songs_uri=None):
    # # Get current dives info: (includes volume level, kind of device, id and etc...)
    """

    :param list_of_songs_uri:
    :param song_uri: song's uri. This is how Spotify reads each track/album/artist...
    :param artist_name:
    :param song_name:
    :return: start playing the track
    """

    devices = spotify_object.devices()
    # print(json.dumps(devices, sort_keys=True, indent=4))
    try:
        device_ID = devices['devices'][0]['id']
    except IndexError:
        print()
        print('Your Spotify app is not open. Open it and try again')
        print()
    else:
        # # In a case were the function play is used by outside program the inputs only artist and song names
        # if song_uri is None and list_of_songs_uri is None:
        #     artist_results = spotify_object.search(q='artist:' + artist_name, type='artist')
        #     print(artist_results)
        #     song_results = spotify_object.search(q='track:' + song_name, type='track')
        #     print(song_results)
        #     return results
        # spotify_object.start_playback(device_id=device_ID, uris=list_of_songs_uri)
        # else:
        if song_uri is not None:  # I.E. it is a specific song and not a list of songs
            # if song_num_input is not None:
            play_track_URI_lst = list([])  # For some reason, in order to play a song you can't the string of the URI.
            # Even if you have only one song, i.e. one URI, you must pass it in a list.
            # Playing a track from the list of all songs with index numbers:
            play_track_URI_lst.append(song_uri)
            print()
            print(f'Playing {song_name} by {artist_name}, Enjoy :)')
            print()
            spotify_object.start_playback(device_ID, None, play_track_URI_lst)
        else:
            spotify_object.start_playback(device_ID, None, list_of_songs_uri)


def get_artist_Albums_and_tracks(artist_name):
    # All the atrist's Spotify information:
    # global found_song, user_song_num
    search_results = spotify_object.search(artist_name, 1, 0, 'artist')
    # print(json.dumps(search_results, sort_keys=True, indent=4))
    # Get search results:
    # search(q, limit=10, offset=0, type='track', market=None)
    # q - the search query (see how to write a query in the
    # limit - the number of items to return (min = 1, default = 10, max = 50) we would usually want only one
    # (the most popular one).
    # offset - the index of the first item to return.
    # type - the type of item to return. One of ‘artist’, ‘album’,
    # ‘track’, ‘playlist’, ‘show’, or ‘episode’

    # Artist details:
    try:
        artist = search_results['artists']['items'][0]
    except IndexError:
        print()
        print("Artist name does not exist. Please make sure there are no typos and try again")
        print()
    else:  # The program continues only if the artist name exists in Spotify
        artistID = artist['id']

        # Get Albums data:
        albums_data = spotify_object.artist_albums(artistID)
        # print(json.dumps(albums_data, sort_keys=True, indent=4))
        albums_data = albums_data['items']
        song_number_increment = 0  # The song index in the list
        list_of_songs_names = []
        list_of_tracks_URI = []  # The list of each of the songs's URI for future play() function song usage.

        # The Loop that goes through each of the artist's albums:
        for item in albums_data:
            print("Album: " + item['name'])
            album_ID = item['id']
            print()

            # Get tracks of each album:
            tracks_search_results = spotify_object.album_tracks(album_ID)
            tracks_search_results = tracks_search_results['items']
            for song_details in tracks_search_results:
                print(f'{song_number_increment}: {song_details["name"]}')
                # print(json.dumps(song_details, sort_keys=True, indent=4))
                song_number_increment += 1
                list_of_songs_names.append(song_details['name'])
                list_of_tracks_URI.append(song_details['uri'])
            print()

        while True:
            # 1 Main menu
            print()
            print('*' * 80)
            print('What would you like to do now?')
            print()
            print('1 - Get song lyrics')
            print()
            print('2 - Play song')
            print()
            print('3 - Play song with lyrics')
            print()
            print('0 - exit')
            print()
            user_num_choice = input("Enter your choice: ")
            print()
            print('*' * 80)

            # Exit:
            if user_num_choice == '0':
                print('*' * 80)
                break

            # Get Lyrics
            elif user_num_choice == '1':
                print(
                    "* IMPORTANT! * I suggest to give it a few tries as the lyrics database is sometimes inconsistent")
                print()
                user_song_pick = input("Enter a song name or number: ")
                try:
                    user_song_num = int(user_song_pick)
                except ValueError:  # It is not a number. (It is a song name)
                    for song_name in list_of_songs_names:  # Taking the possibility that the user didn't entered the full name of the song.
                        found_song = False
                        if user_song_pick in song_name:
                            Lyrics_Player.get_lyrics(artist_name, song_name)
                            found_song = True
                            break
                    if not found_song:
                        print()
                        print("invalid song name. Please make sure the song name is correct and try again")
                        print()
                        time.sleep(2)
                else:  # if it is a number
                    try:  # check if the index is valid
                        lyrics_for_song_name = list_of_songs_names[
                            user_song_num]  # Choosing the correct song by the number-song index
                    except IndexError:  # If the number is indeed out of range
                        print()
                        print("The song number is invalid. Please make sure that the song number exist")
                        print()
                    else:  # if the number is in range
                        Lyrics_Player.get_lyrics(artist_name, lyrics_for_song_name)

            # Play song
            elif user_num_choice == '2':
                user_song_pick = input("Enter a song name or number: ")
                try:
                    user_song_num = int(user_song_pick)  # checks whether it is a number or a song name
                except ValueError:  # If it is a song name:
                    for song_name in list_of_songs_names:  # Taking the possibility that the user didn't entered the
                        # full name of the song.
                        found_song = False
                        if user_song_pick in song_name:
                            song_index = list_of_songs_names.index(song_name)
                            song_uri = list_of_tracks_URI[song_index]
                            play(song_uri, artist_name, song_name)
                            found_song = True
                            break
                    if not found_song:
                        print()
                        print("invalid song name. Please make sure the song name is correct and try again")
                        print()
                        time.sleep(2)
                else:  # If it is actually a number.
                    try:  # Check whether the number is in valid index
                        song_name = list_of_songs_names[user_song_num]
                    except IndexError:
                        print()
                        print("The song number is invalid. Please make sure that the song number exist")
                        print()
                    else:
                        song_index = user_song_num
                        song_uri = list_of_tracks_URI[song_index]
                        play(song_uri, artist_name, song_name)

            # Play song with lyrics
            elif user_num_choice == '3':
                user_song_pick = input("Enter a song name or number: ")
                try:
                    user_song_num = int(user_song_pick)
                except ValueError:  # It is not a number i.e it is a song name:
                    for song_name in list_of_songs_names:  # Taking the possibility that the user didn't entered the full name of the song.
                        found_song = False
                        if user_song_pick in song_name:  # even if it is only a partial name
                            song_index = list_of_songs_names.index(song_name)
                            song_uri = list_of_tracks_URI[song_index]
                            print()
                            Lyrics_Player.get_lyrics(artist_name, song_name)
                            time.sleep(1)
                            play(song_uri, artist_name, song_name)
                            time.sleep(5)
                            found_song = True
                            break
                    if not found_song:
                        print()
                        print("invalid song name. Please make sure the song name is correct and try again")
                        print()
                        time.sleep(2)
                else:  # It is a number:
                    try:  # Check if the number is valid:
                        song_name = list_of_songs_names[user_song_num]
                    except IndexError:
                        print()
                        print("The song number is invalid. Please make sure that the song number exist")
                        print()
                    else:
                        song_index = user_song_num
                        song_uri = list_of_tracks_URI[song_index]
                        print('Just a few seconds...')
                        print()
                        Lyrics_Player.get_lyrics(artist_name, song_name)
                        time.sleep(1)
                        play(song_uri, artist_name, song_name)
                        time.sleep(5)
            else:
                print()
                print("Number entered is not valid. Please enter a valid number")
                print()


def playlists():
    user_playlists = spotify_object.current_user_playlists()
    user_playlists = user_playlists['items']
    playlist_numbering = 0
    playlists_id_list = []
    playlists_names_list = []
    for playlist in user_playlists:
        print(f'{playlist_numbering} - {playlist["name"]}')
        playlist_numbering += 1
        playlists_names_list.append(playlist['name'])
        playlists_id_list.append(playlist['id'])
    while True:
        print()
        print('*' * 80)
        print("What would you like to do now?")
        print()
        print("1 - Show and play all playlist's tracks")
        print()
        print('0 - exit')
        print()
        print('*' * 80)
        user_num_choice = input("Enter your choice: ")
        print()
        # Exit:
        if user_num_choice == "0":
            break
        # One playlist's tracks
        elif user_num_choice == "1":
            user_playlist_num = input("Enter playlist number: ")
            try:  # checks if the number is a valid index
                chosen_playlist_name = playlists_names_list[int(user_playlist_num)]
            except IndexError:
                print()
                print("Playlist number is not valid. Please chose a valid playlist number and try again.")
                print()
            else:
                chosen_playlist_id = playlists_id_list[int(user_playlist_num)]
                chosen_playlist_tracks = spotify_object.playlist_tracks(chosen_playlist_id)
                chosen_playlist_tracks = chosen_playlist_tracks['items']
                track_numerating = 0
                # print(json.dumps(chosen_playlist_tracks[0]['track'], sort_keys=True, indent=4))
                print(f"{chosen_playlist_name} tracks:")
                print()
                playlist_track_name_list = []
                playlist_track_uri_list = []
                playlist_artist_name_list = []
                for track_info in chosen_playlist_tracks:
                    print(f"{track_numerating} - {track_info['track']['name']}")
                    playlist_track_name_list.append(track_info['track']['name'])
                    playlist_track_uri_list.append(track_info['track']['uri'])
                    playlist_artist_name_list.append(track_info['track']['album']['artists'][0]['name'])
                    track_numerating += 1
                while True:
                    print()
                    print('*' * 80)
                    print("what would you like to do now?")
                    print()
                    print("1 - Play a specific song with lyrics")
                    print()
                    print("2 - Play all current playlist's tracks")
                    print()
                    print('0 - exit')
                    print()
                    print('*' * 80)
                    user_num_choice = input("Enter your choice: ")
                    print()
                    if user_num_choice == '0':
                        break
                    # Play a specific song with lyrics:
                    elif user_num_choice == '1':
                        user_song_num = input("Enter song number: ")
                        song_name = playlist_track_name_list[int(user_song_num)]
                        print(f'song name: {song_name}')
                        song_uri = playlist_track_uri_list[int(user_song_num)]
                        song_artist = playlist_artist_name_list[int(user_song_num)]
                        print(f'song artist: {song_artist}')
                        Lyrics_Player.get_lyrics(song_artist, song_name)
                        time.sleep(1)
                        play(song_uri, song_artist, song_name)
                    # Play all playlist with lyrics
                    elif user_num_choice == '2':
                        # Lyrics_Player.get_lyrics(song_artist, song_name)

                        play(None, None, None,
                             playlist_track_uri_list)  # Once I insert a list of uri's it play them all
                        # One by one. we can then use the next() previous and etc. functions.
                        time.sleep(0.5)
                        current_song_lyrics()
                        music_player_interface()

                    else:
                        print()
                        print("invalid number entered. Please try again")
                        print()
        else:
            print()
            print("invalid number entered. Please try again")
            print()


def user_top():
    while True:
        print("Your top tracks: ")
        print()
        print("1 - recently")
        print()
        print("2 - all-time")
        print()
        print('0 - exit')
        print()
        user_answer = input("Enter your choice: ")
        print()
        if user_answer == '0':
            break

        if user_answer == '1' or 'recently':
            user_top_tracks = spotify_object.current_user_top_tracks(limit=20, offset=0, time_range='short_term')
            user_top_tracks = user_top_tracks['items']
            user_top_tracks_names_list = []
            user_top_tracks_uri_list = []
            user_top_tracks_artist_name_list = []
            top_track_numerating = 0
            # print(json.dumps(user_top_tracks, sort_keys=True, indent=4))
            for track in user_top_tracks:
                print(f"{top_track_numerating} - {track['name']}")
                user_top_tracks_names_list.append(track['name'])
                user_top_tracks_uri_list.append(track['uri'])
                user_top_tracks_artist_name_list.append(track['album']['artists'][0]['name'])
                top_track_numerating += 1
            play(None, None, None, user_top_tracks_uri_list)


        elif user_answer == '2' or 'all-time' or 'all time':
            user_top_tracks_long = spotify_object.current_user_top_tracks(limit=20, offset=0, time_range='long_term')
            user_top_tracks_long = user_top_tracks_long['items']
            user_top_tracks_names_list_long = []
            user_top_tracks_uri_list_long = []
            user_top_tracks_artist_name_list_long = []
            top_track_numerating = 0
            # print(json.dumps(user_top_tracks, sort_keys=True, indent=4))
            for track in user_top_tracks_long:
                print(f"{top_track_numerating} - {track['name']}")
                user_top_tracks_names_list_long.append(track['name'])
                user_top_tracks_uri_list_long.append(track['uri'])
                user_top_tracks_artist_name_list_long.append(track['album']['artists'][0]['name'])
                top_track_numerating += 1
            play(None, None, None, user_top_tracks_uri_list_long)
        else:
            print()
            print("Number is invalid. Please enter a valid number and try again.")
            print()

    # for song in user_recently_played:
    #     print(song['track']['name'])


# Main function:
def main():
    # Main menu
    while True:
        print()
        print(f"Welcome to Spotify Lyrics {display_name} !")
        print()
        print("What would you like to do?")
        print()
        print("1 - Enter the name of your favorite artist to see the best of their work and more!")
        print()
        print('2 - Get Only lyrics')
        print()
        print('3 - Play your favorite playlists with lyrics! ')
        print()
        print('4 - Current playing song lyrics')
        # print('4 - See and play your top listed tracks ')
        print()
        print('0 - exit')
        print()
        user_num_choice = input("Enter your choice: ")
        print()
        # Exit:
        if user_num_choice == '0':
            print("Bye Bye and thank you ")
            print()
            break

        # Favorite artist options::
        elif user_num_choice == '1':
            while True:
                print()
                print('What would you like to do?')
                print()
                print("1 - See all artist's albums and songs")
                print()
                print("2- see your artist's top songs")
                print()
                print('0 - exit')
                print()
                user_input = input("Enter your choice: ")
                print()
                # Break:
                if user_input == '0':
                    break

                # See all artist's albums and songs:
                elif user_input == '1':
                    artist_name = input("Enter your favorite artist name: ")
                    get_artist_Albums_and_tracks(artist_name)

                # see your artist's top songs:
                elif user_input == '2':
                    artist_name = input("Enter your favorite artist name: ")
                    search_results = spotify_object.search(artist_name, 1, 0, 'artist')
                    try:
                        artist = search_results['artists']['items'][0]
                    except IndexError:
                        print()
                        print("Artist name does not exist. Please make sure there are no typos and try again")
                        print()
                    else:  # The program continues only if the artist name exists in Spotify
                        artistID = artist['id']
                        artist_top_songs = spotify_object.artist_top_tracks(artistID)['tracks']
                        # print(json.dumps(artist_top_songs, sort_keys=True, indent=4))
                        song_numerating = 0
                        artist_top_songs_name_list = []
                        artist_top_songs_uri_list = []
                        for song in artist_top_songs:
                            print(f"{song_numerating} - {song['name']}")
                            artist_top_songs_name_list.append(song['name'])
                            artist_top_songs_uri_list.append(song['uri'])
                            song_numerating += 1
                        while True:
                            print()
                            print("What would you like to do now?")
                            print()
                            print("1 - Play a specific song with lyrics")
                            print()
                            print("2 - Play all current top artist's tracks with lyrics")
                            print()
                            print('0 - exit')
                            print()
                            print('*' * 80)
                            user_num_choice = input("Enter your choice: ")
                            print()
                            if user_num_choice == '0':
                                break

                            # Play a specific song with lyrics:
                            elif user_num_choice == '1':
                                user_song_num = input("Enter song number: ")
                                song_name = artist_top_songs_name_list[int(user_song_num)]
                                song_uri = artist_top_songs_uri_list[int(user_song_num)]
                                Lyrics_Player.get_lyrics(artist_name, song_name)
                                time.sleep(1)
                                play(song_uri, artist_name, song_name)
                            # Plat all artist's top tracks
                            elif user_num_choice == '2':
                                play(None, None, None,
                                     artist_top_songs_uri_list)  # Once I insert a list of uri's it play them all
                                # One by one. we can then use the next() previous and etc. functions.
                                time.sleep(0.5)
                                current_song_lyrics()
                                music_player_interface()

                            else:
                                print()
                                print("invalid number entered. Please try again")
                                print()

                else:
                    print()
                    print("invalid number entered. Please try again")
                    print()

        # Only lyrics:
        elif user_num_choice == '2':
            artist_name = input("Enter artist name: ")
            song_name = input("Enter song name: ")
            Lyrics_Player.get_lyrics(artist_name, song_name)

        # Playlists:
        elif user_num_choice == '3':
            playlists()
        # Top of user: Doesn't work well. User top-listened tracks are far from being accurate
        # elif user_num_choice == '4':
        #     user_top()

        elif user_num_choice == '4':
            try:
                current_song_lyrics()
            except:
                print("Error fetching the current song lyrics. Pleas make sure Spotify is open and "
                      "try again. ")
            else:
                pass

        # Invalid number:
        else:
            print()
            print("invalid number entered. Please try again")
            print()


def current_song_lyrics():
    song_name = spotify_object.current_user_playing_track()['item']['name']
    artist_name = spotify_object.current_user_playing_track()['item']['artists'][0]['name']
    print(f"Playing {song_name} by {artist_name}")
    # print(json.dumps(artist_name, sort_keys=True, indent=4))
    Lyrics_Player.get_lyrics(artist_name, song_name)


def music_player_interface():
    while True:
        print()
        print('1 - next track')
        print()
        print('2 - previous track')
        print()
        print('3 - pause track')
        print()
        print('4 - resume track')
        print()
        print('5 - Show current song lyrics')
        print()
        print('0 - exit')
        print()
        user_input = input("Enter your choice: ")
        print()
        if user_input == '0':
            spotify_object.pause_playback()
            break
        # Next track:
        elif user_input == '1':
            try:
                spotify_object.next_track()
                time.sleep(0.3)
                current_song_lyrics()
            except:
                print("Cant switch songs while in Pause")
        # Previous track:
        elif user_input == '2':
            try:
                spotify_object.previous_track()
                current_song_lyrics()
            except:
                print("Cant switch songs while in Pause")
        # Pause:
        elif user_input == '3':
            try:
                spotify_object.pause_playback()
            except:
                print("Cant pause while already in pause")
        # Resume:
        elif user_input == '4':
            try:
                spotify_object.start_playback()
                current_song_lyrics()
            except:
                print("Cant resume while already playing")
        # Current song lyrics
        elif user_input == '5':
            current_song_lyrics()
        else:
            print()
            print('Invalid choice number. Please try again')
            print()


if __name__ == '__main__':
    main()
