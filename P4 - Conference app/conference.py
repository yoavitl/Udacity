from datetime import datetime

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from models import ConflictException
from models import Profile
from models import ProfileMiniForm
from models import ProfileForm
from models import StringMessage
from models import BooleanMessage
from models import Conference
from models import ConferenceForm
from models import ConferenceForms
from models import ConferenceQueryForm
from models import ConferenceQueryForms
from models import TeeShirtSize
from models import Session
from models import SessionForm
from models import SessionForms
from models import Speaker
from models import SpeakerForm
from models import SpeakerForms

from settings import WEB_CLIENT_ID
from settings import ANDROID_AUDIENCE

from utils import getUserId

EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
MEMCACHE_ANNOUNCEMENTS_KEY = "RECENT_ANNOUNCEMENTS"
ANNOUNCEMENT_TPL = ('Last chance to attend! The following conferences '
                    'are nearly sold out: %s')
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DEFAULTS = {
    "city": "Default City",
    "maxAttendees": 0,
    "seatsAvailable": 0,
    "topics": ["Default", "Topic"],
}

OPERATORS = {
            'EQ':   '=',
            'GT':   '>',
            'GTEQ': '>=',
            'LT':   '<',
            'LTEQ': '<=',
            'NE':   '!='
            }

FIELDS = {
            'CITY': 'city',
            'TOPIC': 'topics',
            'MONTH': 'month',
            'MAX_ATTENDEES': 'maxAttendees',
            }

DEFAULTSession = {
    "duration": 0.45,
    "typeofs": "Keynote",
    "startTime": 11.11,
    "highlights": ["Motivation", "Programming"],
    }
 
DEFAULTSPEAKER = {
    "expertise": ["Jack of Trades","Master of None"],
    "lecturs": ["The Importance of Python"],
    "age": 42.0,
    "city": "Tel-Aviv",
    }

CONF_GET_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeConferenceKey=messages.StringField(1),
)

CONF_POST_REQUEST = endpoints.ResourceContainer(
    ConferenceForm,
    websafeConferenceKey=messages.StringField(1),
)

SESSION_GET_REQUEST = endpoints.ResourceContainer(
    SessionForm,
    websafeConferenceKey=messages.StringField(1),
    websafeSpeakerKey=messages.StringField(2),
)

SESSION_BY_TYPE = endpoints.ResourceContainer(
    SessionForm,
    websafeConferenceKey=messages.StringField(1),
    typeofs=messages.StringField(2),
)

SESSION_BY_SPEAKER = endpoints.ResourceContainer(
    SessionForm,
    websafeSpeakerKey=messages.StringField(1),
)

SESSION_ADD_TO_WISHLIST = endpoints.ResourceContainer(
    websafeSessionKey=messages.StringField(1),
)

SESSION_REMOVE_WISHLIST = endpoints.ResourceContainer(
    websafeSessionKey=messages.StringField(1),
)

HIGHLIGHT_SESSION = endpoints.ResourceContainer(
    message_types.VoidMessage,
    highlight=messages.StringField(1),
)

LONG_SESSION = endpoints.ResourceContainer(
    message_types.VoidMessage,
    duration=messages.FloatField(1),
)

SPEAKER_GET_REQUEST = endpoints.ResourceContainer(
    SpeakerForm,
)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


@endpoints.api(name='conference', version='v2', audiences=[ANDROID_AUDIENCE],
               allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID],
               scopes=[EMAIL_SCOPE])
class ConferenceApi(remote.Service):
    """Conference API v2.1"""

