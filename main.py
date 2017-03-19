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

def colorCodeSearcher(color):
    # this will count all total rs in the database, not just each code with a r in the database
    totalCount = 0
    totalCount += AnswerObj.all().filter("spot0", color).count()
    totalCount += AnswerObj.all().filter("spot1", color).count()
    totalCount += AnswerObj.all().filter("spot2", color).count()
    totalCount += AnswerObj.all().filter("spot3", color).count()
    return totalCount

    # a failed attempt, two to be exact, but valiant nonetheless.  and definitely not elegant
    #
    # if color == "r":
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot0 =', 'r').count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot1 =', 'r').count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot2 =', 'r').count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot3 =', 'r').count()
    #     return totalCount
    #
    # elif color == "g":
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot0 =', "g").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot1 =', "g").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot2 =', "g").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot3 =', "g").count()
    #     return totalCount
    # elif color == "b":
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot0 =', "b").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot1 =', "b").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot2 =', "b").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot3 =', "b").count()
    #     return totalCount
    # elif color == "c":
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot0 =', "c").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot1 =', "c").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot2 =', "c").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot3 =', "c").count()
    #     return totalCount
    # elif color == "y":
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot0 =', "y").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot1 =', "y").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot2 =', "y").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot3 =', "y").count()
    #     return totalCount
    # elif color == "m":
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot0 =', "m").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot1 =', "m").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot2 =', "m").count()
    #     totalCount += AnswerObj.all().filter('AnswerObj.spot3 =', "m").count()
    #     return totalCount


    # a valiant effort
    # if color == "r":
    #     return AnswerObj.all().filter('AnswerObj.countCode <', 10).count()
    # elif color == "g":
    #     return AnswerObj.all().filter('AnswerObj.countCode >', 10).filter('AnswerObj.countCode <', 100).count()
    # elif color == "b":
    #     return AnswerObj.all().filter('AnswerObj.countCode >', 100).filter('AnswerObj.countCode <', 1000).count()
    # elif color == "c":
    #     return AnswerObj.all().filter('AnswerObj.countCode >', 1000).filter('AnswerObj.countCode <', 10000).count()
    # elif color == "y":
    #     return AnswerObj.all().filter('AnswerObj.countCode >', 10000).filter('AnswerObj.countCode <', 100000).count()
    # elif color == "m":
    #     return AnswerObj.all().filter('AnswerObj.countCode >', 100000).count()

def colorCodeCount(theListOfAnswerPegs):
    totalCount = 0
    for answerPeg in theListOfAnswerPegs:
        if answerPeg == "r":
            totalCount += 1
        elif answerPeg == "g":
            totalCount += 10
        elif answerPeg == "b":
            totalCount += 100
        elif answerPeg == "c":
            totalCount += 1000
        elif answerPeg == "y":
            totalCount += 10000
        elif answerPeg == "m":
            totalCount += 100000
    return totalCount


def correctAnswer(theGuess):
    theseMatchTheGuess = AnswerObj.all().filter("spot0", theGuess.spot0).filter("spot1", theGuess.spot1).filter("spot2", theGuess.spot2).filter("spot3", theGuess.spot3)
    # not quite sure what this returns.  hoping it's a list, and that if the list is empty, this'll be evaluated to False
    if theseMatchTheGuess.count() > 0:
        return True
    else:
        return False

def clueGiver(theGuess):
    # figure out black first
    # this will always print whites, even if 0

    theseMatchSpot0 = AnswerObj.all().filter("spot0", theGuess.spot0).count()
    theseMatchSpot1 = AnswerObj.all().filter("spot1", theGuess.spot1).count()
    theseMatchSpot2 = AnswerObj.all().filter("spot2", theGuess.spot2).count()
    theseMatchSpot3 = AnswerObj.all().filter("spot3", theGuess.spot3).count()

    if theseMatchSpot0 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot0)
        theGuess.clue0 = sendThisString
    else:
        howMany = colorCodeSearcher("c")
        sendThisString = "{0} White".format(colorCodeSearcher(theGuess.spot0))
        theGuess.clue0 = sendThisString

    if theseMatchSpot1 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot1)
        theGuess.clue1 = sendThisString
    else:
        sendThisString = "{0} White".format(colorCodeSearcher(theGuess.spot1))
        theGuess.clue1 = sendThisString

    if theseMatchSpot2 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot2)
        theGuess.clue2 = sendThisString
    else:
        sendThisString = "{0} White".format(colorCodeSearcher(theGuess.spot2))
        theGuess.clue2 = sendThisString

    if theseMatchSpot3 > 0:
        sendThisString = "{0} Black".format(theseMatchSpot3)
        theGuess.clue3 = sendThisString
    else:
        sendThisString = "{0} White".format(colorCodeSearcher(theGuess.spot3))
        theGuess.clue3 = sendThisString

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
        theListOfAnswerPegs = ["r", "c", "c", "c"]
        totalCount = colorCodeCount(theListOfAnswerPegs)

        hardCodedAnswer = AnswerObj(spot0="r", spot1="c", spot2="c", spot3="c", countCode=totalCount)
        hardCodedAnswer.put()

        anotherListOfAnswerPegs = ["r", "c", "c", "b"]
        anotherTotalCount = colorCodeCount(anotherListOfAnswerPegs)
        hardCodedAnswer2 = AnswerObj(spot0="r", spot1="c", spot2="c", spot3="b", countCode=anotherTotalCount)
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
