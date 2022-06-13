import pygame
from pygame import PixelArray
from pygame import Color
import random

class Dragon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.speed = 0
        self.frames = self.generate_frames()
        self.delete = False
        self.y = self.rect.y
        self.points = 0




    def generate_frames(self):
        dragon1 = pygame.image.load("images/Dragon1.png").convert_alpha()
        dragon1 = pygame.transform.rotozoom(dragon1, 0, 1)
        dragon2 = pygame.image.load("images/dragon2.png").convert_alpha()
        dragon2 = pygame.transform.rotozoom(dragon2, 0, 1)


        dragon3 = pygame.image.load("images/dragon_3.png").convert_alpha()
        dragon3 = pygame.transform.rotozoom(dragon3, 0, 1)

        color = self.generate_color()

        dragon1.fill(color, special_flags=pygame.BLEND_RGB_ADD)
        dragon2.fill(color, special_flags=pygame.BLEND_RGB_ADD)
        dragon3.fill(color, special_flags=pygame.BLEND_RGB_ADD)

        self.image = dragon1

        self.generate_height()

        self.speed = self.generate_speed()
        return [dragon3, dragon1, dragon2]

    def generate_height(self):
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(2000, 2500)
        self.rect.y = random.randint(60, 910)

    def generate_color(self):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)
        alpha = 50

        return (red,green,blue,alpha)



    def generate_speed(self):
        return random.randint(1, 3)


    def animation(self):
        self.index += 0.09
        if self.index >= len(self.frames):
            self.index = 0

        if int(self.index) ==0:
            self.rect.y = self.y -50
        else:self.rect.y = self.y
        self.image = self.frames[int(self.index)]

    def move(self):
        self.rect.x -= self.speed

    def destroy(self, laser):
        if self.rect.x <= -200 or self.delete:
            self.kill()
        if pygame.sprite.spritecollide(self, laser, False):
            self.points = 50


    def update(self, laser):
        self.animation()
        self.move()
        self.destroy(laser)

    def return_score(self):
        score = self.points
        if self.points == 50:
            self.delete = True
            self.points = 0
        return score

class Laser(pygame.sprite.Sprite):
    def __init__(self, x_value, y_value):
        super().__init__()
        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (12, 70))

        self.image = pygame.transform.rotozoom(self.image, 0, .5)
        self.image = pygame.transform.rotate(self.image, -90)
        self.image.fill((0, 120, 135, 50), special_flags=pygame.BLEND_RGB_ADD)

        self.rect = self.image.get_rect(topleft=(x_value + 150, y_value))



    def update(self):
        self.move()
        self.destroy()

    def move(self):
        self.rect.x += 15

    def destroy(self):
        if self.rect.x >= 2000:
            self.kill()



class Plane(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("images/Plane.png")
        self.rect = self.image.get_rect(center = (400,400))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if self.rect.x - 5 > 0:
                self.rect.x -= 10
            else:
                self.rect.x = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.rect.x + 5 < 1810:
                self.rect.x += 10
            else:
                self.rect.x = 1810
        if keys[pygame.K_UP]:
            if self.rect.y - 10 > 5:
                self.rect.y -= 10
            else:self.rect.y = 5
        if keys[pygame.K_DOWN]:
            if self.rect.y + 10 < 905:
                self.rect.y += 10
            else: self.rect.y = 905

    def update(self):
        self.move()

    def player_colided(self, dragon):
        if dragon:
            if pygame.sprite.spritecollide(self, dragon, False):
                return False
        return True

    def reset(self):
        self.rect = self.image.get_rect(center = (400,400))

