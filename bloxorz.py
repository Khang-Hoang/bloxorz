# -*- coding: utf-8 -*-
import copy
import numpy as np
import imp
import sys
import pygame


class Cube:
    """
    This class implements 4 basic operations for a vector
    - rotate
    """

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def rotate(self, direction=None):
        """
        This function return a new position of the vector after perform this action
        :param direction: string, 'left', 'right', 'up', 'down'
        :return: vector<int>(x,y,height)
        O
        +----------------> y
        '   |   |   |   |   |       
        '   |   |   |   |   |
        '   |   |   |   |   |
        '   |   |   |   |   |
        v
        x
        """
        result = copy.deepcopy(self)
        if direction == 'left':
            result.y = self.y - 1
        elif direction == 'right':
            result.y = self.y + 1
        elif direction == 'up':
            result.x = self.x - 1
        elif direction == 'down':
            result.x = self.x + 1
        return result


class Block:
    """
    This class using class Vector to construct a block in the game
    :param stage: integer - the number of stage you want to start
    :return: object of Block
    """

    def __init__(self, first, second):
        """
        :param first: Vector(<x,y>, <index>)
        :param second: Vector(<x,y>, <index>)
        :param height: integer - height of entire block
        :param controlled: integer - 0, 1, 2
        :param stage: number of the state in game from 1 to 33
        """
        # for later, we need to read file .txt to get start position for each stage
        # we divide the block to two small element
        # for example
        # self.first = Vector([0, 0], 1)
        # self.second = Vector([0, 0], 2)
        self.first = first
        self.second = second

        if (first.x == second.x and first.y == second.y):
            self.height = 2
        else:
            self.height = 1

    def is_stick(self):
        if (abs(self.first.x - self.second.x) <= 1 and self.first.y == self.second.y):
            return True
        elif (abs(self.first.y - self.second.y) <= 1 and self.first.x == self.second.x):
            return True
        return False

    def rotate(self, direct, controlled=None):
        # calculate new position
        # return: [<position of 1st>, <pos of 2nd>, <heigh of block>, <which element is controlled>]

        first = copy.deepcopy(self.first)
        second = copy.deepcopy(self.second)
        height = copy.deepcopy(self.height)

        if self.is_stick():
            if height == 2:
                first = first.rotate(direct)
                second = second.rotate(direct)
                second = second.rotate(direct)
            elif first.x == second.x:
                # the block is horizontally
                if direct == 'up' or direct == 'down':
                    first = first.rotate(direct)
                    second = second.rotate(direct)
                elif first.y < second.y:
                    if direct == 'left':
                        #  [x] <-- [1][2]
                        first = first.rotate(direct)
                        second = second.rotate(direct)
                        second = second.rotate(direct)
                    elif direct == 'right':
                        # [1][2] --> [x]
                        second = second.rotate(direct)
                        first = first.rotate(direct)
                        first = first.rotate(direct)

                elif first.y > second.y:
                    if direct == 'left':
                        #  [x] <-- [2][1]
                        second = second.rotate(direct)
                        first = first.rotate(direct)
                        first = first.rotate(direct)
                    elif direct == 'right':
                        # [2][1] --> [x]
                        first = first.rotate(direct)
                        second = second.rotate(direct)
                        second = second.rotate(direct)
            elif first.y == second.y:
                # the block is vertical
                if direct == 'left' or direct == 'right':
                    first = first.rotate(direct)
                    second = second.rotate(direct)
                elif first.x < second.x:
                    if direct == 'up':
                        #    [x]
                        #     ^
                        #     |
                        #    [1]
                        #    [2]
                        first = first.rotate(direct)
                        second = second.rotate(direct)
                        second = second.rotate(direct)
                    elif direct == 'down':
                        #    [1]
                        #    [2]
                        #     |
                        #     V
                        #    [x]
                        second = second.rotate(direct)
                        first = first.rotate(direct)
                        first = first.rotate(direct)
                elif first.x > second.x:
                    if direct == 'up':
                        #    [x]
                        #     ^
                        #     |
                        #    [2]
                        #    [1]
                        second = second.rotate(direct)
                        first = first.rotate(direct)
                        first = first.rotate(direct)
                    elif direct == 'down':
                        #    [2]
                        #    [1]
                        #     |
                        #     V
                        #    [x]
                        first = first.rotate(direct)
                        second = second.rotate(direct)
                        second = second.rotate(direct)
        else:
            # now, the block is break two elements
            # so we get the controlled element and move it
            if controlled == 1:
                first = first.rotate(direct)
            elif controlled == 2:
                second = second.rotate(direct)
        return Block(first, second)


