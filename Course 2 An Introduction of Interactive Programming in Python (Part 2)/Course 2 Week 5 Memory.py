# implementation of card game - Memory

import simplegui
import random

turn = 0

# helper function to initialize globals
def new_game():
    global num_list, exposed, check, turn
    num_list = range(0, 8) + range(0, 8)
    random.shuffle(num_list)
    
    exposed = [False] * 16

    check = 0
    turn = 0

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    
    global exposed, num_list, check, first_exposed, second_exposed, turn
    flip_num = pos[0] / 50
    
    if not exposed[flip_num]:
        if check == 0:
            exposed[flip_num] = True
            first_exposed = flip_num
            check = 1
        elif check == 1:
            exposed[flip_num] = True
            second_exposed = flip_num
            check = 2
        elif check == 2:
            if num_list[first_exposed] != num_list[second_exposed]:
                exposed[first_exposed] = False
                exposed[second_exposed] = False
            exposed[flip_num] = True
            first_exposed = flip_num
            check = 1
            turn += 1
                                
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    for k in range(50, 800, 50):
        canvas.draw_line([k, 0], [k, 100], 1, "White")
    
    for num, j in zip(num_list, range(15, 800, 50)):
        canvas.draw_text(str(num), [j, 60], 24, "White")
               
    for ex, i in zip(exposed, range(50, 850, 50)):
        if not ex:
            canvas.draw_polygon([[i-50, 0], [i, 0], [i, 100], [i-50, 100]], 1, 'White', 'Green') 

    label.set_text("Turns = " + str(turn))

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
label = frame.add_label("Turns = 0")

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric