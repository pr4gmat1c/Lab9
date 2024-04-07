# Game is paused and not paused when a key "P" is pressed
# When the game is paused, you can press UP and Down arrow keys to change the size of the ball
#  When the game is paused, you can press SPACE and ESCAPE keys to change the size of the paddle
import pygame
import random

pygame.init()

W, H = 1200, 800
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
surface = pygame.Surface((W,H), pygame.SRCALPHA)
clock = pygame.time.Clock()
done = False
bg = (0, 0, 0)

# paddle
paddleW = 150
paddleH = 25
paddleSpeed = 20
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

# Ball
ballRadius = 20
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Game score
game_score = 0
game_score_fonts = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (0, 0, 0))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)

# Catching sound
collision_sound = pygame.mixer.Sound('audio/catch.mp3')


def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    if delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy


# Block settings
block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) for i in range(10) for j in
              range(4)]

# Game over Screen
losefont = pygame.font.SysFont('comicsansms', 40)
losetext = losefont.render(f'Game Over' ' \n Press R to Restart', True, (255, 255, 255))
losetextRect = losetext.get_rect()
losetextRect.center = (W // 2, H // 2)

# Win Screen
winfont = pygame.font.SysFont('comicsansms', 40)
wintext = losefont.render(f'You win yay' '\n Press R to restart', True, (0, 0, 0))
wintextRect = wintext.get_rect()
wintextRect.center = (W // 2, H // 2)

restart_game = False  # Flag to restart the game
paused = False        # Flag to pause the game
settings = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (ball.bottom > H or not len(block_list)):
                # Restart game when S is pressed and the game is over
                block_list = [pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
                color_list = [(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) for i in
                              range(10) for j in range(4)]
                ball.x = W // 2
                ball.y = H // 2
                game_score = 0
                restart_game = True
            elif event.key == pygame.K_p:
                # Pause the game when "p" is pressed
                paused = not paused
            elif event.key == pygame.K_UP and paused:
                # Increase ball size when up arrow key is pressed and the game is paused
                ballRadius += 5
                ball_rect = int(ballRadius * 2 ** 0.5)
                ball = pygame.Rect(ball.x, ball.y, ball_rect, ball_rect)
            elif event.key == pygame.K_DOWN and paused:
                # Decrease ball size when down arrow key is pressed and the game is paused
                ballRadius = max(5, ballRadius - 5)
                ball_rect = int(ballRadius * 2 ** 0.5)
                ball = pygame.Rect(ball.x, ball.y, ball_rect, ball_rect)
            elif event.key == pygame.K_SPACE and paused:
                # Increase paddle size when up space key is pressed and the game is paused
                paddleW += 15
                paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)
            elif event.key == pygame.K_ESCAPE and paused:
                # Decrease paddle size when escape key is pressed and the game is paused
                paddleW -= 15
                paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)


    if restart_game:
        restart_game = False  # Reset restart flag
        continue  # Skip the rest of the loop if restarting the game

    if paused:
        # Fill screen with a transparent white color
        pygame.draw.rect(surface, (128, 128, 128, 150), [0,0,W,H])
        screen.blit(surface, (0,0))
        pause_text = losefont.render(f'Game is paused', True, (0, 0, 0))
        # Display a text that game is paused
        screen.blit(pause_text, pause_text.get_rect(center =(W//2,H//2)))
        pygame.display.flip()

        continue



    screen.fill(bg)
    # Collision left
    [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]  # drawing blocks
    pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle)
    pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ballRadius)
    # print(next(enumerate(block_list)))

    # Ball movement
    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy

    if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
        dx = -dx
    # Collision top
    if ball.centery < ballRadius + 50:
        dy = -dy
    # Collision with paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)


    # Collision blocks
    hitIndex = ball.collidelist(block_list)

    if hitIndex != -1:
        hitRect = block_list.pop(hitIndex)
        hitColor = color_list.pop(hitIndex)
        dx, dy = detect_collision(dx, dy, ball, hitRect)
        game_score += 1
        collision_sound.play()



    # Game score
    game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
    screen.blit(game_score_text, game_score_rect)
    

    # Win/lose screens
    if ball.bottom > H:
        screen.fill((0, 0, 0))
        screen.blit(losetext, losetextRect)
    elif not len(block_list):
        screen.fill((255, 255, 255))
        screen.blit(wintext, wintextRect)

    # Paddle Control
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddleSpeed
    if key[pygame.K_RIGHT] and paddle.right < W:
        paddle.right += paddleSpeed



    pygame.display.flip()
    clock.tick(FPS)
