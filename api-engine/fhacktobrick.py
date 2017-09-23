from game import Ball, Brick, Cursor, Life, GameEngine
from math import floor

# Add brick line in the screen
def add_lines_brick(n, resistance, width_screen):
    tmp_bricks = []
    # Use it just to get the brick width
    template = Brick(3, 0, 0)
    # Compute the leap between each brick
    leap_width = template.width+5
    leap_height = template.width+5
    # for each line asked
    for line in range(0, n):
        # Fill line by brick separate by leap_width
        for column in range(0, floor(width_screen/leap_width)):
            tmp_bricks.append(Brick(resistance, 5+column*leap_width, 5+line*leap_height))
    
    # return array of brick to display
    return tmp_bricks


# Detect wall, return 'left', 'right', 'top', 'bottom' or 'none' if ball doesn't touch
def detect_wall(element):
    if element.x <= 0:
        return 'left'

    if element.y <= 0:
        return 'top'

    if (element.x+element.width) >= width_screen:
        return 'right'

    if (element.y+element.height) >= height_screen:
        return 'bottom'

    return 'none'


# Compute the next cursor position according to key pressed
def compute_cursor(key_pressed):
    if key_pressed == 'right':
        cursor.dx = 4
    if key_pressed == 'left':
        cursor.dx = -4
    if key_pressed == 'none':
        cursor.dx = 0
    
    # Avoid cursor to disapear at left
    if cursor.x <= 0:
        cursor.x = 0

    # Avoir cursor to disapear at right
    if (cursor.x + cursor.width) >= width_screen:
        cursor.x = width_screen - cursor.width

# Change by speed according what side ball is touched
def change_ball_speed(touches):
    if 'top' in touches or 'bottom' in touches:
        ball.dy = -ball.dy

    if 'right' in touches or 'left' in touches:
        ball.dx = -ball.dx


# Compute the next position element for each frame
def compute_game(ball, cursor, bricks, lifes, key_pressed):
    # Array containing all ball touches
    touches = []
    # Detect wall
    touch = detect_wall(ball)
    # If ball touch bottom of screen, delete one life
    if touch == 'bottom':
        lifes = lifes[:-1]
    touches.append(touch)
    # Detect cursor
    touches.append(ball.touched_side(cursor))

    # Detect each brick
    for brick in bricks:
        touch = ball.touched_side(brick)
        touches.append(touch)
        # if ball touch brick, then kick brick
        if touch != 'none':
            brick.increment_kicks()
    
    # keep only brick alive
    bricks = [brick for brick in bricks if brick.is_alive()]

    # Change speed by accoriding to touches array
    change_ball_speed(touches)
    # Get the new position cursor
    compute_cursor(key_pressed)

    return ball, cursor, bricks, lifes

# Use it to determine the main program, RESPECT THE SYNTAX
if __name__ == '__main__':
    width_screen = 600
    height_screen = 600
    # Enable graphics engine
    engine = GameEngine(width_screen, height_screen)

    # Create ball
    ball = Ball(width_screen/2, height_screen-200)
    ball.dx = -6
    ball.dy = -3
    
    # Create cursor
    cursor = Cursor(width_screen/2, height_screen-30)
    # Create Bricks
    bricks = add_lines_brick(2, 3, width_screen)
    # Create lifes
    lifes = [Life(5, height_screen-100),
             Life(50, height_screen-100),
             Life(100, height_screen-100)]
    print(bricks)
    
    # Main loop for graphics
    while len(bricks) > 0 and len(lifes) > 0:
        # We need this for technical reason
        engine.handle_events()
        # Get the key pressed
        key_pressed = engine.get_key_pressed()
        # Compute the new element to display
        ball, cursor, bricks, lifes = compute_game(ball, cursor, bricks, lifes, key_pressed)
        # Render new element in screen
        engine.render([ball, cursor] + bricks + lifes)