# - - - Conference objects - - - - - - - - - - - - - - - - -

    def _copyConferenceToForm(self, conf, displayName):
        """Copy relevant fields from Conference to ConferenceForm."""
        cf = ConferenceForm()
        for field in cf.all_fields():
            if hasattr(conf, field.name):
                # convert Date to date string; just copy others
                if field.name.endswith('Date'):
                    setattr(cf, field.name, str(getattr(conf, field.name)))
                else:
                    setattr(cf, field.name, getattr(conf, field.name))
            elif field.name == "websafeKey":
                setattr(cf, field.name, conf.key.urlsafe())
        if displayName:
            setattr(cf, 'organizerDisplayName', displayName)
        cf.check_initialized()
        return cf

    def _createConferenceObject(self, request):
        """Create or update Conference object, returning ConferenceForm."""
        # preload necessary data items
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)

        if not request.name:
            raise endpoints.BadRequestException("Conference 'name' field required")  # noqa

        # copy ConferenceForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}   # noqa
        del data['websafeKey']
        del data['organizerDisplayName']

        # add default values for those missing (both data model & outbound Message)  # noqa
        for df in DEFAULTS:
            if data[df] in (None, []):
                data[df] = DEFAULTS[df]
                setattr(request, df, DEFAULTS[df])

        # convert dates from strings to Date objects; set month based on start_date  # noqa
        if data['startDate']:
            data['startDate'] = datetime.strptime(data['startDate'][:10], "%Y-%m-%d").date()  # noqa
            data['month'] = data['startDate'].month
        else:
            data['month'] = 0
        if data['endDate']:
            data['endDate'] = datetime.strptime(data['endDate'][:10], "%Y-%m-%d").date()  # noqa

        # set seatsAvailable to be same as maxAttendees on creation
        if data["maxAttendees"] > 0:
            data["seatsAvailable"] = data["maxAttendees"]
        # generate Profile Key based on user ID and Conference
        # ID based on Profile key get Conference key from ID
        p_key = ndb.Key(Profile, user_id)
        c_id = Conference.allocate_ids(size=1, parent=p_key)[0]
        c_key = ndb.Key(Conference, c_id, parent=p_key)
        data['key'] = c_key
        data['organizerUserId'] = request.organizerUserId = user_id

        # create Conference, send email to organizer confirming
        # creation of Conference & return (modified) ConferenceForm
        Conference(**data).put()
        taskqueue.add(params={'email': user.email(),
                      'conferenceInfo': repr(request)},
                      url='/tasks/send_confirmation_email')
        return request

    @ndb.transactional()
    def _updateConferenceObject(self, request):
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)

        # copy ConferenceForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}   # noqa

        # update existing conference
        conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()
        # check that conference exists
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s' % request.websafeConferenceKey)  # noqa

        # check that user is owner
        if user_id != conf.organizerUserId:
            raise endpoints.ForbiddenException(
                'Only the owner can update the conference.')

        # Not getting all the fields, so don't create a new object; just
        # copy relevant fields from ConferenceForm to Conference object
        for field in request.all_fields():
            data = getattr(request, field.name)
            # only copy fields where we get data
            if data not in (None, []):
                # special handling for dates (convert string to Date)
                if field.name in ('startDate', 'endDate'):
                    data = datetime.strptime(data, "%Y-%m-%d").date()
                    if field.name == 'startDate':
                        conf.month = data.month
                # write to Conference object
                setattr(conf, field.name, data)
        conf.put()
        prof = ndb.Key(Profile, user_id).get()
        return self._copyConferenceToForm(conf, getattr(prof, 'displayName'))

    @endpoints.method(ConferenceForm, ConferenceForm, path='conference',
                      http_method='POST', name='createConference')
    def createConference(self, request):
        """Create new conference."""
        return self._createConferenceObject(request)

    @endpoints.method(CONF_POST_REQUEST, ConferenceForm,
                      path='conference/{websafeConferenceKey}',
                      http_method='PUT', name='updateConference')
    def updateConference(self, request):
        """Update conference w/provided fields & return w/updated info."""
        return self._updateConferenceObject(request)

    @endpoints.method(CONF_GET_REQUEST, ConferenceForm,
                      path='conference/{websafeConferenceKey}',
                      http_method='GET', name='getConference')
    def getConference(self, request):
        """Return requested conference (by websafeConferenceKey)."""
        # get Conference object from request; bail if not found
        conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s' % request.websafeConferenceKey)   # noqa
        prof = conf.key.parent().get()
        # return ConferenceForm
        return self._copyConferenceToForm(conf, getattr(prof, 'displayName'))

    @endpoints.method(message_types.VoidMessage, ConferenceForms,
                      path='getConferencesCreated',
                      http_method='POST', name='getConferencesCreated')
    def getConferencesCreated(self, request):
        """Return conferences created by user."""
        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)

        # create ancestor query for all key matches for this user
        confs = Conference.query(ancestor=ndb.Key(Profile, user_id))
        prof = ndb.Key(Profile, user_id).get()
        # return set of ConferenceForm objects per Conference
        return ConferenceForms(items=[self._copyConferenceToForm(conf,
                                      getattr(prof, 'displayName'))
                                      for conf in confs])

    def _getQuery(self, request):
        """Return formatted query from the submitted filters."""
        q = Conference.query()
        inequality_filter, filters = self._formatFilters(request.filters)

        # If exists, sort on inequality filter first
        if not inequality_filter:
            q = q.order(Conference.name)
        else:
            q = q.order(ndb.GenericProperty(inequality_filter))
            q = q.order(Conference.name)

        for filtr in filters:
            if filtr["field"] in ["month", "maxAttendees"]:
                filtr["value"] = int(filtr["value"])
            formatted_query = ndb.query.FilterNode(filtr["field"],
                                                   filtr["operator"],
                                                   filtr["value"])
            q = q.filter(formatted_query)
        return q

    def _formatFilters(self, filters):
        """Parse, check validity and format user supplied filters."""
        formatted_filters = []
        inequality_field = None

        for f in filters:
            filtr = {field.name: getattr(f, field.name)
                     for field in f.all_fields()}

            try:
                filtr["field"] = FIELDS[filtr["field"]]
                filtr["operator"] = OPERATORS[filtr["operator"]]
            except KeyError:
                raise endpoints.BadRequestException("Filter contains invalid field or operator.")   # noqa

            # Every operation except "=" is an inequality
            if filtr["operator"] != "=":
                # check if inequality operation has been used in previous filters   # noqa
                # disallow the filter if inequality was performed on a different field before   # noqa
                # track the field on whch the inequality operation is performed
                if inequality_field and inequality_field != filtr["field"]:
                    raise endpoints.BadRequestException("Inequality filter is allowed on only one field.")  # noqa
                else:
                    inequality_field = filtr["field"]

            formatted_filters.append(filtr)
        return (inequality_field, formatted_filters)

    @endpoints.method(ConferenceQueryForms, ConferenceForms,
                      path='queryConferences',
                      http_method='POST',
                      name='queryConferences')
    def queryConferences(self, request):
        """Query for conferences."""
        conferences = self._getQuery(request)

        # need to fetch organiser displayName from profiles
        # get all keys and use get_multi for speed
        organisers = [(ndb.Key(Profile, conf.organizerUserId)) for conf in conferences]    # noqa
        profiles = ndb.get_multi(organisers)

        # put display names in a dict for easier fetching
        names = {}
        for profile in profiles:
            names[profile.key.id()] = profile.displayName

        # return individual ConferenceForm object per Conference
        return ConferenceForms(
                items=[self._copyConferenceToForm(conf, names[conf.organizerUserId]) for conf in    # noqa
                conferences]
        )


