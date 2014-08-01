# Implementation of classic arcade game Pong

import simplegui
import random
import math

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
paddle1_pos = HEIGHT/2
paddle2_pos = HEIGHT/2
paddle1_vel = 0
paddle2_vel = 0


ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [1,1]
time = 0
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel,time # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    time = 1
    
    if direction:
        ball_vel = [1,-1]
    
    else:
        ball_vel = [-1,-1]
    
        
def tick():
    global time
    time += 1

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global LEFT,RIGHT
    spawn_ball(RIGHT)
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel,time
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
        
    # update ball
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[0] *= 1
        ball_vel[1] *= -1
        
    if ball_pos[1] >= HEIGHT-BALL_RADIUS:
        ball_vel[0] *= 1
        ball_vel[1] *= -1
    
    if ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS) and ball_pos[1] >= paddle1_pos and ball_pos[1] <= (paddle1_pos+80):
        ball_vel[0] *= -1
        ball_vel[1] *= 1
        
    if ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS ) and ball_pos[1] >= paddle2_pos and ball_pos[1] <= (paddle2_pos+80):
        ball_vel[0] *= -1
        ball_vel[1] *= 1
        
    ball_pos[0] += time * ball_vel[0]
    ball_pos[1] += time * ball_vel[1]
    
    if ball_pos[0] <= PAD_WIDTH:
        if not(ball_pos[1] >= paddle1_pos and ball_pos[1] <= (paddle1_pos+80)):
            score2+=1
            spawn_ball(RIGHT)
            
    if ball_pos[0] >= WIDTH - PAD_WIDTH:
        if not(ball_pos[1] >= paddle2_pos and ball_pos[1] <= (paddle2_pos+80)):
            score1+=1
            spawn_ball(LEFT)

            
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,2,"Blue","White")
    # update paddle's vertical position, keep paddle on the screen
    
    canvas.draw_line([0,paddle1_pos],[0,80+paddle1_pos],16,"Yellow")
    canvas.draw_line([596,paddle2_pos],[596,80+paddle2_pos],8,"Yellow")
    
    canvas.draw_text(str(score1),[130,235],95,"Blue")
    canvas.draw_text(str(score2),[430,235],95,"Blue")
    
def button1():
    new_game()
    
    
        
def keydown(key):
    global paddle1_vel, paddle2_vel,paddle1_pos,paddle2_pos
    if key == simplegui.KEY_MAP["up"]:
        if paddle2_pos != 0:
            paddle2_vel += 10
            paddle2_pos -= 40
    elif key == simplegui.KEY_MAP["down"]:
        if paddle2_pos != 320:
            paddle2_vel += 10
            paddle2_pos += 40
    elif key == simplegui.KEY_MAP["w"]:
        if paddle1_pos != 0:
            paddle1_vel += 10
            paddle1_pos -= 40
    elif key == simplegui.KEY_MAP["s"]:
        if paddle1_pos != 320:
            paddle1_vel += 10
            paddle1_pos += 40
        
def keyup(key):
    global paddle1_vel, paddle2_vel

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button = frame.add_button("Reset",button1)

timer = simplegui.create_timer(4000,tick)


# start frame
new_game()
frame.start()
timer.start()
