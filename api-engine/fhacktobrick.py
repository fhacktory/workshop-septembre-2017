from game import Ball, Brick, Cursor, Life, GameEngine
from math import floor


def add_lines_brick(n, resistance, width_screen):
    tmp_bricks = []
    template = Brick(3, 0, 0)
    leap_width = template.width+5;
    leap_height = template.width+5;
    for line in range(0, n):
        for column in range(0, floor(width_screen/leap_width)):
            tmp_bricks.append(Brick(resistance, 5+column*leap_width, 5+line*leap_height))

    return tmp_bricks


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


def compute_cursor(key_pressed):
    if key_pressed == 'right':
        cursor.dx = 4
    if key_pressed == 'left':
        cursor.dx = -4
    if key_pressed == 'none':
        cursor.dx = 0

    if cursor.x <= 0:
        cursor.x = 0

    if (cursor.x + cursor.width) >= width_screen:
        cursor.x = width_screen - cursor.width


def change_ball_speed(touches):
    if 'top' in touches or 'bottom' in touches:
        ball.dy = -ball.dy

    if 'right' in touches or 'left' in touches:
        ball.dx = -ball.dx


def compute_game(ball, cursor, bricks, lifes, key_pressed):
    touches = []
    touch = detect_wall(ball)
    if touch == 'bottom':
        lifes = lifes[:-1]
    touches.append(touch)
    touches.append(ball.touched_side(cursor))

    for brick in bricks:
        touch = ball.touched_side(brick)
        touches.append(touch)
        if touch != 'none':
            brick.increment_kicks()

    bricks = [brick for brick in bricks if brick.is_alive()]

    change_ball_speed(touches)
    compute_cursor(key_pressed)

    return ball, cursor, bricks, lifes

if __name__ == '__main__':
    width_screen = 600
    height_screen = 600
    engine = GameEngine(width_screen, height_screen)

    ball = Ball(width_screen/2, height_screen-200)
    ball.dx = -6
    ball.dy = -3

    cursor = Cursor(width_screen/2, height_screen-30)
    bricks = add_lines_brick(2, 3, width_screen)
    lifes = [Life(5, height_screen-100),
             Life(50, height_screen-100),
             Life(100, height_screen-100)]
    print(bricks)

    while len(bricks) > 0 and len(lifes) > 0:
        engine.handle_events()
        key_pressed = engine.get_key_pressed()
        ball, cursor, bricks, lifes = compute_game(ball, cursor, bricks, lifes, key_pressed)
        engine.render([ball, cursor] + bricks + lifes)