class State:
    def __init__(self, direct, block, board, step, traceback=None):
        self.direct = direct
        self.block = block
        self.board = board
        self.step = step
        self.traceback = traceback

    def __eq__(self, other):
        return ((self.block.first.x == other.block.first.x and
                 self.block.first.y == other.block.first.y and
                 self.block.second.x == other.block.second.x and
                 self.block.second.y == other.block.second.y) or
                (self.block.first.x == other.block.second.x and
                 self.block.first.y == other.block.second.y and
                 self.block.second.x == other.block.first.x and
                 self.block.second.y == other.block.first.y)) and \
            np.array_equal(self.board, other.board)


class Game:
    def __init__(self, start, board, buttons):
        self.initState = State(None, Block(
            Cube(start), Cube(start)), np.array(board), 0)
        self.width, self.height = self.initState.board.shape
        self.buttons = buttons

    def is_valid(self, state):
        first = state.block.first
        second = state.block.second
        board = state.board
        if first.x < 0 or first.x >= self.width:
            return False

        if first.y < 0 or first.y >= self.height:
            return False

        if second.x < 0 or second.x >= self.width:
            return False

        if second.y < 0 or second.y >= self.height:
            return False

        if board[first.x, first.y] == 0:
            return False

        if board[second.x, second.y] == 0:
            return False

        if first.x == second.x and first.y == second.y and board[first.x, first.y] == 2:
            return False

        return True

    def get_next_state(self, state, direct, controlled):
        """get next state after rotate a cube or block
        :param state: current state
        :param direct: direction to move
        :param controlld: which cube to move or the entire block    
        """

        next_block = state.block.rotate(direct, controlled)
        next_board = copy.deepcopy(state.board)
        buttons = self.buttons
        x1, y1 = next_block.first.x, next_block.first.y
        x2, y2 = next_block.second.x, next_block.second.y
        z = next_block.height

        if ((x1, y1) in buttons or (x2, y2) in buttons):
            key = (x1, y1) if (x1, y1) in buttons else (x2, y2)
            if z == 2 and next_board[key] == 20 or next_board[key] == 10:
                for mode, pos in buttons[key]:
                    if mode == 0:
                        next_board[pos] = 0
                    elif mode == 1:
                        next_board[pos] = 1
                    elif mode == 2:
                        next_board[pos] = 1 if next_board[pos] == 0 else 0
            elif z == 2 and next_board[key] == 30:
                next_block.first.x, next_block.first.y = buttons[key][0]
                next_block.second.x, next_block.second.y = buttons[key][1]
        return State(direct, next_block, next_board, state.step + 1, state)


def is_contain(array, state):
    for temp in array:
        if temp == state:
            return True
    return False