# - - - Profile objects - - - - - - - - - - - - - - - - - - -

    def _copyProfileToForm(self, prof):
        """Copy relevant fields from Profile to ProfileForm."""
        # copy relevant fields from Profile to ProfileForm
        pf = ProfileForm()
        for field in pf.all_fields():
            if hasattr(prof, field.name):
                # convert t-shirt string to Enum; just copy others
                if field.name == 'teeShirtSize':
                    setattr(pf, field.name, getattr(TeeShirtSize, getattr(prof, field.name)))    # noqa
                else:
                    setattr(pf, field.name, getattr(prof, field.name))
        pf.check_initialized()
        return pf

    def _getProfileFromUser(self):
        """Return user Profile from datastore, creating new one if non-existent."""    # noqa
        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        # get Profile from datastore
        user_id = getUserId(user)
        p_key = ndb.Key(Profile, user_id)
        profile = p_key.get()
        # create new Profile if not there
        if not profile:
            profile = Profile(
                key=p_key,
                displayName=user.nickname(),
                mainEmail=user.email(),
                teeShirtSize=str(TeeShirtSize.NOT_SPECIFIED),
            )
            profile.put()

        return profile      # return Profile

    def _doProfile(self, save_request=None):
        """Get user Profile and return to user, possibly updating it first."""
        # get user Profile
        prof = self._getProfileFromUser()

        # if saveProfile(), process user-modifyable fields
        if save_request:
            for field in ('displayName', 'teeShirtSize'):
                if hasattr(save_request, field):
                    val = getattr(save_request, field)
                    if val:
                        setattr(prof, field, str(val))
                        prof.put()

        # return ProfileForm
        return self._copyProfileToForm(prof)

    @endpoints.method(message_types.VoidMessage, ProfileForm,
                      path='profile', http_method='GET', name='getProfile')
    def getProfile(self, request):
        """Return user profile."""
        return self._doProfile()

    @endpoints.method(ProfileMiniForm, ProfileForm,
                      path='profile', http_method='POST', name='saveProfile')
    def saveProfile(self, request):
        """Update & return user profile."""
        return self._doProfile(request)


