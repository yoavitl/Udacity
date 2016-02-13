# Confrence App API Project *v2.0*
---------------------------

This App powered by the Google App Engine helps create confrences arounfd the world,
Register to them and even look in session that each confrence has to offer.

## Design Explanation
----------------------
I implemented the requirments of the session thinking that the Session is
a conference inside a conference.
the models i used are strings for the text fields like name, highlight and type of session.
I used "webSafeConfId" to link between the session to the conference, so each session
created must have an existing conference in order to regiser it in the database. 
I added also models and forms for the speaker and implemented them- you can create 
entity for speaker and show all of the speakers registered. I didn't made them required 
for the session because only importent speakers should have their identity.

### Task 1
##### Added functioncs
- `conference.getConferenceSessions()` - The user inputs a confrence webkey, and he gets all the sessions happening in the conference. 
- `conference.getSessionsByType()` - The user inputs a session type -lecture, keynote, workshop etc... and gets all of the session in this type 
- `conference.getSessionsBySpeaker()` - The user inputs a speaker name and he get all of the sessions in all of the conferences that this speaker participates in
- `conference.createSession()` - The user can create a session inside a conference
- `conference.createspeaker()` - The user can create entity for a speaker
- `conference.showSpeakers()` - Display the name of all the availble speakers 	
##### Added models 
- `Session` - create the database model of the session
- `SessionForm` - the response of creating a session
- `SessionForms` - model to gather all the sessions toghether
- `Speaker` - create the database model of a speaker
- `SpeakerForm` - the response of creating a speaker
- `SpeakerForms` - model to gather all the speakers toghether
### Task 2
##### Added functioncs
- `conference.addSessionToWishlist()` - Add a session by his webkey to a user whishlist    
- `conference.getSessionsInWishlist()` - Show all of the session in a user wishlist   
- `conference.deleteSessionInWishlist()`- Delete a session by his webkey from a user whishlist

### Task 3 
##### Added Queries 
-`conference.getSessionHighlight()` - Query all sesssions with a spefic highlight in them    
-`conference.getLongSessions()` - Query all the sessions longer then a given time

#### Problem 
>Let’s say that you don't like workshops and you don't like sessions after 7 pm. What is the problem for >implementing this query?   

The Problem with implementing this query is that inequality on multiple properties is not permitted, and in this situation we have two, one is not equal to workshop and the other is lower then the specific time

The solution I found was like this-
1- First select one of the inequalities, and make a query to get the results
2- Insert all the answers into a python array 
3- Make a loop to run through the new array and filter it by the second inequaltiy.
I implemented the solutin using the function `conference.sessionQuestion()`

### Task 4
##### Added Task
-`conference.getFeaturedSpeaker` - Return featured speaker for the conference from memcache

## Setup Instructions.
-----------------------
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
2. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console](https://console.developers.google.com/).
3. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
4. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
5. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080](https://localhost:8080).)
6. (Optional) Generate your client library(ies) with [the endpoints tool](https://localhost:8080/_ah/api/explorer).
7. Deploy your application.
8. To check my code api you can visit [Here](https://apis-explorer.appspot.com/apis-explorer/?base=https://udacityp4-1190.appspot.com/_ah/api#p/conference/v2/).




**Date**:       14.02.2016     
**Copyright**:  Yoavi   
**Auther**:     Yoav T. Levi
