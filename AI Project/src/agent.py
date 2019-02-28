from gameobjects import GameObject
from move import Move, Direction
import numpy as np
import random
import time

class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """
        self.q_table = np.zeros([5,5,4,5,5,3])
        self.alpha = 0.6
        self.gamma = 0.2
        self.t = time.process_time()
        self.epsilon = 0.2
        self.depsilon = 0
        self.total_moves, self.total_penalties, self.food = 0, 0, 0


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
        state_pos = head_position
        state_posx = head_position[0]
        state_posy = head_position[1]
        state_dir = direction.value
        foodlocx, foodlocy = self.get_food_location(board)

        state = (state_posx, state_posy,state_dir, foodlocx, foodlocy)


        done = False

        while not done:

            reward = 0
            if(random.uniform(0,1) < self.epsilon):
                action = random.choice([-1,0,1])
            else:
                action = np.argmax(self.q_table[state])



            next_state_posx  = Direction.get_new_direction(direction,Move(action)).get_xy_manipulation()[0] + state_pos[0]
            next_state_posy = Direction.get_new_direction(direction,Move(action)).get_xy_manipulation()[1] + state_pos[1]
            next_state_dir = Direction.get_new_direction(direction, Move(action)).value

            if(0 <= next_state_posx < 5 and 0 <= next_state_posy < 5):
                done = True




        next_state = (next_state_posx,next_state_posy,next_state_dir,foodlocx,foodlocy)
        reward = self.reward(board,(next_state_posx,next_state_posy))

        if reward == 10000:
            self.food += 1


        old_value = self.q_table[state, int(action)]
        next_max = np.max(self.q_table[next_state])

        new_value = (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)
        self.q_table[state, action] = new_value


        self.total_moves += 1
        self.depsilon = self.total_moves * 0.0000000001
        if(self.depsilon < self.epsilon and self.epsilon > 0.1):
            self.epsilon = self.epsilon - self.depsilon
        else:
            self.epsilon = 0.1

        print("epsilon: " + str(self.epsilon))
        try:
            print("score: " + str(self.food / self.total_penalties) + "\n food: " + str(self.food) + "\n penalties: " + str(self.total_penalties))
        except:
            print("niks")
        return Move(action)

    def get_food_location(self, board):
        for x in range(len(board)):
            for y in range(len(board[x])):
                if (board[x][y] == GameObject.FOOD):
                    return (x,y)

    def reward(self, board, target):


        try:
            nextn = board[target[0]][target[1]]
            print(nextn)
            if(nextn == GameObject.WALL):
                self.total_penalties += 1
                return -100
            elif(nextn == GameObject.SNAKE_BODY):
                return -100
            elif(nextn == GameObject.EMPTY):
                return -1
            elif(nextn == GameObject.FOOD):
                return 10000
            elif(nextn == GameObject.SNAKE_HEAD):
                self.total_penalties += 1
                return -100
        except:
            print("ik kom hier")
            self.total_penalties += 1
            return -100
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
        return False

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
