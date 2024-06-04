import pygame
import random


def game():
    # starting pygame
    pygame.init()

    # settings of game
    fps = 75
    clock = pygame.time.Clock()
    bird_x = 50
    bird_y = 200
    keys = pygame.key.get_pressed()
    behind_border = 100
    distance_pipes = 0

    list_pipes = []
    # colors
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    # screen
    width = 500
    height = 400
    screen = pygame.display.set_mode((width, height))

    # images
    bird_images = [pygame.image.load("img/bird_down.png"),
                   pygame.image.load("img/bird_mid.png"),
                   pygame.image.load("img/bird_up.png")]
    sky_image = pygame.image.load('img/background.png')
    sky_image = pygame.transform.scale(sky_image, (width, height))
    ground_image = pygame.image.load('img/ground.png')
    pipe_top_image = pygame.image.load('img/tube1.png')

    pipe_bottom_image = pygame.image.load('img/tube2.png')
    game_over_image = pygame.image.load('img/game_over.png')
    start_image = pygame.image.load('img/start.png')

    # start 
    start_rect = start_image.get_rect()
    start_rect.width = 176
    start_rect.height = 77
    start_rect.x = width // 2 - start_rect.width // 2
    start_rect.y = height // 2 - start_rect.height // 2

    # game_over
    game_over_rect = game_over_image.get_rect()
    game_over_rect.width = 192
    game_over_rect.height = 71
    game_over_rect.x = width // 2 - game_over_rect.width // 2
    game_over_rect.y = height // 2 - game_over_rect.height // 2

    # score 
    font = pygame.font.SysFont('impact', 40)
    score = 0
    score_text = font.render(f'Score: {score}', True,
                             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    score_text_rect = score_text.get_rect()
    score_text_rect.x = 20
    score_text_rect.y = 20

    class Bird():
        def __init__(self):
            self.image = bird_images[0]
            self.rect = self.image.get_rect()
            self.rect.width = 34
            self.rect.height = 24
            self.rect.x = bird_x
            self.rect.y = bird_y
            self.image_index = 0
            self.fall = 0
            self.jump = False

        def update(self):
            # animating bird
            self.image_index += 1
            if self.image_index >= 30:
                self.image_index = 0
            self.image = bird_images[self.image_index // 10]

            # bird padaet

            self.fall += 0.1
            if self.fall > 3:
                self.fall = 3
            self.rect.y += self.fall
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and self.jump == False and self.rect.y >= 0:
                self.jump = True
                self.fall = -3
                self.jump = False

    bird = Bird()

    class Ground():
        def __init__(self):
            self.image1 = ground_image
            self.image2 = ground_image
            self.rect1 = self.image1.get_rect()
            self.rect1.width = 551
            self.rect1.height = 219
            self.rect2 = self.image2.get_rect()
            self.rect2.width = 551
            self.rect2.height = 219
            self.rect1.x = 0
            self.rect1.y = height - self.rect1.height // 20
            self.rect2.x = width
            self.rect2.y = height - self.rect1.height // 20
            self.ground_index = 0

        def update(self):
            self.ground_index -= 1
            self.rect1.x = self.ground_index
            self.rect1.y = height - self.rect1.height // 20
            self.rect2.x = width + self.ground_index
            self.rect2.y = height - self.rect1.height // 20
            if self.rect1.x == -width:
                self.ground_index = 0

    ground = Ground()

    class Pipe():
        def __init__(self):
            self.image_top = pipe_top_image

            self.image_bottom = pipe_bottom_image

            # Rects widths heights

            self.rect_top = self.image_top.get_rect()
            self.rect_top.width = 52
            self.rect_top.height = 320

            self.rect_bottom = self.image_bottom.get_rect()
            self.rect_bottom.width = 52
            self.rect_bottom.height = 320

            # x y rects
            randomy = random.randint(-90, 75)
            self.rect_top.x = 300 + behind_border + distance_pipes
            self.rect_top.y = -150 + randomy

            self.rect_bottom.x = 300 + behind_border + distance_pipes
            self.rect_bottom.y = 275 + randomy

        def update(self):
            self.rect_top.x -= 1
            self.rect_bottom.x -= 1

            if self.rect_top.x <= -100:
                randomy = random.randint(-90, 75)
                self.rect_top.x = 300 + behind_border + 500
                self.rect_top.y = -150 + randomy

                self.rect_bottom.x = 300 + behind_border + 500
                self.rect_bottom.y = 275 + randomy

    for _ in range(5):
        pipe = Pipe()
        list_pipes.append(pipe)
        distance_pipes += 200

    def quit_game():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lets_continue = False
                pygame.quit()

    def main():

        font = pygame.font.SysFont('impact', 40)

        score = 0
        score_text = font.render(f'Score: {score}', True,
                                 (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        score_text_rect = score_text.get_rect()
        score_text_rect.x = 20
        score_text_rect.y = 20

        start()

        lets_continue = True

        while lets_continue:
            # quit game

            quit_game()

            screen.fill(BLACK)

            # backround
            screen.blit(sky_image, sky_image.get_rect())

            # ground
            ground.update()
            screen.blit(ground.image1, ground.rect1)
            screen.blit(ground.image2, ground.rect2)

            # bird
            bird.update()
            screen.blit(bird.image, bird.rect)

            # pipes

            for pipe in list_pipes:
                pipe.update()

                if (pipe.rect_bottom.colliderect(bird.rect) or pipe.rect_top.colliderect(bird.rect)) or (
                        ground.rect1.colliderect(bird.rect) or ground.rect2.colliderect(bird.rect)):
                    global loose_score
                    loose_score = score

                    game_over()
                if bird.rect.x == pipe.rect_top.x + pipe.rect_top.width:
                    score += 1
                    score_text = font.render(f'Score: {score}', True,
                                             (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                screen.blit(pipe.image_top, pipe.rect_top)
                screen.blit(pipe.image_bottom, pipe.rect_bottom)
            screen.blit(score_text, score_text_rect)
            clock.tick(fps)
            pygame.display.update()

    def start():

        start = True

        while start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start = False
                if event.type == pygame.QUIT:
                    start = False
                    lets_continue = False
                    loose = False
            screen.blit(sky_image, sky_image.get_rect())
            screen.blit(ground.image1, ground.rect1)
            screen.blit(ground.image2, ground.rect2)
            screen.blit(start_image, start_rect)
            screen.blit(bird.image, bird.rect)

            clock.tick(fps)
            pygame.display.update()

    def game_over():
        score_text = font.render(f'Score: {loose_score}', True,
                                 (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        louse_pause = True
        while louse_pause:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game()
                if event.type == pygame.QUIT:
                    lets_continue = False
                    start = False
                    loose = False

            screen.blit(sky_image, sky_image.get_rect())
            screen.blit(ground.image1, ground.rect1)
            screen.blit(ground.image2, ground.rect2)
            screen.blit(bird.image, bird.rect)

            for pipe in list_pipes:
                screen.blit(pipe.image_top, pipe.rect_top)
                screen.blit(pipe.image_bottom, pipe.rect_bottom)
            screen.blit(game_over_image, game_over_rect)
            screen.blit(score_text, score_text_rect)

            clock.tick(fps)
            pygame.display.update()

    main()
game()
