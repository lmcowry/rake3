from google.appengine.ext import db

class AnswerObj(db.Model):


    spot0 = db.StringProperty(required = True)
    spot1 = db.StringProperty(required = True)
    spot2 = db.StringProperty(required = True)
    spot3 = db.StringProperty(required = True)

    countCode = db.IntegerProperty(required = True)




class GuessObj(db.Model):
    # will just be the guess.  will also have clues added later
    spot0 = db.StringProperty(required = True)
    spot1 = db.StringProperty(required = True)
    spot2 = db.StringProperty(required = True)
    spot3 = db.StringProperty(required = True)

    clue0 = db.StringProperty()
    clue1 = db.StringProperty()
    clue2 = db.StringProperty()
    clue3 = db.StringProperty()

    # title = db.StringProperty(required = True)
    # body = db.TextProperty(required = True)
    # created = db.DateTimeProperty(auto_now_add = True)
    # # TODO - we need an author field here; it should be required
    # author = db.ReferenceProperty(Answer, required = True)
