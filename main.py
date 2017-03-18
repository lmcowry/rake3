import webapp2, jinja2, os, random
from google.appengine.ext import db
from models import AnswerObj, GuessObj


import logging

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
listOfGuesses = []


def aColorValidator(guess):
    approvedGuesses = ["b", "r", "g", "c", "m", "y"]

    if guess in approvedGuesses:
        return True
    else:
        return False


def correctAnswer(theGuess):
    theseMatchTheGuess = AnswerObj.all().filter("spot0", theGuess.spot0).filter("spot1", theGuess.spot1).filter("spot2", theGuess.spot2).filter("spot3", theGuess.spot3)
    # not quite sure what this returns.  hoping it's a list, and that if the list is empty, this'll be evaluated to False
    if theseMatchTheGuess.count() > 0:
        return True
    else:
        return False

def clueGiver(theGuess):
    # figure out black first
    makingThoseClues = []
    theseMatchSpot0 = AnswerObj.all().filter("spot0", theGuess.spot0).count()
    theseMatchSpot1 = AnswerObj.all().filter("spot1", theGuess.spot1).count()
    theseMatchSpot2 = AnswerObj.all().filter("spot2", theGuess.spot2).count()
    theseMatchSpot3 = AnswerObj.all().filter("spot3", theGuess.spot3).count()


    if theseMatchSpot0 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot0)
        makingThoseClues.append(sendThisString)

    if theseMatchSpot1 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot1)
        makingThoseClues.append(sendThisString)

    if theseMatchSpot2 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot2)
        makingThoseClues.append(sendThisString)

    if theseMatchSpot3 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot3)
        makingThoseClues.append(sendThisString)




    if theseMatchSpot0 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot0)
        theGuess.clue0 = sendThisString

    if theseMatchSpot1 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot1)
        theGuess.clue1 = sendThisString

    if theseMatchSpot2 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot2)
        theGuess.clue2 = sendThisString

    if theseMatchSpot3 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot3)
        theGuess.clue3 = sendThisString

    return makingThoseClues

class SuperHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class SpecialPageHandler(SuperHandler):
    def render_front(self):
        self.render("specialPage.html")

    def get(self):
        self.render_front()

    def post(self):
        hardCodedAnswer = AnswerObj(spot0="b", spot1="c", spot2="c", spot3="c")
        hardCodedAnswer.put()
        hardCodedAnswer2 = AnswerObj(spot0="b", spot1="c", spot2="c", spot3="b")
        hardCodedAnswer2.put()
        self.redirect("/")

class MainPageHandler(SuperHandler):

    def render_front(self, guessAt0="", guessAt1="", guessAt2="", guessAt3="", error=""):
        # need to check if this hasn't been run before.  if it hasn't then need to generate the answers
        # if len(listOfGuesses) == 0:
        #     hardCodedAnswer = AnswerObj(spot0="b", spot1="c", spot2="c", spot3="c")
        #     hardCodedAnswer.put()
        #     hardCodedAnswer2 = AnswerObj(spot0="b", spot1="c", spot2="c", spot3="b")
        #     hardCodedAnswer2.put()
        self.render("theModel.html", guessAt0=guessAt0, guessAt1=guessAt1, guessAt2=guessAt2, guessAt3=guessAt3, error=error, listOfGuesses=listOfGuesses)

    def get(self):
        self.render_front()

    def post(self):
        guessAt0 = self.request.get("guessAt0")
        guessAt1 = self.request.get("guessAt1")
        guessAt2 = self.request.get("guessAt2")
        guessAt3 = self.request.get("guessAt3")


        if aColorValidator(guessAt0) and aColorValidator(guessAt1) and aColorValidator(guessAt2) and aColorValidator(guessAt3):
            thisGuess = GuessObj(spot0=guessAt0, spot1=guessAt1, spot2=guessAt2, spot3=guessAt3)

            # so i don't need to thisGuess.put() because it doesn't really need to be in the database
            listOfGuesses.append(thisGuess)

            if correctAnswer(thisGuess):
                self.response.out.write("you've won")

            else:
                clueGiver(thisGuess)
                self.render_front()

        else:
            error = "Possible answers are r, g, b, c, m, y.  You fucked up"
            self.render_front(guessAt0, guessAt1, guessAt2, guessAt3, error)


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
    ('/special', SpecialPageHandler)

], debug=True)
