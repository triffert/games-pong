import pygame

# define global parameters
WINDOW_HEIGHT = 450
WINDOW_WIDTH = 800
FRAMES_PER_SECOND = 60

# define the display mode
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Till's Pong Game")

# define style
PADDING = 10
LINE_WIDTH = 10
LINE_WIDTH_THIN = 5
DASH_LENGTH = 20
PADDLE_LENGTH = 50
PADDLE_X_POS = 30

# define colors
BORDER_COLOR = (200, 200, 200)
PADDLE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

# define physics
PADDLE_VELOCITY = 5


class Player:

    def __init__(self, x, y=None, score=0, velocity=PADDLE_VELOCITY, length=PADDLE_LENGTH):
        self.x = x
        if y is None:
            self.y = (WINDOW_HEIGHT - length)/2
        else:
            self.y = y
        self.length = length
        self.score = score
        self.velocity = velocity

    def draw(self):
        pygame.draw.line(surface=WINDOW, color=PADDLE_COLOR, width=LINE_WIDTH,
                         start_pos=(self.x, self.y), end_pos=(self.x, self.y+PADDLE_LENGTH))

    def move_up(self):
        if self.y - self.velocity >= PADDING + LINE_WIDTH:
            self.y -= self.velocity

    def move_down(self):
        if self.y + self.velocity + self.length <= WINDOW_HEIGHT - PADDING - LINE_WIDTH:
            self.y += self.velocity


def draw_dashed_vertical_line(x, y, color=BORDER_COLOR, width=LINE_WIDTH,
                              dash_length=DASH_LENGTH, max_length=WINDOW_HEIGHT):
    while y < WINDOW_HEIGHT:
        pygame.draw.line(surface=WINDOW, color=color, width=width,
                         start_pos=(x, y), end_pos=(x, min(y+dash_length, max_length)))
        y += 2*dash_length


def main():
    run = True
    clock = pygame.time.Clock()

    player_one = Player(x=PADDLE_X_POS)
    player_two = Player(x=WINDOW_WIDTH - PADDLE_X_POS)

    def redraw_elements():
        WINDOW.fill(BACKGROUND_COLOR)
        pygame.draw.rect(surface=WINDOW, color=BORDER_COLOR,
                         rect=(0, PADDING, WINDOW_WIDTH, LINE_WIDTH))
        pygame.draw.rect(surface=WINDOW, color=BORDER_COLOR,
                         rect=(0, WINDOW_HEIGHT - PADDING - LINE_WIDTH, WINDOW_WIDTH, LINE_WIDTH))
        draw_dashed_vertical_line(x=(WINDOW_WIDTH - LINE_WIDTH) / 2, y=PADDING,
                                  max_length=WINDOW_HEIGHT-PADDING, width=LINE_WIDTH_THIN)
        player_one.draw()
        player_two.draw()
        pygame.display.update()

    while run:
        clock.tick(FRAMES_PER_SECOND)
        redraw_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_one.move_up()
        if keys[pygame.K_s]:
            player_one.move_down()
        if keys[pygame.K_UP]:
            player_two.move_up()
        if keys[pygame.K_DOWN]:
            player_two.move_down()

    pygame.quit()


if __name__ == '__main__':
    main()