def DFS(game):
    stack = [game.initState]
    visited = []
    solution = []
    while stack:
        state = stack.pop()
        visited.append(state)
        board = state.board
        block = state.block
        first = state.block.first
        second = state.block.second
        if first.x == second.x and first.y == second.y and board[first.x, first.y] == 100:
            while state.traceback:
                solution.insert(0, state)
                state = state.traceback
            solution.insert(0, state)
            return solution
        if block.is_stick():
            up = game.get_next_state(state, 'up', 0)
            down = game.get_next_state(state, 'down', 0)
            left = game.get_next_state(state, 'left', 0)
            right = game.get_next_state(state, 'right', 0)
            check_up = game.is_valid(up) and not is_contain(visited, up) and not is_contain(stack, up)
            check_down = game.is_valid(down) and not is_contain(visited, down) and not is_contain(stack, down)
            check_left = game.is_valid(left) and not is_contain(visited, left) and not is_contain(stack, left)
            check_right = game.is_valid(right) and not is_contain(visited, right) and not is_contain(stack, right)
            if check_up: stack.append(up)
            if check_down: stack.append(down)
            if check_left: stack.append(left)
            if check_right: stack.append(right)
        else:
            up1 = game.get_next_state(state, 'up', 1)
            down1 = game.get_next_state(state, 'down', 1)
            left1 = game.get_next_state(state, 'left', 1)
            right1 = game.get_next_state(state, 'right', 1)
            up2 = game.get_next_state(state, 'up', 2)
            down2 = game.get_next_state(state, 'down', 2)
            left2 = game.get_next_state(state, 'left', 2)
            right2 = game.get_next_state(state, 'right', 2)
            check_up1 = game.is_valid(up1) and not is_contain(visited, up1) and not is_contain(stack, up1)
            check_down1 = game.is_valid(down1) and not is_contain(visited, down1) and not is_contain(stack, down1)
            check_left1 = game.is_valid(left1) and not is_contain(visited, left1) and not is_contain(stack, left1)
            check_right1 = game.is_valid(right1) and not is_contain(visited, right1) and not is_contain(stack, right1)
            check_up2 = game.is_valid(up2) and not is_contain(visited, up2) and not is_contain(stack, up2)
            check_down2 = game.is_valid(down2) and not is_contain(visited, down2) and not is_contain(stack, down2)
            check_left2 = game.is_valid(left2) and not is_contain(visited, left2) and not is_contain(stack, left2)
            check_right2 = game.is_valid(right2) and not is_contain(visited, right2) and not is_contain(stack, right2)
            if check_up1: stack.append(up1)
            if check_down1: stack.append(down1)
            if check_left1: stack.append(left1)
            if check_right1: stack.append(right1)
            if check_up2: stack.append(up2)
            if check_down2: stack.append(down2)
            if check_left2: stack.append(left2)
            if check_right2: stack.append(right2)


def DFS1(state, visited):
    board = state.board
    block = state.block
    first = block.first
    second = block.second
    solutions = []
    if visited == None:
        visited = []
    visited.append(state)
    if first.x == second.x and first.y == second.y and board[first.x, first.y] == 100:
        solution = []
        while state.traceback:
            solution.insert(0, state)
            state = state.traceback
        solution.insert(0, state)
        #print solution
        # for state in solution:
            # print(state.direct, end=" ")
        # print("")
        solutions.append(solution)
        return solutions
    if block.is_stick():
        up = game.get_next_state(state, 'up', 0)
        down = game.get_next_state(state, 'down', 0)
        left = game.get_next_state(state, 'left', 0)
        right = game.get_next_state(state, 'right', 0)
        check_up = game.is_valid(up) and not is_contain(visited, up)
        check_down = game.is_valid(down) and not is_contain(visited, down)
        check_left = game.is_valid(left) and not is_contain(visited, left)
        check_right = game.is_valid(right) and not is_contain(visited, right)
        if len(solutions) > 0: return solutions
        if check_up:
            solutions.extend(DFS1(up, copy.deepcopy(visited)))
        if check_down:
            solutions.extend(DFS1(down, copy.deepcopy(visited)))
        if check_left:
            solutions.extend(DFS1(left, copy.deepcopy(visited)))
        if check_right:
            solutions.extend(DFS1(right, copy.deepcopy(visited)))
    return solutions
    