# - - - Announcements - - - - - - - - - - - - - - - - - - - -

    @staticmethod
    def _cacheAnnouncement():
        """Create Announcement & assign to memcache; used by
        memcache cron job & putAnnouncement().
        """
        confs = Conference.query(ndb.AND(
            Conference.seatsAvailable <= 5,
            Conference.seatsAvailable > 0)
        ).fetch(projection=[Conference.name])

        if confs:
            # If there are almost sold out conferences,
            # format announcement and set it in memcache
            announcement = ANNOUNCEMENT_TPL % (
                ', '.join(conf.name for conf in confs))
            memcache.set(MEMCACHE_ANNOUNCEMENTS_KEY, announcement)
        else:
            # If there are no sold out conferences,
            # delete the memcache announcements entry
            announcement = ""
            memcache.delete(MEMCACHE_ANNOUNCEMENTS_KEY)

        return announcement

    @endpoints.method(message_types.VoidMessage, StringMessage,
                      path='conference/announcement/get',
                      http_method='GET', name='getAnnouncement')
    def getAnnouncement(self, request):
        """Return Announcement from memcache."""
        return StringMessage(data=memcache.get(MEMCACHE_ANNOUNCEMENTS_KEY) or "")   # noqa

# - - - Registration - - - - - - - - - - - - - - - - - - - -

    @ndb.transactional(xg=True)
    def _conferenceRegistration(self, request, reg=True):
        """Register or unregister user for selected conference."""
        retval = None
        prof = self._getProfileFromUser()  # get user Profile

        # check if conf exists given websafeConfKey
        # get conference; check that it exists
        wsck = request.websafeConferenceKey
        conf = ndb.Key(urlsafe=wsck).get()
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s' % wsck)

        # register
        if reg:
            # check if user already registered otherwise add
            if wsck in prof.conferenceKeysToAttend:
                raise ConflictException(
                    "You have already registered for this conference")

            # check if seats avail
            if conf.seatsAvailable <= 0:
                raise ConflictException(
                    "There are no seats available.")

            # register user, take away one seat
            prof.conferenceKeysToAttend.append(wsck)
            conf.seatsAvailable -= 1
            retval = True

        # unregister
        else:
            # check if user already registered
            if wsck in prof.conferenceKeysToAttend:

                # unregister user, add back one seat
                prof.conferenceKeysToAttend.remove(wsck)
                conf.seatsAvailable += 1
                retval = True
            else:
                retval = False

        # write things back to the datastore & return
        prof.put()
        conf.put()
        return BooleanMessage(data=retval)

    @endpoints.method(message_types.VoidMessage, ConferenceForms,
                      path='conferences/attending',
                      http_method='GET', name='getConferencesToAttend')
    def getConferencesToAttend(self, request):
        """Get list of conferences that user has registered for."""
        prof = self._getProfileFromUser()  # get user Profile
        conf_keys = [ndb.Key(urlsafe=wsck) for wsck in prof.conferenceKeysToAttend]   # noqa
        conferences = ndb.get_multi(conf_keys)

        # get organizers
        organisers = [ndb.Key(Profile, conf.organizerUserId) for conf in conferences]   # noqa
        profiles = ndb.get_multi(organisers)

        # put display names in a dict for easier fetching
        names = {}
        for profile in profiles:
            names[profile.key.id()] = profile.displayName

        # return set of ConferenceForm objects per Conference
        return ConferenceForms(items=[self._copyConferenceToForm(conf, names[conf.organizerUserId])    # noqa
        for conf in conferences])

    @endpoints.method(CONF_GET_REQUEST, BooleanMessage,
                      path='conference/{websafeConferenceKey}',
                      http_method='POST', name='registerForConference')
    def registerForConference(self, request):
        """Register user for selected conference."""
        return self._conferenceRegistration(request)

    @endpoints.method(CONF_GET_REQUEST, BooleanMessage,
                      path='conference/{websafeConferenceKey}',
                      http_method='DELETE', name='unregisterFromConference')
    def unregisterFromConference(self, request):
        """Unregister user for selected conference."""
        return self._conferenceRegistration(request, reg=False)

    @endpoints.method(message_types.VoidMessage, ConferenceForms,
                      path='filterPlayground',
                      http_method='GET', name='filterPlayground')
    def filterPlayground(self, request):
        """Filter Playground"""
        q = Conference.query()
        q = q.filter(Conference.city == "London")
        q = q.filter(Conference.topics == "Medical Innovations")
        q = q.filter(Conference.month == 6)

        return ConferenceForms(items=[self._copyConferenceToForm(conf, "")
                               for conf in q])

