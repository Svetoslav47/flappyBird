from random import randrange
from time import sleep, time
import pygame
import os

pygame.font.init()

WIDTH, HEIGHT = 228*2, 1024
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

font = pygame.font.SysFont(None, 50)


WHITE = (255, 255, 255)

FPS = 60

BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird1.png"))), pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("assets", "bird3.png")))]
PIPE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "base.png")))
BG_IMAGE = pygame.transform.scale2x(
    pygame.image.load(os.path.join("assets", "bg.png")))

BASE_WIDTH = BASE_IMAGE.get_width()
BASE_HIGHT = BASE_IMAGE.get_height()

BIRD_WIDTH = BIRD_IMAGES[0].get_width()
BIRD_HEIGHT = BIRD_IMAGES[0].get_height()

GRAVITY = 0.3

class Bird():
    def __init__(self, x, y, images, jump_strenght, max_speed, max_fall_speed):
        self.x = x
        self.y = y
        self.velocity = 1
        self.images = images
        self.jump_strenght = jump_strenght
        self.max_speed = max_speed
        self.max_fall_speed = max_fall_speed 
        self.score = 0
        self.animation_state = 0
        self.last_animation_change = time()
        self.animation_speed = 0.1

    def draw(self):
        WIN.blit(self.images[self.animation_state], (self.x, self.y))

    def move(self):
        if(self.last_animation_change + self.animation_speed < time()):
            self.animation_state += 1
            self.last_animation_change = time()
            if self.animation_state > len(self.images)-1:
                self.animation_state = 0

        self.y += self.velocity
        self.velocity += GRAVITY
        if self.velocity < -self.max_speed:
            self.velocity = -self.max_speed

        if self.velocity > self.max_fall_speed:
            self.velocity = self.max_fall_speed

    def jump(self):
        self.velocity -= self.jump_strenght


class Base():
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self):
        WIN.blit(self.image, (self.x, self.y))

    def move(self):
        self.x -= self.speed


class Pipe():
    def __init__(self, image, x, hole_height, speed):
        self.image = image
        self.image_flipped = pygame.transform.rotate(image, 180)
        self.hole_height = hole_height
        self.x = x
        self.min_y = HEIGHT-BASE_HIGHT-self.image.get_height()*2-self.hole_height
        self.max_y = 0
        self.y = randrange(self.min_y, self.max_y)
        self.speed = speed
        self.has_given_point = False

    def draw(self):
        WIN.blit(self.image_flipped, (self.x, self.y))
        WIN.blit(
            self.image, (self.x, (self.y + self.hole_height + self.image.get_height())))

    def move(self):
        self.x -= self.speed

    def move_hole(self):
        self.y = randrange(self.min_y, self.max_y)

    def give_score(self, bird):
        if(bird.x > (self.x + BIRD_WIDTH/2) and self.has_given_point == False):
            self.has_given_point = True
            bird.score += 1

    def collide_with_bird(self, bird):
        if((bird.x+BIRD_WIDTH > self.x) and (bird.x < (self.x + self.image.get_width()))):
            if((bird.y < (self.y + self.image.get_height())) or (bird.y > (self.y + self.image.get_height() + self.hole_height))):
                return True
        return False


def draw(bases, bird, pipes):
    WIN.blit(BG_IMAGE, (0, 0))

    for pipe in pipes:
        pipe.draw()

    for base in bases:
        base.draw()

    score_text = font.render(f"Score: {bird.score}", 1, "black")
    WIN.blit(score_text, (10, 10))
    bird.draw()
    pygame.display.update()


def is_colliding(bird):
    if (bird.y < 0) or (bird.y > HEIGHT - BASE_HIGHT - BIRD_HEIGHT):
        return True
    return False

def gameOver():
    text = font.render("Game Over", 1, "black")
    WIN.blit(text,  (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    sleep(3)
    


def main():
    clock = pygame.time.Clock()
    run = True
    bases = []
    number_of_bases = 2
    world_move_speed = 2

    pipes = []
    distance_between_pipes = 300
    number_of_pipes = 3
    pipe_hole_hight = 175

    for i in range(number_of_bases):
        bases.append(Base(BASE_IMAGE, BASE_WIDTH*i,
                     HEIGHT-BASE_HIGHT, world_move_speed))

    for i in range(number_of_pipes):
        pipes.append(Pipe(PIPE_IMAGE, WIDTH + ((PIPE_IMAGE.get_width() +
                     distance_between_pipes)*i), pipe_hole_hight, world_move_speed))

    bird = Bird(50, ((HEIGHT-BASE_HIGHT)/2 - BIRD_HEIGHT/2),
                BIRD_IMAGES, 10, 10, 5)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        for base in bases:
            base.move()
            if (base.x <= -BASE_WIDTH):
                base.x += BASE_WIDTH*number_of_bases

        bird.move()
        for pipe in pipes:
            pipe.move()
            pipe.give_score(bird)
            if(pipe.collide_with_bird(bird)):
                run = False
                gameOver()
            if (pipe.x < (0-PIPE_IMAGE.get_width())):
                pipe.has_given_point = False
                pipe.x = pipe.x + \
                    ((PIPE_IMAGE.get_width() + distance_between_pipes)*number_of_pipes)
                pipe.move_hole()

        draw(bases, bird, pipes)

        if is_colliding(bird):
            run = False
            gameOver()

    pygame.quit()


if __name__ == "__main__":
    main()
    