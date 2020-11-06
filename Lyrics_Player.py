import requests  # for the HTTP commands - get the source code from the web
import lxml  # makes it much easier to get HTML and XML data
from bs4 import BeautifulSoup  # connect to the web


def get_lyrics(artist_name=None, song_name=None):
    """
    :param artist_name: The artist name
    :param song_name: The song name (can include "(ft. )")
    :return: Lyrics
    """
    if (artist_name is None) or (song_name is None):  # Makes sure the user inputs the artist name and the song name.
        print()
        print("Please make sure you have entered the artist name and the song name to the get_lyrics function")
        print()
    else:
        if '(' in song_name:  # In a case that the song name input has (ft. Drake) in it for example.
            letter_before_parentheses_index = (song_name.index('(') - 1)
            song_name = song_name[
                        :letter_before_parentheses_index]  # Takes only the song name (without the "(ft. Drake)")

        url_song_name = f'{artist_name} {song_name}'.replace(" ", "-")  # Making the url from the artist&song names
        url = f'https://genius.com/{url_song_name}-lyrics'  # Turns the artist name and the song name to the typical
        # Genius page url
        print()
        print("Just a few seconds please...")
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        lyrics_page_section = soup.find("div", class_="lyrics")
        i = 0
        number_of_tries_to_get_the_lyrics = 20
        while lyrics_page_section is None:
            # Often 'soup.find' doesn't work well (Beautiful instability) and
            # lyrics_page_section is getting the value None. So the while loop is running until lyrics_page_section is
            # not None (with a limit set above)
            source = requests.get(url).text
            soup = BeautifulSoup(source, 'lxml')
            lyrics_page_section = soup.find("div", class_="lyrics")
            i += 1
            if i == number_of_tries_to_get_the_lyrics:
                print(f'Tried {i} times')
                print()
                print("Error finding the lyrics")
                print('Please make sure the there are no typos and try again')
                # breaks if lyrics_page_section is NOT None or i reached its limit. The first of the two.
                break
        try:
            lyrics = lyrics_page_section.p.text
        except AttributeError:
            pass
        else:
            print("All the lyrics rights reserved to https://genius.com/")
            print(f'{song_name} by {artist_name} lyrics:')
            print()
            print(lyrics)


def main():
    get_lyrics('50 Cent', 'Just A Lil Bit')



# get_songs_list_lyrics(['https://genius.com/Eminem-rap-god-lyrics', 'https://genius.com/The-scotts-the-scotts-lyrics',
# 'https://genius.com/Drake-gods-plan-lyrics',
# 'https://genius.com/Lil-uzi-vert-xo-tour-llif3-lyrics',
# 'https://genius.com/Idina-menzel-let-it-go-lyrics'])

# -------------------------------------------------------------------------------------------------------|
# Some Basic Explanation:                                                                                |
# source = requests.get().text  # get the source code of the website as text                             |
# # print(source) = prints the exact HTML as it seems on the web (with inspect) .                        |
# soup = BeautifulSoup(source, 'lxml')  # Turn the website's HTML source code to more convenient,        |
# readable HTML text.                                                                                    |
# # print(soup.prettify())  # prettify makes the HTML text more structured.                              |
# -------------------------------------------------------------------------------------------------------|

# -------------------------------------------------------------------------------------------------------|
# The First Working Sequence Of Actions To Make It Work:                                                 |
# source = requests.get('https://genius.com/Lil-uzi-vert-xo-tour-llif3-lyrics').text                     |
# soup = BeautifulSoup(source, 'lxml')                                                                   |
# lyrics_page_section = soup.find("div", class_="lyrics")                                                |
# print()                                                                                                |
# lyrics = lyrics_page_section.p.text                                                                    |
# print(lyrics)                                                                                          |
# -------------------------------------------------------------------------------------------------------|


if __name__ == '__main__':
    main()
