# Confrence App API Project *v2.0*
---------------------------

This App powered by the Google App Engine helps create confrences arounfd the world,
Register to them and even look in session that each confrence has to offer.

## Design Explanation
----------------------
I implemented the requrments of the session and the speaker just like the conference,
thinking that the Session is like a conference inside a conference. 
I added also models and forms for the speaker but I havn't made the option to added speakers. 
### Task 1
##### Added functioncs
- `conference.getConferenceSessions()` 
- `conference.getSessionsByType()`
- `conference.getSessionsBySpeaker()`
- `conference.createSession()`
##### Added models 
- `Session`
- `SessionForm`
- `SessionForms`
- `Speaker`
- `SpeakerForm`
### Task 2
##### Added functioncs
- `conference.addSessionToWishlist()`    
- `conference.getSessionsInWishlist()`   
- `conference.deleteSessionInWishlist()`
### Task 3 
##### Added Queries 
-`conference.sessionquery()` - Query all motivation sesssions    
-`conference.getLongSessions()` - Query all the sessions longer then a given time
#### Problem 
>Let’s say that you don't like workshops and you don't like sessions after 7 pm. What is the problem for >implementing this query?   

The Problem with implementing this query is that you cant have more then one inequality filter, and in this situation we have two, one is not equal to workshop and the other is lower then the specific time

The solution I found was to enter the result into a new array and then loop through it
I implemented the solutin using this function `conference.sessionQuestion()`

### Task 4
##### Added Task
-`conference.getFeaturedSpeaker`

## How to run the application.
---------------------------
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080].)
2. visit [Api Explorer](https://localhost:8080/_ah/api/explorer) to check the entire API's.
3. To check my code api you can visit [Here](https://apis-explorer.appspot.com/apis-explorer/?base=https://udacityp4-1190.appspot.com/_ah/api#p/conference/v2/).




**Date**:       07.02.2016     
**Copyright**:  Yoavi   
**Auther**:     Yoav T. Levi
