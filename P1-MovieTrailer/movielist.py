import media
import fresh_tomatoes


# Creating a Class for each movie
Inception = media.Movie("Inception",
                        "Movie about dreams",
                        "Leonardo Dicaprio",
                        "http://goo.gl/RZnZ82",
                        "https://www.youtube.com/watch?v=66TuSJo4dZM")

Whiplash = media.Movie("Whiplash",
                       "The relationsip between a drummer and his proffesor",
                       "J.K Simmons",
                       "https://goo.gl/5zrejj",
                       "https://www.youtube.com/watch?v=7d_jQycdQGo")

SlumDog = media.Movie("Slum Dog Millionare",
                      "A story about a boy in India",
                      "Dev Patel",
                      "http://goo.gl/lb5JEH",
                      "https://www.youtube.com/watch?v=AIzbwV7on6Q")

YellowSubmarine = media.Movie("Yellow submarine",
                              "The Beatles Movie",
                              "Ringo Starr",
                              "http://goo.gl/WNt5Kb",
                              "https://www.youtube.com/watch?v=vefJAtG-ZKI")

TheMartian = media.Movie("The Martian",
                         "Saving Matt Damon",
                         "Matt Damon",
                         "http://goo.gl/R8jlwO",
                         "https://www.youtube.com/watch?v=Ue4PCI0NamI")

Interstellar = media.Movie("Interstellar",
                           "The earth is about to be uninhabitable",
                           "Matthew McConaughey",
                           "http://goo.gl/DOJ3o9",
                           "https://www.youtube.com/watch?v=zSWdZVtXT7E")

# The list of all the movies
mvs = [Inception, Whiplash, SlumDog, YellowSubmarine, TheMartian, Interstellar]

# The function the creats the webpage by using fresh tomatoes module
fresh_tomatoes.open_movies_page(mvs)
