"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    # replace with your code from the previous mini-project
    length = len(line)
    result = [0] * length 
    result_index = 0
    
    for line_index in range(length):
        if line[line_index] != 0:
            result[result_index] = line[line_index]
            result_index += 1
            
    for key in range(length - 1):
        if result[key] == result[key + 1]:
            result[key] += result[key + 1]
            result.pop(key + 1)
            result.append(0)
    
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
        up_start_list = [(0, i) for i in range(0, self._width)]
        down_start_list = [(self._height - 1, i) for i in range(0, self._width)] 
        left_start_list = [(i, 0) for i in range(0, self._height)]
        right_start_list = [(i, self._height - 1) for i in range(0, self._height)]
        self._initial_dict = {UP:up_start_list, DOWN:down_start_list, LEFT:left_start_list, RIGHT:right_start_list}
    

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._cell = [[0 * col * row for col in range(self._width)] for row in range(self._height)]
        self.new_tile()
        self.new_tile()

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        output = ''
        for row in self._cell:
            for entry in row:
                output += str(entry) + '\t'
            output += '\n'
        return output

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        start_list = self._initial_dict[direction]

        row = start_list[0][0]
        col = start_list[0][1]
        
        changed = 0
        while 0 <= row < self._height and 0 <= col < self._width:
            crow = row
            ccol = col
            line = []
            while 0 <= crow < self._height and 0 <= ccol < self._width:
                line += [self.get_tile(crow, ccol)]
                crow += OFFSETS[direction][0]
                ccol += OFFSETS[direction][1]
            crow = row
            ccol = col
            newline = merge(line)
            if newline != line:
                changed += 1
            item = 0
            while 0 <= crow < self._height and 0 <= ccol < self._width:
                self.set_tile(crow, ccol, newline[item])
                crow += OFFSETS[direction][0]
                ccol += OFFSETS[direction][1]
                item += 1
            row += 1 - abs(OFFSETS[direction][0])
            col += 1 - abs(OFFSETS[direction][1])
        if changed > 0:
            self.new_tile()
            
        print self._cell

            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zeros_index = [[row_ind, col_ind] for row_ind, col_ind in zip(range(self._width), range(self._height)) if self._cell[row_ind][col_ind] == 0]
        
        
        if len(zeros_index) != 0:
            new_select_ind = zeros_index[random.randint(0, len(zeros_index) - 1)]
            if random.randint(0,9) > 0:
                new_select_value = 2
                
            else:
                new_select_value = 4
                
            self.set_tile(new_select_ind[0], new_select_ind[1], new_select_value)      
        
        

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._cell[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._cell[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

