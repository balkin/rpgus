class World:
    def __init__(self):
        self.locations = []

    def tick(self):
        print("TICK!!!")
        for location in self.locations:
            location.tick()


class Location:
    def __init__(self):
        self.rooms = []

    def generate_rooms(self):
        pass

    def tick(self):
        if len(self.rooms) == 0:
            self.generate_rooms()

        for room in self.rooms:
            room.tick()


class GusGrad(Location):

    def generate_rooms(self):
        super().generate_rooms()
        center = Room('Гусьград')
        left = Room('Левая комната')
        right = Room("Не левая комната")
        les = Room("Лес")
        ozero = Room("Озеро")
        center.link_west(left)
        center.link_east(right)
        left.link_north(les)
        left.link_south(ozero)
        self.rooms = [center, left, right, les, ozero]


class Room:
    def __init__(self, name = 'Комната'):
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.mobiles = []
        self.name = name

    def tick(self):
        for mobile in self.mobiles:
            mobile.tick()

    def enter(self, mobile):
        self.mobiles.append(mobile)
        mobile.room = self

    def link_west(self, another):
        another.east = self
        self.west = another

    def link_east(self, another):
        another.west = self
        self.east = another

    def link_north(self, another):
        another.south = self
        self.north = another

    def link_south(self, another):
        another.north = self
        self.south = another

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
        print("{} двигается на север в комнату {}".format(self.name, self.room.name))

    def west(self):
        if self.room.west is None:
            print("{} не может идти на запад".format(self.name))
            return

        old = self.room
        self.room = self.room.west
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на запад в комнату {}".format(self.name, self.room.name) )

    def east(self):
        if self.room.east is None:
            print("{} не может идти на восток".format(self.name))
            return

        old = self.room
        self.room = self.room.east
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на восток в комнату {}".format(self.name, self.room.name))

    def south(self):
        if self.room.south is None:
            print("{} не может идти на юг".format(self.name))
            return

        old = self.room
        self.room = self.room.south
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на юг в комнату {}".format(self.name, self.room.name))

    def random_movement(self):
        import random
        i = random.randint(1, 4)
        if i == 1:
            self.north()
            pass
        elif i == 2:
            self.west()
            pass
        elif i == 3:
            self.east()
            pass
        elif i == 4:
            self.south()
            pass

class Player(Mobile):
    def tick(self):
        self.random_movement()
        pass


vasya = Player('Вася')
petya = Player("Петя")

world = World()
gus_city = GusGrad()
world.locations.append(gus_city)
gus_city.generate_rooms()
gus_city_main = gus_city.rooms[0]
gus_city_main.enter(vasya)
gus_city_main.enter(petya)

step = 0
import time
last = time.time_ns()

while step < 100:
    while time.time_ns() < last + 1000000000:
        pass
    last = time.time_ns()
    step = step+1
    world.tick()