#  Project 4 udacity
    # Part 1- add Sessions and sort by sessions

    def _copySessionToForm(self, session):
        """Copy relevant fields from Session to SessionForm."""
        sf = SessionForm()
        for field in sf.all_fields():
            if hasattr(session, field.name):
                # convert Date to date string; just copy others
                if field.name.endswith('date'):
                    setattr(sf, field.name, str(getattr(session, field.name)))
                else:
                    setattr(sf, field.name, getattr(session, field.name))
            elif field.name == "websafeSessionKey":
                setattr(sf, field.name, session.key.urlsafe())
        sf.check_initialized()
        return sf

    def _copySpeakerToForm(self, speaker):
        """Copy relevant fields from Speaker to SpeakerForm."""
        speakerf = SpeakerForm()
        for field in speakerf.all_fields():
            if hasattr(speaker, field.name):
                setattr(speakerf, field.name, getattr(speaker, field.name))
            elif field.name == "websafeSpeakerKey":
                setattr(speakerf, field.name, speaker.key.urlsafe())
        speakerf.check_initialized()
        return speakerf

    @endpoints.method(CONF_GET_REQUEST, SessionForms,
                      path='conference/sessions/{websafeConferenceKey}',
                      http_method='GET', name='getConferenceSessions')
    def getConferenceSessions(self, request):
        """Given a conference, return all sessions"""
        sessions = Session.query()
        sessions = sessions.filter(Session.webSafeConfId == request.websafeConferenceKey)   # noqa

        # return set of SessionForm objects one per Session
        return SessionForms(items=[self._copySessionToForm(sn) for sn in sessions])   # noqa

    @endpoints.method(SESSION_GET_REQUEST, SessionForm,
                      path='session/{websafeConferenceKey}/{websafeSpeakerKey}',
                      http_method='POST', name='createSession')
    def createSession(self, request):
        """Create or update Session object"""
        if not request.name:
            raise endpoints.BadRequestException("Session 'name' field required")   # noqa

        # check for authorization, valid conference key
        # and that the current user is the conference orgainizer
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException("Authorization required")
        user_id = getUserId(user)
        try:
            conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()
        except TypeError:
            raise endpoints.BadRequestException("Only string is allowed as websafeConferenceKey input")  # noqa
        except Exception, e:
            if e.__class__.__name__ == 'ProtocolBufferDecodeError':
                raise endpoints.BadRequestException("The websafeConferenceKey string is invalid")  # noqa
            else:
                raise
        if not conf:
            raise endpoints.NotFoundException('No conference found with key: %s' % request.webSafeConfId)   # noqa
        if user_id != getattr(conf, 'organizerUserId'):
            raise endpoints.UnauthorizedException('Only conference organizer is authorized to add sessions.')   # noqa

        # check for valid speaker key 
        try:
            speak = ndb.Key(urlsafe=request.websafeSpeakerKey).get()
        except TypeError:
            raise endpoints.BadRequestException("Only string is allowed as websafeSpeakerKey input")  # noqa
        except Exception, e:
            if e.__class__.__name__ == 'ProtocolBufferDecodeError':
                raise endpoints.BadRequestException("The websafeSpeakerKey string is invalid")  # noqa
            else:
                raise
        if not speak:
            raise endpoints.NotFoundException('No speaker found with key: %s' % request.websafeSpeakerKey)   # noqa

        # copy SessionForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}   # noqa
        del data['websafeConferenceKey']
        del data['websafeSpeakerKey']

        # add default values for those missing (both data model & outbound Message)   # noqa
        for df in DEFAULTSession:
            if data[df] in (None, []):
                data[df] = DEFAULTSession[df]
                setattr(request, df, DEFAULTSession[df])

        # convert dates from strings to Date objects
        if data['date']:
            data['date'] = datetime.strptime(data['date'][:10], "%Y-%m-%d").date()   # noqa

        data['webSafeConfId'] = request.websafeConferenceKey
        del data['websafeSessionKey']

        data['speaker'] = request.websafeSpeakerKey
        # creation of Session, record the key to get the item & return (modified) SessionForm   # noqa
        sessionKey = Session(**data).put()
        # start the task to update the conference featured speaker if needed
        taskqueue.add(params={'websafeConferenceKey': request.websafeConferenceKey,    # noqa
                          'speaker': data['speaker']},
                          url='/tasks/set_featured_speaker')

        return self._copySessionToForm(sessionKey.get())

    @endpoints.method(SESSION_BY_TYPE, SessionForms,
                      path='conference/{websafeConferenceKey}/sessions/{typeofs}',    # noqa
                      http_method='GET', name='getSessionsByType')
    def getSessionsByType(self, request):
        """Given a conference, return all sessions of a specified
        type (eg lecture, keynote, workshop)"""
        sessions = Session.query()
        sessions = sessions.filter(Session.webSafeConfId == request.websafeConferenceKey)   # noqa
        sessions = sessions.filter(Session.typeofs == request.typeofs)

        # return set of SessionForm objects one per Session
        return SessionForms(items=[self._copySessionToForm(sn) for sn in sessions])    # noqa

    @endpoints.method(SESSION_BY_SPEAKER, SessionForms,
                      path='sessions/{websafeSpeakerKey}',
                      http_method='GET', name='getSessionsBySpeaker')
    def getSessionsBySpeaker(self, request):
        """Given a speaker, return all sessions given by this particular speaker,
        across all conferences"""
        sessions = Session.query()
        sessions = sessions.filter(Session.speaker == request.speaker)

        # return set of SessionForm objects one per Session
        return SessionForms(items=[self._copySessionToForm(sesn)
                            for sesn in sessions])
  
    @endpoints.method(SPEAKER_GET_REQUEST, SpeakerForm,
                      path='Speaker/createspeaker',
                      http_method='POST', name='createspeaker')
    def createspeaker(self, request):
        """Create a Speaker object"""
        if not request.name:
            raise endpoints.BadRequestException("Speaker must have a name")

        # check for authorization, valid conference key, and that the current user is the conference orgainizer   # noqa
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException("Authorization required")
        # copy SpeakerForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}   # noqa
        del data['websafeSpeakerKey']
     
        # add default values for those missing (both data model & outbound Message)   # noqa
        for df in DEFAULTSPEAKER:
            if data[df] in (None, []):
                data[df] = DEFAULTSPEAKER[df]
                setattr(request, df, DEFAULTSPEAKER[df])

        # creation of Session, record the key to get the item & return (modified) SessionForm   # noqa
        speakerKey = Speaker(**data).put()
        return self._copySpeakerToForm(speakerKey.get())

    @endpoints.method(SPEAKER_GET_REQUEST, SpeakerForms,
                      path='Speaker/showspeakers',
                      http_method='GET', name='ShowSpeakers')
    def getSpeakers(self, request):
        """Show all Availble speakers"""
        speakers = Speaker.query().fetch()

        # return set of SessionForm objects one per Session
        return SpeakerForms(items=[self._copySpeakerToForm(sp) for sp in speakers])   # noqa

    # Part 2- Add Wishlist

    @endpoints.method(SESSION_ADD_TO_WISHLIST, BooleanMessage,
                      path='conferences/sessions/addtowishlist/{websafeSessionKey}',
                      http_method='POST', name='addSessionToWishlist')
    def addSessionToWishlist(self, request):
        """Adds the session to the user's list of sessions
        they are interested in attending"""

        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        # Get user profile
        profile = self._getProfileFromUser()
        retval = True
        # Check if the user already have the session key in his wishlist
        if request.websafeSessionKey in profile.WishList:
            raise endpoints.BadRequestException("You have this Session in your Wishlist")  # noqa
            retval = False
        else:
            profile.WishList.append(request.websafeSessionKey)
        profile.put()
        return BooleanMessage(data=retval)

    @endpoints.method(message_types.VoidMessage, SessionForms,
                      path='conferences/sessions/wishlist',
                      http_method='GET', name='getSessionsInWishlist')
    def getSessionsInWishlist(self, request):
        """query for all the sessions in a conference that the user is interested in"""  # noqa
        prof = self._getProfileFromUser()  # get user Profile
        Session_keys = [ndb.Key(urlsafe=wsck) for wsck in prof.WishList]
        sessions = ndb.get_multi(Session_keys)

        # return set of ConferenceForm objects per Conference
        return SessionForms(items=[self._copySessionToForm(sesn)
                            for sesn in sessions])

    @endpoints.method(SESSION_REMOVE_WISHLIST, BooleanMessage,
                      path='conferences/sessions/deletewishlist/{websafeSessionKey}',
                      http_method='DELETE', name='deleteSessionInWishlist')
    def deleteSessionInWishlist(self, request):
        """removes a session from the users list of sessions they are interested"""

        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        # Get user profile
        profile = self._getProfileFromUser()
        sessions = Session.query()
        retval = None
        # Check if the user have the session key in his wishlist
        if request.websafeSessionKey in profile.WishList:
            profile.WishList.remove(request.websafeSessionKey)
            profile.put()
            retval = True
        else:
            raise endpoints.BadRequestException("You Don't have this Session in your Wishlist")  # noqa
            retval = False

        return BooleanMessage(data=retval)

    # Part 3 - Add Queries
    @endpoints.method(HIGHLIGHT_SESSION, SessionForms,
                      path='sessions/highlight/{highlight}',
                      http_method='GET', name='getSessionHighlight')
    def Sessionquery(self, request):
        """Query Sesssions by highlight"""
        sessions = Session.query()
        sessions = sessions.filter(Session.highlights == request.highlight)

        return SessionForms(
            items=[self._copySessionToForm(sesn) for sesn in sessions]
        )

    @endpoints.method(LONG_SESSION, SessionForms,
                      path='sessions/time/{duration}',
                      http_method='GET', name='getLongSessions')
    def getLongSessions(self, request):
        """Return all sessions longer then specific time"""
        sessions = Session.query()
        sessions = sessions.filter(Session.duration >= request.duration)

        # return set of SessionForm objects one per Session
        return SessionForms(items=[self._copySessionToForm(sesn) for sesn in sessions])  # noqa

    @endpoints.method(message_types.VoidMessage, SessionForms,
                      path='noworkshopnotlate',
                      http_method='GET', name='SessionQuestion')
    def SessionQuestion(self, request):
        """Query for all non-workshop sessions before 7 pm"""
        sessions = Session.query()
        sessions = sessions.filter(Session.typeofs != "workshop").fetch()
        SecondFilter = []
        for i in sessions:
            if i.startTime < 19.00:
                SecondFilter.append(i)
        return SessionForms(
            items=[self._copySessionToForm(sesn) for sesn in SecondFilter])

    # Part 4 - Memcache message
    @staticmethod
    def _cacheFeaturedSpeaker(wsck, speaker):
        """When adding a new session to a conference, determine whether or not the
           session's speaker should be the new featured speaker
        """
        sessions = Session.query()
        sessions = sessions.filter(Session.webSafeConfId == wsck)
        sessions = sessions.filter(Session.speaker == speaker)
        sessions = sessions.fetch()
        if(len(sessions) < 2):
            return
        announcement = "Featured speaker: %s, Sessions: " % speaker
        for session in sessions:
            announcement += "%s, " % session.name
        memcache.set(wsck, announcement[:-2])

    @endpoints.method(CONF_GET_REQUEST, StringMessage,
                      path='conference/{websafeConferenceKey}/featuredspeaker/get',   # noqa
                      http_method='GET', name='getFeaturedSpeaker')
    def getFeaturedSpeaker(self, request):
        """Return featured speaker for the conference from memcache
        (if there is one, '' if none)"""
        info = memcache.get(request.websafeConferenceKey)
        return StringMessage(data=info or '')

api = endpoints.api_server([ConferenceApi])  # register API
