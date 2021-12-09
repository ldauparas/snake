# Imports and dependencies
from typing import NoReturn
import pygame
import math
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Snake(pygame.sprite.Sprite):
    def __init__(self, starting_position):
        super(Snake, self).__init__()
        self.surf = []
        self.rect = []
        self.direction = []
        # Able to determine screen dimensions from this
        # TODO: turn this into x and y coords
        self.starting_position = starting_position
        self.speed = 21
        self.body_size = 21

        self.init_block()
        self.add_block()
        self.add_block()
        self.add_block()

    def init_block(self):
        # SURFACE
        new_surface = pygame.Surface((self.body_size, self.body_size))
        new_surface.fill((0, 255, 0))
        self.surf.append(new_surface)

        # RECT
        new_rect = new_surface.get_rect(
            center = (
                self.starting_position
            )
        )
        self.rect.append(new_rect)

        # DIRECTION
        self.direction.append(pygame.Vector2(self.speed, 0))

    def add_block(self):
        # Do stuff
        last_body_index = len(self.surf) - 1
        last_rect = self.rect[last_body_index]
        last_direction = self.direction[last_body_index]

        # SURFACE
        new_surface = pygame.Surface((self.body_size, self.body_size))
        new_surface.fill((0, 255, 0))
        self.surf.append(new_surface)

        # RECT
        new_rect = new_surface.get_rect(
            center = (
                last_rect.centerx + (self.body_size * last_direction.normalize()[0] * -1),
                last_rect.centery + (self.body_size * last_direction.normalize()[1] * -1),
            )
        )
        self.rect.append(new_rect)

        # DIRECTION
        self.direction.append(last_direction)

    def has_collided_w_self(self):
        # Check if head has collided with any rects in body
        pass

        # Return true or false so event can be handled at game loop
        return(False)

    def update(self, pressed_keys):

        new_direction = pygame.math.Vector2(0, 0)
        current_direction = self.direction[0]

        # Handle player event
        if pressed_keys[K_UP]:
            new_direction = pygame.math.Vector2(0, -self.speed)
        if pressed_keys[K_DOWN]:
            new_direction = pygame.math.Vector2(0, self.speed)
        if pressed_keys[K_LEFT]:
            new_direction = pygame.math.Vector2(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            new_direction = pygame.math.Vector2(self.speed, 0)

        # When there is a new direction; change head of snake
        # Do not change direction if its opposite of current direction
        if ((new_direction[0] != float(0)) | (new_direction[1] != float(0))) & (new_direction != (current_direction * -1)):
            self.direction[0] = new_direction

        # Move each part of body
        for i in range(len(self.rect)):

            # Create references to each rect and vector
            body_rect = self.rect[i]
            body_direction = self.direction[i]

            # Handle going off screen
            if body_rect.centerx < 0:
                body_rect.centerx = self.starting_position[0] * 2 - 1
            if body_rect.centerx > self.starting_position[0] * 2:
                body_rect.centerx = 0
            if body_rect.centery < 0:
                body_rect.centery = self.starting_position[1] * 2 - 1
            if body_rect.centery > self.starting_position[1] * 2:
                body_rect.centery = 0

            # Move the snake
            body_rect.move_ip(body_direction)

        # Shift entire direction list
        body_direction_copy = self.direction.copy()

        self.direction.pop(len(body_direction_copy) - 1)
        self.direction.insert(0, body_direction_copy[0])


class Apple(pygame.sprite.Sprite):
    def __init__(self, screen_size):
        super(Apple, self).__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(1, screen_size[0]),
                random.randint(1, screen_size[1]),
            )
        )


# Define main program
def main():

    # important game-state variables
    running = True
    SCREEN_HEIGHT = 600
    SCREEN_WIDTH = 800

    # Initialize pygame
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Snake((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    all_sprites = pygame.sprite.Group()
    apple_group = pygame.sprite.Group()
    all_sprites.add(player)

    while running:

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        screen.fill((0, 0, 0))

        # If no apples, add one
        if len(apple_group) == 0:
            new_apple = Apple((SCREEN_WIDTH, SCREEN_HEIGHT))
            apple_group.add(new_apple)

        # Draw player to screen
        for i in range(len(player.surf)):
            screen.blit(player.surf[i], player.rect[i])
        
        # Draw Apples
        for apple in apple_group:
            screen.blit(apple.surf, apple.rect)
        
        # If snake collides with apple, remove and extend snake
        for apple in apple_group:
            if apple.rect.collidelist(player.rect) != -1:
                apple.kill()
                player.add_block()

        pygame.display.flip()

        clock.tick(25)

    pygame.quit()


# Run the game
main()
