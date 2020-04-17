from os import path
from algorithm import DFS, BFS


class Wall:
    pass


class Door:
    pass


class Bot:
    pass


class Vector():
    """
    A vector to determine bots coordinates
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def plus(self, other_v):
        """
        adding a new vector to the current vector
        """
        return Vector(other_v.x + self.x, other_v.y + self.y)


class ParseMaze():
    """
    Parsing the maze
    """
    def __init__(self, filename, legend):

        if path.exists(filename):
            with open(filename) as f:
                self.contents = [line.rstrip('\n') for line in f.readlines()]

        self.h = len(self.contents)
        self.w = len(self.contents[0])
        self.legend = legend
        self.goal = None
        self.start = None
        self.solution = None
        self.space = [' '] * (self.h * self.w)

    def isinside(self, v):
        """
        check the position of the bot
        if it's inside the maze
        """
        return (0 <= v.x < self.w) and (0 <= v.y < self.h)

    def get_position(self, v):
        return self.space[v.y + (self.h * v.x)]

    def set_position(self, value, v):
        """
        set the bot to a new position
        """
        self.space[v.y + (self.h * v.x)] = value

    def get_character(self, element):
        """
        Get the character holding a position in the maze
        """
        if not element or element == ' ':
            return ' '
        return element.origin_char

    def char_element(self, legend, ch):
        """
        Reference each character by an object
        """
        if ch == ' ':
            return None
        element = legend[ch](
        )  # an example of legend is 'b' which is reference by an object Bot()
        element.origin_char = ch  # create a new field in the object
        return element

    def parser(self):
        """
        Get all the characters and create a one-dimensional array
        """
        for x in range(self.h):
            for y in range(self.w):
                self.set_position(
                    self.char_element(self.legend, self.contents[x][y]),
                    Vector(x, y))

    def set_start_goal(self):
        """
        Get the starting position for the bot and the goal
        """
        self.parser()  # parse the maze

        for index, element in enumerate(self.space):
            ch = self.get_character(element)
            c = index // self.h, index % self.h

            if ch == 'b':
                self.start = c
            elif ch == 'e':
                self.goal = c

    def output(self, sol, count):
        """
        Humanize the output
        """
        for x in range(self.h):
            out = ''
            for y in range(self.w):
                coords = (x, y)
                if coords in sol:
                    if coords == self.goal:
                        out += '█'
                    else:
                        out += '*'
                else:
                    v = Vector(x, y)
                    ch = self.get_character(self.get_position(v))

                    if coords == self.start:
                        out += 'ß'
                    elif ch == ' ':
                        out += ch
                    else:
                        out += '░'
            print(out)


class Maze(ParseMaze):
    """
    Maze
    """
    def __init__(self, filename, legend):
        super().__init__(filename, legend)
        self.set_start_goal()

    def adjacent_coords(self, current_state):
        """
        Get all the nearest neighbours for the current visited node
        """
        directions = {
            'N': (0, 1),
            'E': (1, 0),
            'W': (-1, 0),
            'S': (0, -1)
        }  # vector coordinates

        (r, c) = current_state
        neighbours = []

        for action in directions.keys():
            x, y = directions[action]
            row, col = r + x, c + y
            v = Vector(row, col)
            agent = self.get_position(v)

            if not agent or self.get_character(agent) == 'e':
                neighbours.append((action, (row, col)))

        return neighbours

    def solve(self):
        dfs = BFS()
        count, self.solution = dfs.algorithm(self.start, self.goal,
                                             self.adjacent_coords)
        self.output(self.solution, count)


if __name__ == '__main__':
    legend = {'#': Wall, 'b': Bot, 'e': Door}
    s = Maze('map.txt', legend)
    s.solve()
