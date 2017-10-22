# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [random.randrange(60, 180) / 60, random.randrange(120, 240) / 60]
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0
displayed = True
count = 0
timer_interval = 1000

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2 , HEIGHT / 2]
    ball_vel[1] = -random.randrange(60, 180) / 60
    
    if direction == RIGHT:
        ball_vel[0] = random.randrange(120, 240) / 60
    elif direction == LEFT:
        ball_vel[0] = -random.randrange(120, 240) / 60


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2, count  # these are ints
    
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    count = 0
    
    spawn_ball(RIGHT)
    

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
    
    if ball_pos[1] < BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    if ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    ball = canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    # draw paddles
    paddle1 = canvas.draw_line([WIDTH - HALF_PAD_WIDTH,paddle1_pos + HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH,paddle1_pos - HALF_PAD_HEIGHT],8, "Yellow")
    paddle2 = canvas.draw_line([HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [HALF_PAD_WIDTH,paddle2_pos - HALF_PAD_HEIGHT],8, "Yellow")
   
    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    if paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
       
    if paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    if paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    
    # determine whether paddle and ball collide  
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if (ball_pos[1] <= (paddle1_pos - HALF_PAD_HEIGHT)) or (ball_pos[1] >= (paddle1_pos + HALF_PAD_HEIGHT)):
            spawn_ball(LEFT)
            score1 += 1
        else:
            '''rebounce velocity is 1.1 times original velocity'''
            ball_vel[0] = - ball_vel[0] * 1.1
            
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if (ball_pos[1] <= (paddle2_pos - HALF_PAD_HEIGHT)) or (ball_pos[1] >= (paddle2_pos + HALF_PAD_HEIGHT)):
            spawn_ball(RIGHT)
            score2 += 1
        else:
            '''rebounce velocity is 1.1 times original velocity'''
            ball_vel[0] = - ball_vel[0] * 1.1
    
    # draw scores
    if score1 > score2:
        canvas.draw_text(str(score1), (120, 200), 80, "Green")
        canvas.draw_text(str(score2), (420, 200), 80, "Red")
    elif score1 < score2:
        canvas.draw_text(str(score1), (120, 200), 80, "Red")
        canvas.draw_text(str(score2), (420, 200), 80, "Green")
    else:
        canvas.draw_text(str(score1), (120, 200), 80, "Green")
        canvas.draw_text(str(score2), (420, 200), 80, "Green")
                
    # draw instructions
    canvas.draw_text("'w' moves up and 's' moves down", (50,380), 12, "White")
    canvas.draw_text("'up' moves up and 'down' moves down", (330,380), 12, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    acc = 5
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel -= acc
    elif key == simplegui.KEY_MAP['down']:
        paddle1_vel += acc
    elif key == simplegui.KEY_MAP['w']:
        paddle2_vel -= acc
    elif key == simplegui.KEY_MAP['s']:
        paddle2_vel += acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['up']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['down']:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP['w']:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP['s']:
        paddle2_vel = 0

def draw_pre(canvas):
    
    global count, displayed
    
    if count == 0 and displayed:
        canvas.draw_text("3",(280, HEIGHT / 2), 80, "White")
    elif count == 1 and displayed:
        canvas.draw_text("2",(280, HEIGHT / 2), 80, "White")
    elif count == 2 and displayed:
        canvas.draw_text("1",(280, HEIGHT / 2), 80, "White")
    elif count == 3 and displayed:
        canvas.draw_text("Ready Go!",(120, HEIGHT / 2), 80, "White")
    elif count > 3:
        draw(canvas)
        
               
def timer_handler():
    global displayed, count
    #displayed = not displayed
    if displayed:
        count += 1
        
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw_pre)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

#frame.add_button("Start", new_game, 150)
frame.add_button("Restart", new_game, 150)

timer = simplegui.create_timer(timer_interval, timer_handler)

# start frame
new_game()
frame.start()
timer.start()
