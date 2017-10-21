# template for "Stopwatch: The Game"

# define global variables
import simplegui

current = 0
clock = "0:00:0"
clock_position = [150, 250]
result_position = [400, 50]
width = 500
height = 500
interval = 100
correct_num = 0
total_num = 0
timer_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    ones = t % 10
    tens = t / 10
    
    seconds = tens % 60
    minutes = tens / 60
    
    if minutes > 100:
        return "Error: Time is ended"
    
    elif seconds >= 10:
        return str(minutes) + ":" + str(seconds) + ":" + str(ones)
    
    elif seconds < 10:
         return str(minutes) + ":0" + str(seconds) + ":" + str(ones)
        
# define event handlers for buttons; "Start", "Stop", "Reset"
def Start():
    timer.start()
    
    global timer_running
    timer_running = True

def Stop():
    timer.stop()
    
    global correct_num
    global total_num
    global current
    global timer_running
    
    if timer_running:
        timer_running = False
        total_num = total_num + 1
        if current % 10 == 0:
            correct_num = correct_num + 1
    
def Reset():
    timer.stop()
    
    global current
    global clock
    global correct_num
    global total_num
    current = 0
    clock = format(current)
    correct_num = 0
    total_num = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global clock
    global current
    current = current + 1
    clock = format(current)

# define draw handler
def draw(canvas):
    canvas.draw_text(clock, clock_position, 72, "Red")
    canvas.draw_text(str(correct_num) + "/" + str(total_num), result_position, 36, "Green")
    
# create frame
frame = simplegui.create_frame("Stopwatch: The Game", width, height)

# register event handlers
frame.add_button("Start", Start, 100)
frame.add_button("Stop", Stop, 100)
frame.add_button("Reset", Reset, 100)

frame.set_draw_handler(draw)

timer = simplegui.create_timer(interval, tick)

# start frame
frame.start()

# Please remember to review the grading rubric
