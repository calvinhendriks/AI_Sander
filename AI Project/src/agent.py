from gameobjects import GameObject
from move import Move, Direction
from queue import PriorityQueue

class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
        
        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
        0]][head_position[1]] == GameObject.SNAKE_HEAD.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """
        self.board = board
        foodlocation= self.get_food_location(self.board)
        route, cost = self.a_star_search(self.board,head_position,foodlocation,direction)
        nextlocation = (1,2)
        print(route.items())
        print("Next location: " + str(nextlocation))
        x, y = head_position
        xnext, ynext = nextlocation

        if(direction == Direction.NORTH):
            #STRAIGHT
            if(x == xnext & y + 1 == ynext):
                return Move.STRAIGHT
            #LEFT
            if(x - 1 == xnext & y == ynext):
                return Move.LEFT
            #RIGHT
            if(x + 1 == xnext & y == ynext):
                return Move.RIGHT


        elif(direction == Direction.EAST):
            if(x + 1 == xnext & y == ynext):
                return Move.STRAIGHT
            if(x  == xnext & y + 1 == ynext):
                return Move.LEFT
            if(x == xnext & y - 1 == ynext):
                return Move.RIGHT

        elif(direction == Direction.SOUTH):
            if(x  == xnext & y - 1 == ynext):
                return Move.STRAIGHT
            if(x + 1 == xnext & y == ynext):
                return Move.LEFT
            if(x - 1 == xnext & y == ynext):
                return Move.RIGHT

        elif(direction == Direction.WEST):
            if(x - 1 == xnext & y == ynext):
                return Move.STRAIGHT
            if(x  == xnext & y - 1 == ynext):
                return Move.LEFT
            if(x == xnext & y + 1 == ynext):
                return Move.RIGHT


        return Move.STRAIGHT

    



    def a_star_search(self, board, start, goal,direction):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0
        previousdir= direction
        while not frontier.empty():
            current = frontier.get()
        
            if current == goal:
                break
            print()
            for next in self.get_neighbours(current,previousdir):
                print(str(next[0]) + "," + str(next[1]))
                new_cost = cost_so_far[current] + self.cost(board, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current
                previousdir = self.get_nextdirection(current,next,previousdir)
        return came_from, cost_so_far

    def heuristic(self,a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return True

    def on_die(self, head_position, board, score, body_parts):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """
    def get_neighbours(self, current, direction):
        neighbours = []
        iks, yj = current
        print("get_neighbours for: " + str(current))
        if(direction == Direction.NORTH):
            leftx, lefty = iks - 1, yj
            straightx, straighty = iks , yj + 1
            rightx, righty = iks + 1, yj
            if (leftx > 0 & leftx < 24 & lefty > 0 & lefty < 24 ):
                neighbours.append((leftx,lefty))
            if (rightx > 0 & rightx < 24 & righty > 0 & righty < 24 ):
                neighbours.append((rightx,righty))
            if (straightx > 0 & straightx < 24 & straightx > 0 & straightx < 24 ):
                neighbours.append((straightx,straighty))
            return neighbours


        elif(direction == Direction.EAST):
            leftx, lefty = iks, yj + 1
            straightx, straighty = iks +1, yj
            rightx, righty = iks, yj -1
            if (leftx > 0 & leftx < 24 & lefty > 0 & lefty < 24 ):
                neighbours.append((leftx,lefty))
            if (rightx > 0 & rightx < 24 & righty > 0 & righty < 24 ):
                neighbours.append((rightx,righty))
            if (straightx > 0 & straightx < 24 & straightx > 0 & straightx < 24 ):
                neighbours.append((straightx,straighty))
            return neighbours

        elif(direction == Direction.SOUTH):
            leftx, lefty = iks + 1, yj
            straightx, straighty = iks, yj -1
            rightx, righty = iks - 1, yj
            if (leftx > 0 & leftx < 24 & lefty > 0 & lefty < 24 ):
                neighbours.append((leftx,lefty))
            if (rightx > 0 & rightx < 24 & righty > 0 & righty < 24 ):
                neighbours.append((rightx,righty))
            if (straightx > 0 & straightx < 24 & straightx > 0 & straightx < 24 ):
                neighbours.append((straightx,straighty))
            return neighbours

        elif(direction == Direction.WEST):
            leftx, lefty = iks, yj -1
            straightx, straighty = iks -1, yj
            rightx, righty = iks, yj +1
            if (leftx > 0 & leftx < 24 & lefty > 0 & lefty < 24 ):
                neighbours.append((leftx,lefty))
            if (rightx > 0 & rightx < 24 & righty > 0 & righty < 24 ):
                neighbours.append((rightx,righty))
            if (straightx > 0 & straightx < 24 & straightx > 0 & straightx < 24 ):
                neighbours.append((straightx,straighty))
            return neighbours



    def get_food_location(self, board):
        for x in range(len(board)):
            for y in range(len(board[x])):
                if (board[x][y] == GameObject.FOOD):
                    return (x,y)
        return

    def cost(self, board, target):
        next = board[target[0]][target[1]]
        if(next == GameObject.WALL):
            return 1000
        elif(next == GameObject.SNAKE_BODY):
            return 1000
        elif(next == GameObject.EMPTY):
            return 1
        elif(next == GameObject.FOOD):
            return 0
        elif(next == GameObject.SNAKE_HEAD):
            return 1000

    def get_nextdirection(self, current, goal, direction):
        xnext, ynext = goal
        x,y = current
        if(direction == Direction.NORTH):
            #STRAIGHT
            if(x == xnext & y + 1 == ynext):
                return Direction.NORTH
            #LEFT
            if(x - 1 == xnext & y == ynext):
                return Direction.WEST
            #RIGHT
            if(x + 1 == xnext & y == ynext):
                return Direction.EAST


        elif(direction == Direction.EAST):
            if(x + 1 == xnext & y == ynext):
                return Direction.EAST
            if(x  == xnext & y + 1 == ynext):
                return Direction.NORTH
            if(x == xnext & y - 1 == ynext):
                return Direction.SOUTH

        elif(direction == Direction.SOUTH):
            if(x  == xnext & y - 1 == ynext):
                return Direction.SOUTH
            if(x + 1 == xnext & y == ynext):
                return Direction.EAST
            if(x - 1 == xnext & y == ynext):
                return Direction.WEST

        elif(direction == Direction.WEST):
            if(x - 1 == xnext & y == ynext):
                return Direction.WEST
            if(x  == xnext & y - 1 == ynext):
                return Direction.SOUTH
            if(x == xnext & y + 1 == ynext):
                return Direction.NORTH
