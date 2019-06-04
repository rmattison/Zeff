#MAKE SECRET NOTES SCATTERED AROUND
#MAKE A HIDDEN MAP SOMEWHERE
#MAKE A PUZZLE SOMEWHERE

import os
import random, string


class Item(object):

    def __init__(self, name, description, dam):
        self.name = name
        self.description = description
        self.dam = dam


class Enemy(object):

    def __init__(self, name, description, hp, dam):
        self.name = name
        self.description = description
        self.hp = hp
        self.dam = dam


class Player(object):

    def __init__(self, name, description, hp, dam):
        self.name = name
        self.description = description
        self.hp = hp
        self.dam = dam
        self.inventory = []
        self.best_weapon = None

    def battle(self, enemy):
        for i in self.inventory:
            if i.dam > self.dam:
                self.dam = i.dam
                self.best_weapon = i
        while enemy.hp > 0:
            self.hp -= enemy.dam
            enemy.hp -= self.dam
    

class Engine(object):

    def __init__(self, scenes):
        self.scenes = scenes

    def play(self):
        current_room = self.scenes['start_screen']
        last_room = self.scenes['last_screen']

        while current_room != last_room and Player.hp > 0:
            os.system('cls')
            current_room.enter()
            
            if current_room.enemy and current_room.enemy.hp > 0:
                print ("\n  A %s appears!" % current_room.enemy.name)
                print ("\n  You enter battle with the %s!" % current_room.enemy.name)

                Player.battle(current_room.enemy)

                if Player.hp > 0 and current_room.enemy.hp <= 0:
                    print ("\n You killed the %s with your %s!" % (current_room.enemy.name, Player.best_weapon.name))
                    print (" Your hp is now %s" % Player.hp)
                    print ("\n The %s dropped a %s." % (current_room.enemy.name, current_room.item.name))

                else:
                    print ("\nYou were killed.")
                    again = input("\n\n\nRetry? (y/n)")
                    if "y" in again:
                        Player.hp = 100
                        Player.inventory = []
                        word = ''.join(random.choice(string.lowercase) for i in range(3))
                        word = Engine(scenes)
                        word.play()
                    break

            if current_room.item:
                print ("\n  You find %s." % current_room.item.description)
                print ("  You take the %s." % current_room.item.name)
                Player.inventory.append(current_room.item)
                print ("\n Your inventory is now:")
                for i in Player.inventory:
                    print ("     -", i.name, "    damage =", i.dam)
                current_room.item = None

            while True:
                val = input("\nWhich way do you go?\n\n>").lower()

                if "help" in val:
                    print ("THIS IS THE HELP SCREEN.\nBEEP BOOP BEEP")

                elif val in current_room.paths:
                    val = current_room.paths[val]
                    current_room = self.scenes[val]
                    break

                else:
                    print ("\n", current_room.look)

        os.system('cls')
        current_room.enter()


class Scene(object):

    def __init__(self, enemy, item, look):
        self.enemy = enemy
        self.item = item
        self.look = look

        
class Start_Screen(Scene):

    paths = {'north': 'north',
             'south': 'south',
             'east': 'east',
             'west': 'west'}
    
    def enter(self):
        print ("""
                       ================================
                        ZZZZZZ  EEEEEE  FFFFFF  FFFFFF
                           ZZ   EE      FF      FF
                          ZZ    EEEEE   FFFFF   FFFFF
                         ZZ     EE      FF      FF
                        ZZZZZZ  EEEEEE  FF      FF
                       ================================
        """)

        print ("""

        You wake up under a dark night sky, your senses spinning.
	You feel the wind whipping west and immediately seek shelter.



                                -Instructions-
                    You Start With 100 Health Points (hp)
                        Use Compass Directions To Move
                Type "look" At Any Time To See Your Surroundings""")



class Main(Scene):

    paths = {'north': 'north',
             'south': 'south',
             'east': 'east',
             'west': 'west'}

    def enter(self):
        print ("\nYou are back at the beginning.")

#---NORTH---
class North(Scene):

    paths = {'south': 'main',
             'north': 'troll_den'}
    
    def enter(self):
        print ("""\n You travel north and find yourself
        terribly lost.""")


class Troll_Den(Scene):

    paths = {'south': 'north',
             'west': 'killer_troll'}

    def enter(self):
        print ("""
 You find yourself in the Troll's Den.
 You get the feeling you probably shouldn't be here...""")


class Killer_Troll(Scene):

    paths = {'east': 'troll_den'}

    def enter(self):
        print ("""
  You peek around the Troll's Den, trying to find some goodies,
  when you're spooked by a noise from behind.
  Just as you're about to turn around...""")
    

#---SOUTH---
class South(Scene):

    paths = {'north': 'main',
             'west': 'fishing_hut',
             'hut': 'fishing_hut'}
    
    def enter(self):
        print ("""
                                    SOUTH
                                    
        As you travel south the ground starts to become wet and muddy.
        You soon stumble upon a lake with an old fishing hut to the west.
        The smell of rotten fish is in the air...""")


