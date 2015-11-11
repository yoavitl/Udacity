import webbrowser


class Movie():
    # The intializing function, takes the main information about the movie
    def __init__(self, title, story, poster, actor, trailer_youtube_url):
        self.title = title
        self.poster_image_url = poster
        self.story_line = story
        self.main_actor = actor
        self.trailer_youtube_url = trailer_youtube_url

    # This function opens the trialer of the movie in a web browser
    def ShowTrailer(self):
        webbrowser.open(self.trailer_youtube_url)
