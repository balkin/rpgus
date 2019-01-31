class World:
    def __init__(self):
        self.locations = []

    def tick(self):
        for location in self.locations:
            location.tick()

class Location:
    def __init__(self):
        self.rooms = []

    def tick(self):
        for room in self.rooms:
            room.tick()

class Room:
    def __init__(self):
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.mobiles = []

    def tick(self):
        for mobile in self.mobiles:
            mobile.tick()

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