class Fishing_Hut(Scene):

    paths = {'east': 'south',
             'oven': 'oven'}

    def enter(self):
        print ("""
    As you walk closer to the hut, the smell of fish
    gets heavier in the air. When you open the door, the odor comes to
    the point of absolute sickness. You go inside and find only stacks
    of dead fish scattered across the floor, all totally rotten. Some
    have been half devoured by maggots and some other infestation.

    The only thing that looks remotely interesting
    is the old wood burning oven...""")
        

class Oven(Scene):

    paths = {'east': 'south'}

    def enter(self):
        print ("""
    You open the stove to find that someone tried to
    burn a stack of papers rather hastily. One of the papers seems mostly
    undamaged...

    IT READS:
            "Today, while venturing into the caves to the west, I found
             a rather perculiar set of markings over the western wall
             where a hole opens up into the ground. I believe it to
             be of some old language, possibly latin. It says,
                "Lasciate ogne speranza, voi ch'intrate."

            I am unable to translate it at this time, but I hope to
            in the next couple of days.""")

    
#---EAST---
class East(Scene):

    paths = {'east': 'barn',
             'west': 'main'}

    def enter(self):
        print ("""
                                    EAST
                                    
	You look east and see in the distance what looks like a barn.
	As you get nearer you can tell the paint is worn to a dark-grey colour,
	faded by time.
	Once you get close, you spot faded footprints in the sand, leading
	further East.""")


class Barn(Scene):

    paths = {'down': 'barn_down',
             'west': 'east'}

    def enter(self):
        print ("""
    You notice the footprints are leading straight for the Barn, and devide
    to follow. As you get nearer to the Barn, There are strange markings that
    closely resemble a Baphomet head. The inside of the Barn smells of
    rotten flesh but is too dark to make out any details.""")


class Barn_Down(Scene):

    paths = {'up': 'barn'}

    def enter(self):
        print ("""
    This is the basement of the Barn.""")

#---WEST---
class West(Scene):

    paths = {'north': 'cave_main',
             'east': 'main'}

    def enter(self):
        print ("""
                                    WEST
                                    
	You stare into the endless abyss as the terrain has seemingly no end.
	But as you strain to see clearly through the whipping wind,
	you see a dim light illuminating the entrance
	of a small cave to the north.""")


class Cave_Main(Scene):

    paths = {'west': 'cave_west',
             'south': 'west'}

    def enter(self):
        print ("""
        As you approach the cave, you hear a faint sound
        emanating from the dark interior.
        The dim light came from an old lantern
        seemingly untouched for hundreds of years...        """)


class Cave_West(Scene):

    paths = {'down': 'cave_down_1',
             'east': 'cave_main'}

    def enter(self):
        print ("""
        You see a ladder leading down. The lantern's light
        does not reach the bottom of the hole...""")


class Cave_Down_1(Scene):

    paths = {'up': 'cave_west'}

    def enter(self):
        print ("""
    When you climb down the ladder, the light from the lantern
    illuminates some markings on the top of the passage. You can't quite
    make it out, but it definitely is not english.""")
      

class Last_Screen(Scene):

    def enter(self):
        input("Game Over")


Player = Player("Player", "This is me.", 100, 0)


items = {
    'fists': Item("Fists", "Your bloody knuckles", 2),
    'lantern': Item("Lantern", "an old, damaged lantern", 0),
    'knife': Item("Knife", "a rusty knife", 5),
    'club': Item("Club", "a giant piece of wood", 10),
    'battle-axe': Item("Battle-Axe", "a humungous axe you snagged off that Troll", 25),
    'dark-essence': Item("Dark Essence", "a formless black smoke", 30),
    'note': Item("note", "a note", 0)
    }

enemies = {
    'troll': Enemy("Troll", "A huge beast of a thing.", 10, 5),
    'big_troll': Enemy("Big Troll", "This Troll is even bigger than the last one!", 20, 12.5),
    'dark_beast': Enemy("Dark Beast", "No light illuminates this beast.", 25, 10)
    }

scenes = {
    'start_screen': Start_Screen(None, None, "You can go North, South, East, and West."),
    'last_screen': Last_Screen(None, None, None),
    'main': Main(None, None, "You can go North, South, East, or West."),
    #NORTH
    'north': North(enemies['troll'], items['club'], "You can go North or South"),
    'troll_den': Troll_Den(None, None, "You can go South or West."),
    'killer_troll': Killer_Troll(enemies['big_troll'], items['battle-axe'], "You can go East."),
    #SOUTH
    'south': South(None, None, "You can go North or West"),
    'fishing_hut': Fishing_Hut(None, None, "You can go East, back to the lake."),
    'oven': Oven(None, items['note'], "You can go East, back to the lake."),
    #EAST
    'east': East(None, None, "You can go West."),
    'barn': Barn(None, None, "You can go Up, Down, or around back."),
    'barn_down': Barn_Down(enemies['dark_beast'], items['dark-essence'], "You can go up."),
    #WEST
    'west': West(None, None, "You can go North and East."),
    'cave_main': Cave_Main(None, items['lantern'], "You can go North, South, East, or West."),
    'cave_west': Cave_West(None, None, "You can go down and East."),
    'cave_down_1': Cave_Down_1(None, items['knife'], "You can go Up.")
    }


Player.inventory.append(items['fists'])
    
game = Engine(scenes)
game.play()
