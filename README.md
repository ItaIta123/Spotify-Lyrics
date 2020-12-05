# Spotify-Lyrics
A solution to Spotify's lack of Lyrics for its tracks. 


"""
A solution to the absence of good lyrics on Spotify's app/web (at the time of writing this 
program there was no adequate lyrics support on Spotify's app/web). 

How to run the program:

1. The first phase would be to create an "APP" on Spotify's Developers website:
 (https://developer.spotify.com/dashboard/applications) 

2. After creating the 'APP' go to EDIT SETTINGS and paste whatever link into the Redirect URI section.
 I've used https://www.google.com/

3. In the Spotify's developers website enable to following scopes: user-read-private , user-read-playback-state , user-modify-playback-state , playlist-read-private 
 , playlist-read-collaborative , and user-top-read user-read-recently-played.
 
4. Copy your client ID and secret ID into token variable in the code.

5. There are two ways to run the program:
  
    1. Through terminal: cd to the program file directiry and run: python3 Spotify_Lyrics.py 'your spotify user name' REMEMBER TO UNCOMMENT THE TERMINAL CODE BLOCK        IN THE CODE FILE. This will direct you to a website. Copy the url of this website and paste it in the terminal (the terminal will ask you for it), and you          are good to go.
    2. This is the default running method. Just run the code the paste the directed website's url into your IDE terminal. 
    

  
