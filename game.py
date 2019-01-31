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
        self.name = 'Комната'

    def tick(self):
        for mobile in self.mobiles:
            mobile.tick()


class Mobile:
    def __init__(self, name=None):
        self.name = name
        self.room = None

    def tick(self):
        pass

    def say(self, phrase):
        print("{} говорит: {}".format(self.name, phrase))

    def north(self):
        if self.room.north is None:
            print("{} не может идти на север".format(self.name))
            return

        old = self.room
        self.room = self.room.north
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на север в комнату {}", self.name, self.room.name)

    def west(self):
        if self.room.west is None:
            print("{} не может идти на запад".format(self.name))
            return

        old = self.room
        self.room = self.room.west
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на запад в комнату {}", self.name, self.room.name)

    def east(self):
        if self.room.east is None:
            print("{} не может идти на восток".format(self.name))
            return

        old = self.room
        self.room = self.room.east
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на восток в комнату {}", self.name, self.room.name)

    def south(self):
        if self.room.south is None:
            print("{} не может идти на юг".format(self.name))
            return

        old = self.room
        self.room = self.room.south
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на юг в комнату {}", self.name, self.room.name)


class Player(Mobile):
    def tick(self):
        pass


vasya = Player('Вася')
petya = Player("Петя")
vasya.say("Я вася")
petya.say("Я петя")
