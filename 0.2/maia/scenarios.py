import pygame, sys
from pygame.locals import *
from asura_generals import *
             
class Scenario(pygame.sprite.Sprite):
	def __init__(self, screenx, screeny):
		pygame.sprite.Sprite.__init__(self)
        	self.bg = None
		self.screendimms = IntegerContainer()
		self.screendimms.x = screenx
		self.screendimms.y = screeny
		self.camera = Camera(0, 0+self.screendimms.x, 0, 0+self.screendimms.y)
		self.objs = [ ]
		self.chs = [ ]
		self.layers = 0

	def set_bg(self, png):
		self.bg = png

	def repos_camera(self, x, y):
		self.camera.limizq = x
		self.camera.limder = x + self.screendimms.x
		self.camera.limsup = y
		self.camera.liminf = y + self.screendimms.y
	
	def move_camera(self, x, y):
		self.camera.limizq = self.camera.limizq + x
		if self.camera.limizq < 0:
			self.camera.limizq = 0
		if (self.camera.limizq + self.screendimms.x) > self.bg.get_width():
			self.camera.limizq = self.camera.limizq - x
		self.camera.limder = self.camera.limizq + self.screendimms.x

		self.camera.limsup = self.camera.limsup + y
		if self.camera.limsup < 0:
			self.camera.limsup = 0
		if (self.camera.limsup + self.screendimms.y) > self.bg.get_height():
			self.camera.limsup = self.camera.limsup - y
		self.camera.liminf = self.camera.limsup + self.screendimms.y

	def direct_camera(self, director, x, y, ts):
		check_left = director.rect.centerx
		check_right = self.screendimms.x - director.rect.centerx
		check_top = director.rect.centery
		check_bottom = self.screendimms.y - director.rect.centery

		if check_left <= ts:
			self.move_camera(-x, 0)

		if check_right <= ts:
			self.move_camera(x, 0)

		if check_top <= ts:
			self.move_camera(0, -y)

		if check_bottom <= ts:
			self.move_camera(0, y)

	def legislate(self):
		for obj in self.objs:
			obj.update(self.screendimms.x, self.screendimms.y, self.camera.limder, self.camera.liminf)
		for ch in self.chs:
			ch.update(self.screendimms.x, self.screendimms.y, self.camera.limder, self.camera.liminf)
			ch.prohibited_zones = [ ]
			for obj in self.objs:
				ch.prohibited_zones.append(obj.ironwall)                                   
	
	def draw(self, screen):
		bg_area = (self.camera.limizq, self.camera.limsup, self.camera.limder, self.camera.liminf)
		screen.blit(self.bg, (0,0), bg_area)
		count = 1
		while count <= self.layers:
                        for obj in self.objs:
                                for drawingoption in obj.drawingoptions:
                                        area = drawingoption[0]
                                        layer = drawingoption[1]
                                        if layer == count:
                                                screen.blit(obj.png, obj.rect_correction(area), area)
                        for ch in self.chs:
                                for drawingoption in ch.drawingoptions:
                                        area = drawingoption[0]
                                        layer = drawingoption[1]
                                        if layer == count:
                                                screen.blit(ch.png, ch.rect_correction(area), area)


                        count = count + 1                        
	
	def add_obj(self, obj):
		self.objs.append(obj)

	def add_ch(self, ch):
		self.chs.append(ch)

	def layering(self, layers):
                self.layers = layers

	def create_layer(self):
		self.layers = self.layers + 1
		
class Camera():
        def __init__(self, limizq, limder, limsup, liminf):
		self.limizq = limizq
		self.limder = limder
		self.limsup = limsup
		self.liminf = liminf
		
class LimitBox():
	def __init__(self, limizq, limder, limsup, liminf, plus):
		self.limizq = limizq
		self.limder = limder
		self.limsup = limsup
		self.liminf = liminf
		if isinstance(plus, tuple):
                        self.plus = plus
                else:
                        self.plus = (plus, plus, plus, plus)
		

	def update(self, limizq, limder, limsup, liminf):
		self.limizq = limizq
		self.limder = limder
		self.limsup = limsup
		self.liminf = liminf

	def calculate_pnglimits_update(self, x, y, png):
                self.limizq = x - int(float( png.get_width() ) / float( 2 ) ) - self.plus[0]
		self.limder = x + int(float( png.get_width() ) / float( 2 ) ) + self.plus[1]
		self.limsup = y - int(float( png.get_height() ) / float( 2 ) ) - self.plus[2]
		self.liminf = y + int(float( png.get_height() ) / float( 2 ) ) + self.plus[3]

