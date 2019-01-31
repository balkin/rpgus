class Location:
    def tick(self):
        pass

class Room:
    def tick(self):
        pass

class Mobile:
    def __init__(self, name = None):
        self.name = name

    def tick(self):
        pass

    def say(self, phrase):
        print("{} говорит: {}".format( self.name, phrase))

class Player(Mobile):
    def tick(self):
        pass

vasya = Player('Вася')
petya = Player("Петя")
vasya.say("Я вася")
petya.say("Я петя")