def show_map(states):
    # init game dimensions
    initState = states[0]
    TILESIZE = 50
    MAPHEIGHT, MAPWIDTH = initState.board.shape
    # a dictionary linking resources to colours
    BLACK = (44,  62,  80)
    GREY = (189, 195, 199)
    ORANGE = (205,  97,  51)
    CUBE = (192,  57,  43)
    OBUTTON = (52, 152, 219)
    XBUTTON = (41, 128, 185)
    TELEPORT = (30,  55, 153)

    colors = {
        0: BLACK,
        1: GREY,
        2: ORANGE,
        10: OBUTTON,
        20: XBUTTON,
        30: TELEPORT,
        100: BLACK
    }
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(
        (MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
    step = 0
    length = len(states)
    while True:
        # get all the user events
        # for event in pygame.event.get():
            # if the user wants to quit
            # if event.type == pygame.QUIT:
                # and the game and close the window
                # pygame.quit()
                # sys.exit()            
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         if (step > 0):
            #             step = step - 1
            #     if event.key == pygame.K_RIGHT:
            #         if (step < length - 1):
            #             step = step + 1            
        step += 1
        # loop through each row
        state = states[step]
        first = state.block.first
        second = state.block.second
        pygame.display.set_caption(
            'step %d, direct: %s' % (step, state.direct))
        for row in range(MAPHEIGHT):
            # loop through each column in the row
            for column in range(MAPWIDTH):
                pos = state.board[row, column]
                color = colors[pos]
                text = None
                coords = (column*TILESIZE, row*TILESIZE, TILESIZE/2, TILESIZE/2)
                if pos == 10:
                    # OBUTTON
                    text = pygame.font.SysFont("sans", 40).render("O", True, (0,0,0))
                elif pos == 20:
                    # XBUTTON
                    text = pygame.font.SysFont("sans", 40).render("X", True, (0,0,0))
                elif pos == 30:
                    # TELEPORT
                    text = pygame.font.SysFont("sans", 40).render("( )", True, (0,0,0))                                
                # draw the resource at that position in the tilemap, using the correct colour
                pygame.draw.rect(DISPLAYSURF, color, (
                    column*TILESIZE, row*TILESIZE, TILESIZE, TILESIZE))
                if text:
                    DISPLAYSURF.blit(text, coords)
        pygame.draw.rect(DISPLAYSURF, CUBE, (first.y*TILESIZE,
                                             first.x*TILESIZE, TILESIZE, TILESIZE))
        pygame.draw.rect(DISPLAYSURF, CUBE, (second.y*TILESIZE,
                                             second.x*TILESIZE, TILESIZE, TILESIZE))

        # update the display
        pygame.display.update()
        pygame.time.delay(500)


if __name__ == "__main__":


    stage = imp.load_source('stage', 'stage/stage10.py')
    game = Game(stage.start, stage.board, stage.buttons)
    solution = DFS(game)
    show_map(solution)


    # stage = imp.load_source('stage', 'stage/stage0.py')
    # game = Game(stage.start, stage.board, stage.buttons)
    # solutions = DFS1(game.initState, [])
    # solution = solutions[0]
    # min_sol = len(solution)
    # for item in solutions:
    #     if len(item) < min_sol:
    #         solution = item
    #         min_sol = len(item)
    # print(len(solutions))
    # show_map(solution)
    # show_map([state])
    
    # """Stage 1: R-2, D-1, R-3, D-1"""
    # stage = imp.load_source('stage', 'stage/stage1.py')
    # game = Game(stage.start, stage.board, stage.buttons)
    # states = []
    # state = game.initState
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # show_map(states)

    # """Stage 2: U-1, R-1, D-1, R-3, U-3, R-1, D-2, R-4, U-1, L-1, U-1"""
    # stage = imp.load_source('stage', 'stage/stage1.py')
    # game = Game(stage.start, stage.board, stage.buttons)
    # state = game.initState
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # show_map(states)

    # """Stage 4: U-1, L-1, U-1, R-2, U-1, R-6, D-1, R-1, D-5, R-1, U-1, L-6, D-1"""
    # stage = imp.load_source('stage', 'stage/stage4.py')
    # game = Game(stage.start, stage.board, stage.buttons)
    # states = []
    # state = game.initState
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'left', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 0)
    # states.append(state)
    # show_map(states)

    # """Stage 8: R-2, D-3, R-2, S-1, U-3, R-2"""
    # stage = imp.load_source('stage', 'stage/stage8.py')
    # game = Game(stage.start, stage.board, stage.buttons)
    # states = []
    # state = game.initState
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 1)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 1)
    # states.append(state)
    # state = game.get_next_state(state, 'down', 1)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 1)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 1)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 2)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 2)
    # states.append(state)
    # state = game.get_next_state(state, 'up', 2)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 2)
    # states.append(state)
    # state = game.get_next_state(state, 'right', 0)
    # states.append(state)
    # show_map(states)