class Character(pygame.sprite.Sprite):
	def __init__(self, png, bgx, bgy):
		pygame.sprite.Sprite.__init__(self)
		self.png = png
		self.png_backup = png
		self.drawingoptions = [ ]
		self.animate = False
		self.framing = -1
		if self.png == None:
			self.rect = None
		else:
			self.rect = self.png.get_rect()
		self.bgx = bgx
		self.bgy = bgy
		self.prohibited_zones = [ ]
	
	def repos(self, x, y):
		if not self.animation:
			self.rect.centerx = x
			self.rect.centery = y
		if self.animation:
			for rect in self.rectarray:
				rect.centerx = x
				rect.centery = y

	def move(self, x, y):
		self.bgx = self.bgx + x
		self.bgy = self.bgy + y
		for zone in self.prohibited_zones:
			if self.is_in(zone):
				self.bgx = self.bgx - x
				self.bgy = self.bgy - y

	def update(self, screenx, screeny, camera_limder, camera_liminf):
		self.rect.centerx = screenx - (camera_limder - self.bgx)
		self.rect.centery = screeny - (camera_liminf - self.bgy)

	def rect_correction(self, new_values):
                if new_values <> None:
                        new_rect = self.rect.copy()
                        new_rect.centerx = new_rect.centerx + new_values[0]
                        new_rect.centery = new_rect.centery + new_values[1]
                        return new_rect
                else:
                        return self.rect
                
	def is_in(self, limobj):
		if self.bgx > limobj.limizq and self.bgx < limobj.limder and self.bgy > limobj.limsup and self.bgy < limobj.liminf:
			return True
		else:
			return False
				

	def set_png(self, png):
		self.png = png
		self.png_backup = png
		self.rect = self.png.get_rect()

	def set_animation(self, pngarray):
		self.pngarray = pngarray
		self.rectarray = [ ]
		for png in self.pngarray:
			self.rectarray.append(png.get_rect())
		self.animation = True

	def set_png_backup(self, png):
		self.png_backup = png

	def start_animation(self):
		self.animate = True

	def stop_animation(self):
		self.animate = False

	def animation(self, pngarray, asura_frames):
		if self.animate:
			self.framing = self.framing + 1
			for png in pngarray:
				index = pngarray.index(png)
				if self.framing == asura_frames[index]:
					self.png = png
					self.rect = png.get_rect()
			if self.framing == asura_frames[len(asura_frames) - 1]:
				self.framing = -1
				return True

	def resetpng_check(self):
		if self.animate == False:
			self.png = self.png_backup
			self.rect = self.png_backup.get_rect()

	def resetpng(self):
		self.png = self.png_backup
		self.rect = self.png_backup.get_rect()

	def add_drawingoption(self, area, fate):
                self.drawingoptions.append([area, fate])
                
	def reset_drawingoptions(self):
		self.drawingoptions = [ ]
		

class Obj(pygame.sprite.Sprite):
	def __init__(self, png, bgx, bgy, collplus):
		pygame.sprite.Sprite.__init__(self)
		self.png = png
		self.drawingoptions = [ ]
		if self.png == None:
			self.rect = None
		else:
			self.rect = self.png.get_rect()
		self.bgx = bgx
		self.bgy = bgy
		self.ironwall = LimitBox(0, 0, 0, 0, collplus)
		self.ironwall.calculate_pnglimits_update(self.bgx, self.bgy, self.png)
		self.interactbox = None

	def update(self, screenx, screeny, camera_limder, camera_liminf):
		self.rect.centerx = screenx - (camera_limder - self.bgx)
		self.rect.centery = screeny - (camera_liminf - self.bgy)                        

        def rect_correction(self, new_values):
                if new_values <> None:
                        new_rect = self.rect.copy()
                        new_rect.centerx = new_rect.centerx + new_values[0]
                        new_rect.centery = new_rect.centery + new_values[1]
                        return new_rect
                else:
                        return self.rect

	def set_png(self, png):
		if self.rect <> None:
			centerx = self.rect.centerx
			centery = self.rect.centery
		self.png = png
		self.rect = self.png.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery
                # Bug cuando self.rect = None ?

	def set_collplus(self, collplus_tuple):
		self.ironwall.plus = collplus_tuple
		self.ironwall.calculate_pnglimits_update(self.bgx, self.bgy, self.png)

	def add_drawingoption(self, area, fate):
                self.drawingoptions.append([area, fate])

	def reset_drawingoptions(self):
		self.drawingoptions = [ ]

	def create_interactbox(self, boxplus):
                self.interactbox = LimitBox(0, 0, 0, 0, boxplus)
                self.interactbox.calculate_pnglimits_update(self.bgx, self.bgy, self.png)

        def check_interactbox(self, ch):
                if self.interactbox <> None:
                        if ch.is_in(self.interactbox):
                                return True
				
