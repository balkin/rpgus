import time


class World:
    def __init__(self):
        self.ticked = {}
        self.locations = []
        self.last_tick = 0
        self.step = 0

    def wait_for_tick(self):
        while time.time_ns() < self.last_tick + 1000000000:
            pass

    def tick(self):
        self.step = self.step + 1
        self.ticked.clear()
        # import datetime
        # print("TICK!!!", datetime.datetime.now())
        self.last_tick = time.time_ns()
        for location in self.locations:
            location.tick()

    def can_tick(self, mobile):
        return not self.ticked.__contains__(mobile)

    def make_tick(self, mobile):
        if self.can_tick(mobile):
            mobile.tick()
            self.ticked[mobile] = True

    def replace_with_corpse(self, victim):
        corpse = FloorObject(name="Труп " + victim.name)
        room = victim.room
        room.mobiles.remove(self)
        room.floor.append(corpse)
        victim.emote("превращается в труп")

    def rotten(self, victim):
        victim.emote("превращается в пыль")
        victim.room.floor.remove(victim)
        pass


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
    def __init__(self, name='Комната'):
        self.north = None
        self.south = None
        self.west = None
        self.east = None
        self.mobiles = []
        self.floor = []
        self.name = name

    def tick(self):
        for mobile in self.mobiles:
            world.make_tick(mobile)

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


class FloorObject:
    def __init__(self, name="Объект на полу", rotting = False, rotDelta = 1, rotValue = 10, rotThreshold = 3, room=None):
        self.rotting = rotting
        self.rotDelta = rotDelta
        self.rotValue = rotValue
        self.rotThreshold = rotThreshold
        self.name = name
        self.room = room

    def tick(self):
        if self.rotting:
            self.rotValue = self.rotValue - self.rotDelta
            if self.rotValue % self.rotThreshold == 0:
                self.emote("тихонько гниёт")
            if self.rotValue == 0:
                world.rotten(self)

    def emote(self, emotion):
        print("{} {}".format(self.name, emotion))


class Mobile:
    def __init__(self, name=None, strength=1, health=10):
        self.name = name
        self.room = None
        self.strength = strength
        self.health = health
        self.fighting = None

    def tick(self):
        if not self.alive():
            world.replace_with_corpse(self)
            return
        if self.fighting:
            self.maybe_update_fighting()

    def say(self, phrase):
        print("{} говорит: {}".format(self.name, phrase))

    def attack(self, victim):
        print("{} нападает на {}".format(self.name, victim.name))
        self.fighting = victim
        victim.fighting = self

    def emote(self, emotion):
        print("{} {}".format(self.name, emotion))

    def north(self):
        if self.room.north is None or self.cannot_move():
            print("{} не может идти на север".format(self.name))
            return

        old = self.room
        self.room = self.room.north
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на север в комнату {}".format(self.name, self.room.name))

    def west(self):
        if self.room.west is None or self.cannot_move():
            print("{} не может идти на запад".format(self.name))
            return

        old = self.room
        self.room = self.room.west
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на запад в комнату {}".format(self.name, self.room.name))

    def east(self):
        if self.room.east is None or self.cannot_move():
            print("{} не может идти на восток".format(self.name))
            return

        old = self.room
        self.room = self.room.east
        old.mobiles.remove(self)
        self.room.mobiles.append(self)
        print("{} двигается на восток в комнату {}".format(self.name, self.room.name))

    def south(self):
        if self.room.south is None or self.cannot_move():
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
            if self.room.north:
                self.north()
            pass
        elif i == 2:
            if self.room.west:
                self.west()
            pass
        elif i == 3:
            if self.room.east:
                self.east()
            pass
        elif i == 4:
            if self.room.south:
                self.south()
            pass

    def cannot_move(self):
        if self.fighting:
            return self.fighting.room == self.room

    def alive(self):
        return self.health > 0

    def maybe_update_fighting(self):
        self.deal_damage(self.fighting)
        if not self.fighting.alive():
            self.fighting.fighting = None
            self.fighting = None
            self.emote("завершил бой")

    def deal_damage(self, fighting):
        damage = self.strength
        self.emote("наносит " + str(damage) + " единиц урона " + fighting.name)
        fighting.health = fighting.health - damage


class Player(Mobile):
    def tick(self):
        super().tick()
        if not self.alive():
            return
        old_room = self.room
        self.random_movement()
        if old_room != self.room:
            for mob in self.room.mobiles:
                if mob != self and mob.__class__ == Player:
                    if self.health >= mob.health:
                        self.emote("злобно ухмыляется в сторону " + mob.name)
                        self.attack(mob)
                    else:
                        self.emote("с завистью смотрит в сторону " + mob.name)


vasya = Player('Вася', strength=2, health=20)
petya = Player("Петя", strength=1, health=40)

world = World()
gus_city = GusGrad()
world.locations.append(gus_city)
gus_city.generate_rooms()
gus_city_main = gus_city.rooms[0]
gus_city_main.enter(vasya)
gus_city_main.enter(petya)

while world.step < 100:
    world.wait_for_tick()
    world.tick()
