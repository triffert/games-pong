import random
import sys
import pygame

pygame.font.init()

# define global parameters
MAX_Y = 450
MAX_X = 800
SCREEN = pygame.display.set_mode((MAX_X, MAX_Y))
pygame.display.set_caption("Till's Pong Game")

# define style
GAME_FONT = 'Arial'
GAME_FONT_SIZE_SMALL = 30
GAME_FONT_SIZE_MEDIUM = 50
GAME_FONT_SIZE_HUGE = 90

PADDING = 10
LINE_WIDTH = 10
LINE_WIDTH_THIN = 5
DASH_LENGTH = 20
PADDLE_LENGTH = 50
PADDLE_X_POS = 30
BALL_RADIUS = 7
END_SCORE = 10

# define colors
BORDER_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)
PADDLE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)
BALL_COLOR = (255, 255, 255)

# define physics
FRAMES_PER_SECOND = 60
PADDLE_VELOCITY = 5
BALL_VELOCITY = 5


class Player:

    def __init__(self, x, y=None, score=0, velocity=PADDLE_VELOCITY, length=PADDLE_LENGTH):
        self.x = x
        self.y = (MAX_Y - length) / 2 if y is None else y
        self.length = length
        self.score = score
        self.velocity = velocity

    def draw(self):
        pygame.draw.line(surface=SCREEN, color=PADDLE_COLOR, width=LINE_WIDTH,
                         start_pos=(self.x, self.y), end_pos=(self.x, self.y + PADDLE_LENGTH))

    def move_up(self):
        if self.y - self.velocity >= PADDING + LINE_WIDTH:
            self.y -= self.velocity

    def move_down(self):
        if self.y + self.velocity + self.length <= MAX_Y - PADDING - LINE_WIDTH:
            self.y += self.velocity


class Ball:

    def __init__(self, x, y, dx=1.0, color=BALL_COLOR):
        self.x = self.start_x = x
        self.y = self.start_y = y
        self.dx = dx
        self.dy = 0
        self.spin = 0.0
        self.color = color
        self.velocity = BALL_VELOCITY
        self.radius = BALL_RADIUS

    def move(self):
        self.x += self.velocity * self.dx
        self.y += self.velocity * self.dy

    def draw(self):
        pygame.draw.circle(surface=SCREEN, color=BALL_COLOR,
                           center=(self.x, self.y), radius=BALL_RADIUS)

    def restart(self, dx):
        self.dx = dx
        self.dy = 0
        self.velocity = BALL_VELOCITY
        self.spin = 0.0
        self.x = self.start_x
        self.y = self.start_y


def draw_dashed_vertical_line(x, y, color=BORDER_COLOR, width=LINE_WIDTH_THIN,
                              dash_length=DASH_LENGTH, max_length=MAX_Y - PADDING):
    while y < MAX_Y:
        pygame.draw.line(surface=SCREEN, color=color, width=width,
                         start_pos=(x, y), end_pos=(x, min(y + dash_length, max_length)))
        y += 2 * dash_length


def wait_for_key():
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return


def run_pong():
    run = True
    clock = pygame.time.Clock()

    player_left = Player(x=PADDLE_X_POS)
    player_right = Player(x=MAX_X - PADDLE_X_POS)
    ball = Ball(x=MAX_X / 2, y=MAX_Y / 2, dx=random.choice([-1, 1]))

    score_font = pygame.font.SysFont(GAME_FONT, GAME_FONT_SIZE_SMALL)
    game_over_font = pygame.font.SysFont(GAME_FONT, GAME_FONT_SIZE_HUGE)
    game_start_font = pygame.font.SysFont(GAME_FONT, GAME_FONT_SIZE_MEDIUM)

    def colide_wall():
        if ball.y + ball.radius >= MAX_Y - PADDING - LINE_WIDTH:
            ball.dy = -abs(ball.dy)
        if ball.y - ball.radius <= PADDING + LINE_WIDTH:
            ball.dy = abs(ball.dy)

    def colide_players():
        if (player_left.x - ball.radius <= ball.x <= player_left.x + LINE_WIDTH + ball.radius
                and player_left.y - ball.radius <= ball.y <= player_left.y + PADDLE_LENGTH + ball.radius):
            ball.dx = abs(ball.dx)
            ball.dy = -BALL_VELOCITY / PADDLE_LENGTH/2 * (ball.y - player_left.y - PADDLE_LENGTH / 2)
        if (player_right.x - LINE_WIDTH - ball.radius <= ball.x <= player_right.x + ball.radius
                and player_right.y - ball.radius <= ball.y <= player_right.y + PADDLE_LENGTH + ball.radius):
            ball.dx = -abs(ball.dx)
            ball.dy = -BALL_VELOCITY / PADDLE_LENGTH/2 * (ball.y - player_right.y - PADDLE_LENGTH / 2)

    def redraw_elements():
        SCREEN.fill(BACKGROUND_COLOR)
        pygame.draw.rect(surface=SCREEN, color=BORDER_COLOR,
                         rect=(0, PADDING, MAX_X, LINE_WIDTH))
        pygame.draw.rect(surface=SCREEN, color=BORDER_COLOR,
                         rect=(0, MAX_Y - PADDING - LINE_WIDTH, MAX_X, LINE_WIDTH))
        draw_dashed_vertical_line(x=MAX_X / 2, y=PADDING,
                                  max_length=MAX_Y - PADDING, width=LINE_WIDTH_THIN)
        score_label = score_font.render(f"{player_left.score}   {player_right.score}", True, TEXT_COLOR)
        SCREEN.blit(source=score_label,
                    dest=((MAX_X - score_label.get_width()) / 2, PADDING + LINE_WIDTH + PADDING))

        player_left.draw()
        player_right.draw()
        ball.draw()
        pygame.display.update()

    def game_over():
        if player_left.score >= END_SCORE or player_right.score >= END_SCORE:
            game_over_label = game_over_font.render(f"GAME OVER", True, TEXT_COLOR)
            SCREEN.blit(source=game_over_label,
                        dest=((MAX_X - game_over_label.get_width()) / 2,
                              (MAX_Y - game_over_label.get_height()) / 2))
            pygame.display.update()
            wait_for_key()
            return True
        else:
            return False

    redraw_elements()
    game_start_label = game_start_font.render(f"Press any key to start", True, TEXT_COLOR)
    SCREEN.blit(source=game_start_label,
                dest=((MAX_X - game_start_label.get_width()) / 2,
                      (MAX_Y - game_start_label.get_height()) / 2))
    pygame.display.update()
    wait_for_key()

    while run:
        clock.tick(FRAMES_PER_SECOND)
        colide_wall()
        colide_players()
        ball.move()

        if ball.x <= 0 or ball.x >= MAX_X:
            if ball.x <= 0:
                player_right.score += 1
                direction = -1
            else:
                player_left.score += 1
                direction = 1
            redraw_elements()
            run = not game_over()
            if run:
                # TODO COUNTDOWN
                ball.restart(dx=direction)
        else:
            redraw_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_left.move_up()
        if keys[pygame.K_s]:
            player_left.move_down()
        if keys[pygame.K_UP]:
            player_right.move_up()
        if keys[pygame.K_DOWN]:
            player_right.move_down()


def main():
    run = True
    while run:
        run_pong()


if __name__ == '__main__':
    main()
