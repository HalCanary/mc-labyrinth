#!/usr/bin/python
# Copyright 2015 Hal Canary
# Use of this program is governed by the file LICENSE.md.

import random
import sys
import time

class Vector(tuple):
    '''
    A three-vector that represents a point in space.
    '''
    __slots__ = ()
    @property
    def x(self):
        return self[0]
    @property
    def y(self):
        return self[1]
    @property
    def z(self):
        return self[2]
    def __new__(cls, x, y, z):
        return tuple.__new__(cls, (x, y, z))
    def __repr__(self):
        return 'Vector(%r, %r, %r)' % self
    def __str__(self):
        return '%r %r %r' % self
    def __add__(self, v):
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
    def __mul__(self, s):
        return Vector(s * self.x, s * self.y, s * self.z)
    def __sub__(self, v):
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
    def amul(self, v):
        '''
        array-multiplication
        '''
        return Vector(self.x * v.x, self.y * v.y, self.z * v.z)
    @staticmethod
    def X():
        return Vector(1, 0, 0)
    @staticmethod
    def Y():
        return Vector(0, 1, 0)
    @staticmethod
    def Z():
        return Vector(0, 0, 1)
    @staticmethod
    def Ones():
        return Vector(1, 1, 1)

def write(arg):
    sys.stdout.write(arg)
    sys.stdout.write('\n')
    sys.stdout.flush()

class MC:
    '''
    Mincecraft constantants and functions.
    '''
    air = 'minecraft:air'
    glass = 'minecraft:glass'
    glow = 'minecraft:glowstone'
    brick = 'minecraft:stonebrick'
    bedrock = 'minecraft:bedrock'
    torch = 'minecraft:torch'
    stone = 'minecraft:stone'
    @staticmethod
    def fill(v, u, t):
        write('fill %s %s %s' % (v, u, t))
    @staticmethod
    def setblock(v, t, datavalue=None, entity=None):
        if datavalue is None:
            datavalue = ''
        if entity is None:
            entity = ''
        else:
            entity = 'replace ' + entity
        write('setblock %s %s %s %s' % (v, t, datavalue, entity))
    @staticmethod
    def setladder(v, height, datavalue):
        write('fill %s %s minecraft:ladder %s' % (
            v, v + Vector(0, height - 1, 0), datavalue))
    @staticmethod
    def set_chest(pos, direction, items):
        MC.setblock(pos, 'minecraft:chest', direction,
                    '{Items:[%s]}' % ','.join(
                        '{id:%d,Count:%d,Slot:%d}' % (i[0], i[1], j)
                        for j, i in enumerate(items)))
    @staticmethod
    def hollow_cube(wln_corner, ehs_corner, material):
        west, low, north = wln_corner
        east, high, south = ehs_corner
        MC.fill(Vector(west, low, north), Vector(east, low, south), material)
        MC.fill(Vector(west, high, north), Vector(east, high, south), material)
        MC.fill(Vector(east, low, north), Vector(east, high, south), material)
        MC.fill(Vector(west, low, north), Vector(west, high, south), material)
        MC.fill(Vector(west, low, north), Vector(east, high, north), material)
        MC.fill(Vector(west, low, south), Vector(east, high, south), material)
    class Items:
        diamond_block = 57 
        iron_block = 42 
        pumpkin = 86 
        coal_block = 173
        slime_block = 165
        slime_ball = 341
        ink_sack = 352
        apple = 260
        torch = 50 
        brown_mushroom = 39 
        log = 17 
        string  = 287
        potato = 392
        bread = 297
        melon_block = 103
        saddle = 329
        red_mushroom  = 40
        cocoa = 127
        experience_bottle = 384
        gold_block = 41
        blaze_rod = 369
        emerald_block = 133
        name_tag = 421	
        diamond_horse_armor = 419	

