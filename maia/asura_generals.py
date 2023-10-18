import pygame, sys
from pygame.locals import *

class IntegerContainer():
    def __init__(self):
        self.x = 0
        self.y = 0

class DefaultAssets(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
        	self.nothing = pygame.image.load("asura_generals/nothing.png")
