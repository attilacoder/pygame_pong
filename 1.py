import pygame, sys, random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
c = pygame.time.Clock()

def move_ball():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= w_size[1]:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1
    if ball.left <= 0:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= w_size[0]:
        player_score += 1
        score_time = pygame.time.get_ticks()
def move_player(up, down):
    if up:
        speed = -7
    elif down:
        speed = 7
    else:
        speed = 0
    if player.top <= 0:
        player.top = 0
    if player.bottom >= w_size[1]:
        player.bottom = w_size[1]
    return speed
def move_opponent():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= w_size[1]:
        opponent.bottom = w_size[1]
def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (w_size[0]/2, w_size[1]/2)
    if current_time - score_time < 700:
        number_three = font.render("3", False, light_grey)
        w.blit(number_three, (w_size[0]/2 - 10, w_size[1]/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = font.render("2", False, light_grey)
        w.blit(number_two, (w_size[0]/2 - 10, w_size[1]/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = font.render("1", False, light_grey)
        w.blit(number_one, (w_size[0]/2 - 10, w_size[1]/2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_x = 7 * random.choice((1,-1))
        ball_speed_y = 7 * random.choice((1,-1))
        score_time = None


w_size = [1280,960]
w = pygame.display.set_mode(w_size)
pygame.display.set_caption('Pong')

ball = pygame.Rect(w_size[0]/2-15,w_size[1]/2-15,30,30)
player = pygame.Rect(10,w_size[1]/2 - 70, 10,140)
opponent = pygame.Rect(w_size[0] - 20, w_size[1]/2 - 70, 10, 140)

bg_color = pygame.Color('grey12')
light_grey = (200,200,200)

ball_speed_x = 7
ball_speed_y = 7
player_speed = 0
opponent_speed = 7
up = False
down = False


player_score = 0
opponent_score = 0
font = pygame.font.Font("freesansbold.ttf", 32)

score_time = True
current_time = None

pong_sound = pygame.mixer.Sound("pong.wav")


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up = True
            if event.key == pygame.K_s:
                down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                up = False
            if event.key == pygame.K_s:
                down = False




    move_ball()
    player_speed = move_player(up,down)
    move_opponent()
    player.y += player_speed
    if ball.colliderect(player) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - player.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
    if ball.colliderect(opponent) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - opponent.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    w.fill(bg_color)
    pygame.draw.rect(w,light_grey, player)
    pygame.draw.rect(w, light_grey, opponent)
    pygame.draw.ellipse(w, light_grey, ball)
    pygame.draw.aaline(w,light_grey, (w_size[0]/2, 0), (w_size[0]/2, w_size[1]))

    if score_time:
        ball_restart()

    player_text = font.render(f"{player_score}", False, light_grey)
    w.blit(player_text, (600, 470))
    opponent_text = font.render(f"{opponent_score}", False, light_grey)
    w.blit(opponent_text, (660, 470))

    pygame.display.flip()
    c.tick(60)
