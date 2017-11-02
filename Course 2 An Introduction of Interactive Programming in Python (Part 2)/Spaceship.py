# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
acc = [0, 0]
rock_group = set([])
missile_group = set([])
explosion_group = set([])
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + 90,self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
            
        self.angle += self.angle_vel
        
        # velocity update - acceleration in forward direction
        acc = angle_to_vector(self.angle)
        
        if self.thrust:
            self.vel[0] += 0.2 * acc[0]
            self.vel[1] += 0.2 * acc[1]
        else:
            self.vel[0] -= 0.1 * self.vel[0]
            self.vel[1] -= 0.1 * self.vel[1]
 
    def update_thrust(self,thrust):
        self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()   
        else:
            ship_thrust_sound.pause()
    
    def left_angle_vel(self):
        self.angle_vel -= 0.1
        
    def right_angle_vel(self):
        self.angle_vel += 0.1
        
    def shoot(self):
        global missile_group
        
        acc = angle_to_vector(self.angle)
        missile_vel = [self.vel[0] + 8 * acc[0], self.vel[1] + 8 * acc[1]]
        missile_pos = [self.pos[0] + self.radius * acc[0], self.pos[1] + self.radius * acc[1]]
        
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def get_radius(self):
        return self.radius        
        
    def draw(self, canvas):
        # canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        
        # canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

        if self.animated:
            center = (self.image_center[0] + self.age * self.image_size[0], self.image_center[1])
            canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)


    def update(self):
        if started:
            
            # Update angle
            self.angle += self.angle_vel
        
            # Update position, and keep the sprite always in the canvas
            self.pos[0] += self.vel[0]
            self.pos[0] = self.pos[0] % WIDTH
        
            self.pos[1] += self.vel[1]      
            self.pos[1] = self.pos[1] % HEIGHT

            #update age
            self.age += 1
        
            if self.age < self.lifespan:
                return True
            else:
                return False
        
    def collide(self, other_object):
        total_radius = self.radius + other_object.get_radius()
        total_distance = dist(self.get_position(), other_object.get_position())
        
        if total_radius >= total_distance:
            return True
        else:
            return False

        
# Key handlers

def keydown(key):
    if key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    if key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(True)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.left_angle_vel()  
    if key == simplegui.KEY_MAP["right"]:
        my_ship.right_angle_vel()

def keyup(key):
    if key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(False)
    if key == simplegui.KEY_MAP["left"]:
        my_ship.right_angle_vel()  
    if key == simplegui.KEY_MAP["right"]:
        my_ship.left_angle_vel()
    
# Collide functions

def group_collide(object_group, other_object):
    is_collide = False
    remove_object = set([])
    for obj in object_group:
        if obj.collide(other_object):
            is_collide = True
            remove_object.add(obj)
            a_explosion = Sprite(other_object.get_position(), [0, 0], other_object.angle, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(a_explosion)

    object_group.difference_update(remove_object)
    return is_collide        

def group_group_collide(one_group, other_group):
    num_collide = 0
    for obj in one_group:
        if group_collide(other_group, obj):
            one_group.discard(obj)
            num_collide += 1
    return num_collide

def process_object_group(object_group, canvas):
    for obj in object_group:
        if obj.update():
            obj.draw(canvas)
        else:
            object_group.discard(obj)

def game_start():
    global lives, score, rock_group, missile_group, explosion_group, started
    
    score = 0
    lives = 3
    rock_group = set([])
    missile_group = set([])
    explosion_group = set([])
    started = False
    soundtrack.rewind()
    ship_thrust_sound.rewind()
    missile_sound.rewind()
    explosion_sound.rewind()
    

    
def click_to_start(position):
    global started
    upper_left_pos = [WIDTH / 2 - splash_info.get_size()[0] / 2, HEIGHT / 2 - splash_info.get_size()[1] / 2] 
    below_right_pos = [WIDTH / 2 + splash_info.get_size()[0] / 2, HEIGHT / 2 + splash_info.get_size()[1] / 2]
    if (position[0] < below_right_pos[0]) and (position[0] > upper_left_pos[0]) and (position[1] < below_right_pos[1]) and (position[1] > upper_left_pos[1]) and not started:
        started = True
        soundtrack.rewind()
        soundtrack.play()
            
def draw(canvas):
    global time, rock_group, missile_group, explosion_group, lives, score, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    canvas.draw_text("Lives: " + str(lives), [(WIDTH / 20), HEIGHT / 15], 30, "White")
    canvas.draw_text("Score: " + str(score), [(WIDTH / 20) * 15, HEIGHT / 15], 30, "White")
    
    #a_rock.draw(canvas)
    #a_missile.draw(canvas)
    
    if started:
        process_object_group(rock_group, canvas)
        process_object_group(missile_group, canvas)
        process_object_group(explosion_group, canvas)
    
        if group_collide(rock_group, my_ship):
            lives -= 1
        
        if lives <= 0:
            game_start()
        
        score += group_group_collide(rock_group, missile_group) * 10
     
    else:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), (WIDTH / 2, HEIGHT / 2), splash_info.get_size())
    
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
    #a_missile.update()
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    if len(rock_group) <= 5: # maximum 5 rocks in the screen
        rock_pos = [random.randint(0, WIDTH - 1), random.randint(0 , HEIGHT - 1)]
        rock_vel = [random.choice([random.randrange(1, 2), -random.randrange(1,2)]), random.choice([random.randrange(1, 2), -random.randrange(1, 2)])]
        rock_ang = 0
        rock_ang_vel = random.choice([random.randrange(5, 10, 1) / 100.0])
        
        a_rock = Sprite(rock_pos, rock_vel, rock_ang, rock_ang_vel, asteroid_image, asteroid_info)
        rock_group.add(a_rock)
   
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click_to_start)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()