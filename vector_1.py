# -*- coding: utf-8 -*-
import copy
import matplotlib.pyplot as plt
import numpy as np
import json


from matplotlib.colors import ListedColormap


"""
* GLOBAL VARIABLES
"""
special = {
    1: {},
    2: {
        (2, 2): [2, (4, 4), (4, 5)],
        (1, 8): [2, (4, 10), (4, 11)]
    },
    5: {
        (1, 8): [2, (1, 5), (1, 6)],
        (3, 3): [1, (8, 5), (8, 6)],
        (5, 6): [0, (8, 5), (8, 6)],
        (6, 14): [2, (8, 5), (8, 6)]
    },
    9: {
        (1, 13): [(1, 12), (1, 2)]
    }
}


class Vector:
    """
    This class implements 4 basic operations for a vector
    - rotate
    """
    def __init__(self, start_position=None, index=None):
        """
        Initial position of block
        Each element of the block has different id
        :param start_position: is a dict that stores [x, y] of block in 2D
        """
        if index:
            self.index = index
        if not start_position:
            self.x = 0
            self.y = 0
        else: 
            self.x = start_position[0]
            self.y = start_position[1]

    def rotate(self, direction=None):
        """
        This function return a new position of the vector after perform this action
        :param direction: string, 'left', 'right', 'up', 'down'
        :return: vector<int>(x,y,z)
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

    def get_idx(self):
        return self.index

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y    
        

class Block:
    """
    This class using class Vector to construct a block in the game
    :param stage: integer - the number of stage you want to start
    :return: object of Block
    """
    def __init__(self, first, second, z, is_controlled):
        """
        :param first: Vector(<x,y>, <index>)
        :param second: Vector(<x,y>, <index>)
        :param z: integer - height of entire block
        :param is_controlled: integer - 0, 1, 2
        :param stage: number of the state in game from 1 to 33
        """       
        # for later, we need to read file .txt to get start position for each stage
        # we divide the block to two small element
        # for example
        # self.first = Vector([0, 0], 1)          
        # self.second = Vector([0, 0], 2)               
        self.first = first
        self.second = second

        # store height of the block, if two elements have the same position (x1, y1) = (x2, y2), self.z = self.z1 + self.z2
        self.z = z

        # we also need to know what the element is controlled by the user
        # 0 - entire block
        # 1 - the first element
        # 2 - the second element
        self.is_controlled = is_controlled
        

    def move(self, direct=None):     
        # calculate new position
        # return: [<position of 1st>, <pos of 2nd>, <heigh of block>, <which element is controlled>]
        is_controlled = self.is_controlled

        first = copy.deepcopy(self.first)
        second = copy.deepcopy(self.second)
        z = copy.deepcopy(self.z)

        if is_controlled == 0:            
            if z == 2:
                # the height of entire block is 2, it need to update after perform
                # the action
                z = 1
                first = first.rotate(direct)
                second = second.rotate(direct)
                second = second.rotate(direct) 
            elif first.get_x() == second.get_x():
                # the block is horizontally
                if direct == 'up' or direct == 'down':
                    first = first.rotate(direct)
                    second = second.rotate(direct)
                elif first.get_y() < second.get_y():     
                    z = 2                                   
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
                
                elif first.get_y() > second.get_y():     
                    z = 2                                   
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
            elif first.get_y() == second.get_y():
                # the block is vertical
                if direct == 'left' or direct == 'right':
                    first = first.rotate(direct)
                    second = second.rotate(direct)                
                elif first.get_x() < second.get_x():     
                    z = 2                                   
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
                elif first.get_x() > second.get_x():     
                    z = 2                                   
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
            if is_controlled == 1:
                first = first.rotate(direct)
            elif is_controlled == 2:
                second = second.rotate(direct)            
            # check if the distance between 2 element is very close so we 
            # combine to entire the block

            if abs(first.get_x() - second.get_x()) == 1 and first.get_y() == second.get_y():
                # [1]
                # [2]                
                is_controlled = 0
            elif abs(first.get_y() - second.get_y()) == 1  and first.get_x() == second.get_x():
                # [1][2]
                is_controlled = 0
 
        return Block(first, second, z, is_controlled)   
            
      
def show_map(position=None, board=None, step=0):     

    data = np.array(board)  
    x1, y1 = position.first.x, position.first.y 
    x2, y2 = position.second.x, position.second.y 
    z = position.z

    if z == 2:
        data[x1, y1] = 3
    else:
        data[x1, y1] = 3
        data[x2, y2] = 3


    # convert the matrix to continously number
    u, i = np.unique(data, return_inverse=True)
    y = i.reshape(data.shape)
        
    plt.matshow(y, cmap=ListedColormap(['k', 'y', 'g', 'r', 'b']))
    plt.yticks(range(y.shape[0]), range(y.shape[0]))
    plt.xticks(range(y.shape[1]), range(y.shape[1]))
    plt.show()


def read_file(file_name):
    """
    Read the in in path ``file_name`` and return
    - start position of the block : [x, y]
    - board : matrix 2D    
    """
    with open(file_name) as f:
        reader = f.read()
        json_value = json.loads(reader)        
        return json_value["start"], np.array(json_value["board"])

def is_valid(position, board):
    """
    This function check valid position after moving the block
    :param position: Block
    :param board: matrix 2D
    """
    x1, y1 = position.first.x, position.first.y 
    x2, y2 = position.second.x, position.second.y 
    z = position.z    
    x, y = board.shape[0], board.shape[1]

    if x1 < 0 or x1 >= x or x2 < 0 or x2 >= x:
        return False

    if y1 < 0 or y1 >= y or y2 < 0 or y2 >= x:
        return False 

    if board[x1, y1] == 0 or board[x2, y2] == 0:
        return False

    if z == 2 and board[x1, y1] == 2:
        # orange cell
        return False

    return True


def change_board(position, board, stage):
    """Change the board if the current cell is 'O', 'X'
    :param stage: integer
    :param position: Block
    :param board: matrix 2D
    """
    x1, y1 = position.first.x, position.first.y 
    x2, y2 = position.second.x, position.second.y
    z = position.z    

    # X cell and O cell
    if (z == 2 and board[x1, y1] == 10) or (board[x1, y1] == 20 or board[x2, y2] == 20):
        # get cells will be changed
        # (1,8): [2,(4,10),(4,11), ...]
        key = (x1, y1) if board[x1, y1] == 20 else (x2, y2)
        cell_lst = special[stage][key]
        # get mode to change
        mode = cell_lst[0]
        # list cells will be changed
        change_cells = cell_lst[1:]
        for cell in change_cells:
            curr_val = board[cell[0], cell[1]]
            if mode == 2:
                # switch 0 -> 1 or 1 -> 0                
                board[cell[0], cell[1]] = 0 if curr_val == 1 else 1
            elif mode == 0:
                # change to 0 - no way
                board[cell[0], cell[1]] = 0
            elif mode == 1:
                board[cell[0], cell[1]] = 1
            elif mode == -1:
                # get current state of each cell
                board[cell[0], cell[1]] = cell[2]


def change_position(position, board, stage):

    """Change the block if the current cell is '( )'
    :param stage: integer
    :param position: Block
    :param board: matrix 2D
    """
    x1, y1 = position.first.x, position.first.y 
    x2, y2 = position.second.x, position.second.y
    z = position.z
    # ( ) cell
    if z == 2 and board[x1, y1] == 30:
        new_pos = special[stage][(x1, y1)]
        position.first.x = new_pos[0][0]
        position.first.y = new_pos[0][1]
        position.second.x = new_pos[1][0]
        position.second.y = new_pos[1][1]
        position.is_controlled = 1


def check_moves(position, board, stage):
    valid = is_valid(position, board)
    if not valid:
        return valid
    change_position(position, board, stage)
    change_board(position, board, stage)
    return valid


moves = {
    'L': 'left',
    'R': 'right',
    'U': 'up',
    'D': 'down'
}


def play(stage, paths):
    """
    Test functions
    :param paths: 'R-2,D-1,R-3,D-1'
    :param stage: integer
    """
    start, board = read_file('stage_%d.txt' % stage)
    block_2 = Block(Vector(start, 1), Vector(start, 2), 2, 0)
    show_map(block_2, board)
    i_step = 0
    steps = paths.split(',')
    for step in steps:
        splited_step = step.split('-')
        times = int(splited_step[1])
        direct = moves[splited_step[0]]
        for i in range(0, times):
            block_2 = block_2.move(direct)
            valid = check_moves(block_2, board, stage)
            show_map(block_2, board, i_step)
            i_step += 1
            if not valid:
                return False

def is_goal_state(position, board):
    x1, y1 = position.first.x, position.first.y 
    x2, y2 = position.second.x, position.second.y
    z = position.z

    if z == 2 and board[x1, y1] == 100:
        return True
    return False
    
def traceback_path(queue, goal_state): 
    """
    goal_state is node in queue
    """   
    solution = [goal_state[2]]
    idx = goal_state[3]
    while int(idx) > 0:
        solution.append(queue[idx][2])
        idx = queue[idx][3]    
    print(list(reversed(solution)))
    print("Number os steps = ", len(solution))

def BFS(stage=None):
    start, board = read_file('stage_%d.txt' % stage)
    block = Block(Vector(start, 1), Vector(start, 2), 2, 0)
    # Node: [<position>, <board>, <direction>, <index>]
    queue = [[block, board, None, 0]]

    for s in queue:
        if is_goal_state(s[0], board):
            print("Find the path!")
            # trace back the path
            traceback_path(queue, s)
            return True        
        for d in ['left', 'right', 'up', 'down']:
            pre_direct = s[2]
            if pre_direct == 'left' and d == 'right':
                continue
            elif pre_direct == 'right' and d == 'left':
                continue
            elif pre_direct == 'up' and d == 'down':
                continue
            elif pre_direct == 'down' and d == 'up':
                continue
            temp = s[0].move(direct=d)
            if check_moves(temp, board, stage):
                queue.append([temp, board, d, queue.index(s)])
            temp = None
        print(s[0].first.x, s[0].first.y, s[0].second.x, s[0].second.y)

if __name__ == "__main__":
    # play(2, 'U-1,R-1,D-1,R-3,U-3,R-1,D-2,R-4,U-1,L-1,U-1')
    BFS(1)
            

    