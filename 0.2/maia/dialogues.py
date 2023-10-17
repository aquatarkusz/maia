import pygame, sys
from pygame.locals import *
from asura_generals import *

class Diagbox(pygame.sprite.Sprite):
    def __init__(self):
	pygame.sprite.Sprite.__init__(self)
        self.png1 = None
        self.face = None
        self.position = IntegerContainer()
        self.text = None
        self.font = None
        self.txt_face = None
        self.txt_position = IntegerContainer()
        self.txt_move_x = 10
        self.txt_move_y = 5
        self.y_checked = True

    def shape(self, png, dimensions):
	x = dimensions[0]
	y = dimensions[1]
	ox = dimensions[2]
	oy = dimensions[3]
	self.png1 = pygame.transform.scale(png, ( int(float(float(png.get_width())/float(ox))*x), int(float(float(png.get_height())/float(oy))*y) ) )

    def with_animation(self, screenx, screeny):
        self.animation = []
	self.frames_fractions = [0.1833, 0.3666, 0.55, 0.7333, 0.9166, 0.825, 1]
        for fraction in self.frames_fractions:
            self.animation.append(pygame.transform.scale(self.png1, (int(self.png1.get_width()*fraction), self.png1.get_height())))

        self.animation_positions_x = []
        for frame_png in self.animation:
            self.animation_positions_x.append((screenx/2)-(frame_png.get_width()/2))

        self.animation_positions_y = []
        for frame_png in self.animation:
            self.animation_positions_y.append(screeny - frame_png.get_height())


        self.face = self.animation
        self.position.x = self.animation_positions_x
        self.position.y = self.animation_positions_y

    def simple(self, screenx, screeny):
        self.face = [self.png1]
        self.position.x = [screenx - self.png1.get_width()]
        self.position.y = [screeny - self.png1.get_height()]

    def set_text(self, font, text, colour, screenx, screeny, separation_x, separation_y, marginal):
        self.txt_anim = [ ]
        self.txt_animation_positions_x = []           
        self.txt_animation_positions_y = []
        
        for word in text:
            render = font.render(word, False, colour)
            self.txt_anim.append(render)
            position_x = screenx - self.png1.get_width()+self.txt_move_x
            self.txt_animation_positions_x.append(position_x)
            position_y =  screeny - self.png1.get_height()+self.txt_move_y
            self.txt_animation_positions_y.append(position_y)
            self.txt_move_x = self.txt_move_x + render.get_width() + separation_x             
            if position_x > screenx - marginal and position_x < screenx:
                self.txt_move_y = self.txt_move_y + render.get_height() + separation_y
                self.txt_move_x = 0
            
        self.txt_face = self.txt_anim
        self.txt_position.x = self.txt_animation_positions_x
        self.txt_position.y = self.txt_animation_positions_y


class Displayer():
	def __init__(self, nothing):
		self.status = "none"
		self.nothing = nothing
		self.frame = -1
		self.queue = []
		self.to_draw = self.nothing
		self.to_draw_position = (0, 0)
		self.asura_frames = [0, 1, 2, 3, 4, 5, 6]
		self.textmove = 5
		self.textpointer = 0
		self.text_to_draw = []
		self.text_to_draw_position = []
		self.surface = pygame.Surface((800, 600), pygame.SRCALPHA)
		self.surface.convert_alpha()
		self.draw = True
		

	def to_draw_reset(self):
		self.to_draw = self.nothing
		self.to_draw_position = (0, 0)

	def to_draw_reset_definitive(self):
            self.surface = pygame.Surface((800, 600), pygame.SRCALPHA)
	    self.surface.convert_alpha()

	def change_status(self, mode, frames):
            self.status =  mode
            self.frame = frames

	def draw_dialogue(self, screen, skip_key):
		self.frame = self.frame + 1
		for display in self.queue[0].face:
			disp_idx = self.queue[0].face.index(display)
			if self.frame == self.asura_frames[disp_idx]:
				self.to_draw = display
				self.to_draw_position = (self.queue[0].position.x[disp_idx], self.queue[0].position.y[disp_idx])
                self.surface.blit(self.to_draw, self.to_draw_position)
		if self.frame > 10:
                    self.change_status("writing", -1)
                    

        def write_dialogue(self, screen, skip_key):
                self.frame = self.frame + 1
                word = self.queue[0].txt_face[self.textpointer]
                position = (self.queue[0].txt_position.x[self.textpointer], self.queue[0].txt_position.y[self.textpointer])
                if self.draw:
                    self.surface.blit(word, position)
                if self.frame % 4 == 0:
                    self.textpointer = self.textpointer + 1
                    self.draw = True
                else:
                    self.draw = False
                if self.textpointer >= len(self.queue[0].txt_face):
                        self.textpointer = 0
                        self.queue[0].txt_face = self.queue[0].txt_anim
                        self.frame = -1
			self.to_draw_reset()
			self.queue.pop(0)
			self.status = "stop"
		if skip_key:
                        self.textpointer = 0
                        self.queue[0].txt_face = self.queue[0].txt_anim
			self.frame = -1
			self.to_draw_reset()
			self.queue.pop(0)
			self.to_draw_reset_definitive()
        		if self.queue == []:
                            self.status = "none"
                        else:
                            self.status = "drawing"
                        self.draw = True

	def stopped(self, screen, skip_key):
            if skip_key:
                self.to_draw_reset_definitive()
		if self.queue == []:
		    self.status = "none"
		else:
                    self.status = "drawing"

        def update_screen(self, screen, skip_key):
		if self.status == "drawing":
		    self.draw_dialogue(screen, skip_key)
		    screen.blit(self.surface, (0,0))
		if self.status == "writing":
                    self.write_dialogue(screen, skip_key)
                    screen.blit(self.surface, (0,0))
                if self.status == "stop":
                    self.stopped(screen, skip_key)
                    screen.blit(self.surface, (0,0))
                    
	def add_dialogue(self, content):
		self.queue.append(content)

class Manager():
	def __init__(self):
		self.assets = DefaultAssets()
		self.displayer = Displayer(self.assets.nothing)