def make_maze(dimensions, origin, seed):
    class MazeDirections:
        '''
        bit field constants to represent directions
        '''
        up = 1 << 0
        down = 1 << 1
        north = 1 << 2
        south = 1 << 3
        east = 1 << 4
        west = 1 << 5

    def pick(probability_dict):
        '''
        Return one of the keys, with probability proportional to the given value.
        '''
        total_prob = sum(prob for prob in probability_dict.itervalues())
        rnd = random.uniform(0, total_prob)
        for item, prob in probability_dict.iteritems():
            rnd -= prob
            if rnd <= 0:
                return item
        assert False

    def grid(dim):
        '''
        Generate all the integral vectors in the given interval.
        '''
        for k in xrange(dim.z):
            for j in xrange(dim.y):
                for i in xrange(dim.x):
                    yield Vector(i, j, k)
    def recursive_maze_maker(maze, v):
        def neighbors(v):
            return {v + Vector.Z(): 9,
                    v - Vector.Z(): 9,
                    v + Vector.Y(): 1,
                    v - Vector.Y(): 1,
                    v + Vector.X(): 9,
                    v - Vector.X(): 9}
        def unvisited_neighbors(maze, v):
            return dict((pos, prob)
                        for pos, prob in neighbors(v).iteritems()
                        if pos in maze and maze[pos] == 0)
        def connect(maze, u, v):
            # x-axis : east (+) or west (-)
            # y-axis : high (+) or low (-)
            # z-axis : south (+) or north (-)
            diff = u - v
            if diff.x + diff.y + diff.z < 0:
                connect(maze, v, u)
            elif diff == Vector(0, 0, 1):  # u is south of v
                maze[v] |= MazeDirections.south
                maze[u] |= MazeDirections.north
            elif diff == Vector(0, 1, 0):  # u is above v
                maze[v] |= MazeDirections.up
                maze[u] |= MazeDirections.down
            elif diff == Vector(1, 0, 0):  # u is east of v
                maze[v] |= MazeDirections.east
                maze[u] |= MazeDirections.west
            else:
                assert False

        possibles = unvisited_neighbors(maze, v)
        while possibles:
            p = pick(possibles)
            connect(maze, v, p)
            recursive_maze_maker(maze, p)
            possibles = unvisited_neighbors(maze, v)

    dimensions = Vector(*dimensions)
    origin = Vector(*origin)
    random.seed(seed)
    maze = {room: 0 for room in grid(dimensions)}
    recursive_maze_maker(maze, Vector(0,0,0))
    block = Vector(8, 6, 8)

    center = origin + dimensions.amul(Vector(4, 0, 4))
    player_loc = Vector(center.x, 200, center.z)
    #player_loc = origin + dimensions.amul(Vector(4, 0, 4)) + Vector(0, 200, 0)
    write('tp @p %s' % str(player_loc))
    time.sleep(0.25)
    MC.hollow_cube(player_loc - Vector.Ones() * 4,
                   player_loc + Vector.Ones() * 4,
                   MC.glass)
    MC.fill(player_loc - Vector.Ones() * 3,
            player_loc + Vector.Ones() * 3,
            MC.air)
    time.sleep(2)
    write('tp @p %s' % str(player_loc))

    MC.hollow_cube(origin - Vector.Ones(),
                   origin + block.amul(dimensions) + Vector.Ones(),
                   MC.stone)

    entrance = Vector(0, dimensions.y - 1, 0)
    maze[entrance] |= MazeDirections.up

    e = origin + entrance.amul(block) + Vector(4, 6, 4)
    MC.fill(Vector(e.x - 1, e.y, e.z - 1),
            Vector(e.x + 1, 64, e.z + 1),
            MC.brick)
    MC.setladder(e, 128-e.y, 4)

    for room in grid(dimensions):
        #room = Vector(i, j, k)
        monsters = pick({True: 1, False: 8})
        light = pick({True: 1, False: 8}) or room == entrance
        has_chest = pick({True: 1, False: 8})

        o = origin + room.amul(block)
        mazeValue = maze[room]

        if False:
            MC.fill(o, o + block, MC.air)
            MC.setblock(o + Vector(4, 3, 4), MC.glow)
            continue

        #clear
        MC.hollow_cube(o, o + block, MC.brick)
        MC.hollow_cube(o + Vector.Ones(), o + block - Vector.Ones(), MC.brick)
        #MC.fill(o , o + block, MC.brick)
        MC.fill(o + Vector(2, 2, 2) , o + block - Vector(2, 2, 2), MC.air)

        # floor
        if not mazeValue & MazeDirections.down:
            MC.fill(o, o + Vector(8, 0, 8), MC.bedrock)
        else:
            MC.fill(o + Vector(4, 0, 4), o + Vector(4, 1, 4), MC.air)
            MC.setladder(o + Vector(4, 0, 4), 2, 4)

        # ceiling
        if not mazeValue & MazeDirections.up:
            MC.fill(o + Vector(0, 6, 0), o + Vector(8, 6, 8), MC.bedrock)
            #light
            if light:
                MC.setblock(o + Vector(4, 5, 4), MC.glow)
        else:
            MC.fill(o + Vector(4, 5, 4), o + Vector(4, 6, 4), MC.air)
            MC.fill(o + Vector(5, 2, 4), o + Vector(5, 6, 4), MC.brick)
            MC.setladder(o + Vector(4, 2, 4), 5, 4)
            if light:
                MC.setblock(o + Vector(6, 4, 4), MC.torch, 1)
                MC.setblock(o + Vector(2, 4, 4), MC.torch, 1)
            # 1 Facing east (attached to a block to its west)
            # 2 Facing west (attached to a block to its east)
            # 3 Facing south (attached to a block to its north)
            # 4 Facing north (attached to a block to its south)

            #   0 1 2 3 4 5 6 7 8
            # 6 B S S S   S S S B
            # 5 B S S S . S S S B
            # 4 B S           S B
            # 3 B S           S B
            # 2 B S           S B
            # 1 B S S S S S S S B
            # 0 B B B B B B B B B

            # 2: Ladder facing north
            # 3: Ladder facing south
            # 4: Ladder facing west
            # 5: Ladder facing east

        # west wall
        if not mazeValue & MazeDirections.west:
            MC.fill(o, o + Vector(0, 6, 8), MC.bedrock)
        else:
            MC.fill(o + Vector(0, 2, 2), o + Vector(1, 4, 6), MC.air)
        # east wall
        if not mazeValue & MazeDirections.east:
            MC.fill(o + Vector(8, 0, 0), o + Vector(8, 6, 8), MC.bedrock)
        else:
            MC.fill(o + Vector(7, 2, 2), o + Vector(8, 4, 6), MC.air)

        # north wall
        if not mazeValue & MazeDirections.north:
            MC.fill(o, o + Vector(8, 6, 0), MC.bedrock)
        else:
            MC.fill(o + Vector(2, 2, 0), o + Vector(6, 4, 1), MC.air)
        #south wall
        if not mazeValue & MazeDirections.south:
            MC.fill(o + Vector(0, 0, 8), o + Vector(8, 6, 8), MC.bedrock)
        else:
            MC.fill(o + Vector(2, 2, 7), o + Vector(6, 4, 8), MC.air)

        if monsters:
            MC.setblock(o + Vector(2,2,2), 'minecraft:mob_spawner', 0,
                        '{EntityId:%d}' % pick({51:1,52:1,54:1}))

        if has_chest:
            chest_map = {
                7: [(MC.Items.apple, 1),
                    (MC.Items.torch, 16)],
                6: [(MC.Items.ink_sack, 1),
                    (MC.Items.brown_mushroom, 1),
                    (MC.Items.red_mushroom, 1)],
                5: [(MC.Items.slime_ball, 1),
                    (MC.Items.log, 4),
                    (MC.Items.cocoa,1)],
                4: [(MC.Items.coal_block, 1),
                    (MC.Items.string, 4)],
                3: [(MC.Items.slime_block, 1),
                    (MC.Items.potato, 1),
                    (MC.Items.experience_bottle, 3)],
                2: [(MC.Items.pumpkin, 1),
                    (MC.Items.bread, 2),
                    (MC.Items.gold_block, 1)],
                1: [(MC.Items.iron_block, 1),
                    (MC.Items.melon_block, 1),
                    (MC.Items.blaze_rod, 2),
                    (MC.Items.name_tag,1)],
                0: [(MC.Items.diamond_block, 2),
                    (MC.Items.saddle, 1),
                    (MC.Items.emerald_block, 1),
                    (MC.Items.diamond_horse_armor, 1)]
            }
            MC.set_chest(o + Vector(6,2,2), 4, chest_map[room.y])

    MC.set_chest(origin + entrance.amul(block) + Vector(2,2,6), 4,
                 [(173, 64), (17,64), (17,64), (298, 1), (299, 1),
                  (300, 1), (301, 1), (267, 1)])

    write('tp @p %s' % str(origin + entrance.amul(block) + Vector(3,2,4)))
    MC.hollow_cube(player_loc - Vector.Ones() * 3,
                   player_loc + Vector.Ones() * 3,
                   MC.air)

if __name__ == '__main__':
    SEED = 12345678
    DIMENSIONS = (8, 8, 8)
    ORIGIN = (0, 4, 0)
    make_maze(DIMENSIONS, ORIGIN, SEED)
