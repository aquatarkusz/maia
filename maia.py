# ------------------------------------------------------
# Maia 0.1 (Asura Early Release)
# ------------------------------------------------------
# Early versions of menus.py, sound.py and other scripts 
# of Asura Engine
# ------------------------------------------------------

import pygame, sys
from pygame.locals import *

class Audio():
    def __init__(self, path):
        self.path = path
        self.pygame_sound_object = None

    def trymixer(self):
        try:
            self.pygame_sound_object = pygame.mixer.Sound(self.path)
        except:
            self.pygame_sound_object = None

    def play(self):
        if self.pygame_sound_object == None:
            self.trymixer()
            if self.pygame_sound_object <> None:
                self.pygame_sound_object.play()
        else:
            self.pygame_sound_object.play()

class EmptySurface():
    def __init__(self, height, width):
        self.height = height
        self.width = width

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

class Empty():
    def __init__(self, png):
        self.png = png
        self.alt_png = None
        self.fx = None

    def set_png(self, png):
        self.png = png

    def alter_png(self, png):
        self.alt_png = png

class Option():
    def __init__(self, png):
        self.png = png
        self.alt_png = None
        self.status = 0
        self.fx = None

    def set_png(self, png):
        self.png = png

    def alter_png(self, png):
        self.alt_png = png

    def set_fx(self, soundobj):
        self.fx = soundobj

    def play_fx(self):
        if isinstance(self.fx, Audio):
            self.fx.play()

    def press(self):
        if self.status == 0:
            self.status = 1
        elif self.status == 1:
            self.status = 0

class Pointer():
    def __init__(self):
        self.png = None
        self.relative_pos_x = None
        self.relative_pos_y = None
        self.calc_from_opposite = False
        self.alterselection = False
        self.h_pos = 0
        self.v_pos = 0

    def calc_relative_pos(self, current_item_x, current_item_y):
        if not self.calc_from_opposite:
            return (current_item_x - self.png.get_width() + self.relative_pos_x, current_item_y + self.relative_pos_y)
        if self.calc_from_opposite:
            return (current_item_x + menu_item.png.get_width() + self.relative_pos_x, current_item_y + self.relative_pos_y)            

class Menu():
    def __init__(self):
        self.items = [ ]
        self.pointer = Pointer()
        self.x = None
        self.y = None
        self.itemspacing_h = 10
        self.itemspacing_v = 5
        self.fx = None

    def set_pointer_png(self, png):
        self.pointer.png = png

    def set_pointer_options(self, x, y):
        self.pointer.relative_pos_x = x
        self.pointer.relative_pos_y = y

    def set_pointer_alterselection(self):
        self.pointer.alterselection = True

    def set_pointer_position(self, h_pos, v_pos):
        self.pointer.h_pos = h_pos - 1
        self.pointer.v_pos = v_pos - 1

    def set_pointer_h_pos(self, h_pos):
        self.pointer.h_pos = h_pos - 1

    def set_pointer_v_pos(self, v_pos):
        self.pointer.v_pos = v_pos - 1

    def pointer_calc_from_opposite(self):
        self.pointer.calc_from_opposite = True

    def pointer_reset_calc_from_opp(self):
        self.pointer.calc_from_opposite = False

    def set_itemspacing(self, h, v):
        self.itemspacing_h = h
        self.itemspacing_v = v

    def set_itemspacing_h(self, h):
        self.itemspacing_h = h

    def set_itemspacing_v(self, v):
        self.itemspacing_v = v

    def set_noneitem_size(self, x, y):
        self.noneitem_size_x = x
        self.noneitem_size_y = y

    def add_columns(self, number):
        count = 1
        while count <= number:
            self.items.append([])
            count = count + 1

    def add_item(self, item, column):
        self.items[column-1].append(item)

    def column(self, number):
        return self.items[number-1]

    def highest_item_height(self, selected_group):
        the_highest = 0
        for item in selected_group:
            if item.png.get_height() > the_highest:
                the_highest = item.png.get_height()
        return the_highest

    def widest_item_width(self, selected_group):
        the_widest = 0
        for item in selected_group:
            if item.png.get_width() > the_widest:
                the_widest = item.png.get_width()
        return the_widest

    def current_item(self):
        return self.items[self.pointer.h_pos][self.pointer.v_pos]

    def set_fx(self, soundobj):
        self.fx = soundobj

    def play_fx(self):
        if isinstance(self.fx, Audio):
            self.fx.play()
        
    def draw(self, screen, x, y):
        cum_x = x
        cum_y = y
        for column in self.items:
            for item in column:
                if item == self.current_item():
                    if self.pointer.png <> None:
                        screen.blit(self.pointer.png, self.pointer.calc_relative_pos(cum_x, cum_y))
                    if self.pointer.alterselection:
                        if not isinstance(item.alt_png, EmptySurface):
                            screen.blit(item.alt_png, (cum_x, cum_y))
                    else:
                        if not isinstance(item.png, EmptySurface):
                            screen.blit(item.png, (cum_x, cum_y))
                else:
                    if not isinstance(item.png, EmptySurface):
                            screen.blit(item.png, (cum_x, cum_y))
                cum_y = cum_y + item.png.get_height() + self.itemspacing_v
            cum_x = cum_x + self.widest_item_width(column) + self.itemspacing_h
            cum_y = y

    def use(self, navkey_vUP, navkey_vDOWN, navkey_hLEFT, navkey_hRIGHT, navkey_ok):
        if navkey_vUP:
            count = 0
            if self.pointer.v_pos > 0:
                self.pointer.v_pos = self.pointer.v_pos - 1
                count = count + 1
                
            while isinstance(self.current_item(), Empty):
                if self.pointer.v_pos > 0:
                    self.pointer.v_pos = self.pointer.v_pos - 1
                    count = count + 1
                elif self.pointer.v_pos == 0:
                    self.pointer.v_pos = self.pointer.v_pos + count
                    count = 0

            self.play_fx()
                                
        if navkey_vDOWN:
            count = 0
            if self.pointer.v_pos < len(self.items[self.pointer.h_pos])-1:
                self.pointer.v_pos = self.pointer.v_pos + 1
                count = count + 1
                
            while isinstance(self.current_item(), Empty):
                if self.pointer.v_pos < len(self.items[self.pointer.h_pos])-1:
                    self.pointer.v_pos = self.pointer.v_pos + 1
                    count = count + 1
                elif self.pointer.v_pos == len(self.items[self.pointer.h_pos])-1:
                    self.pointer.v_pos = self.pointer.v_pos - count
                    count = 0

            self.play_fx()
                
        if navkey_hLEFT:
            count = 0
            if self.pointer.h_pos > 0:
                self.pointer.h_pos = self.pointer.h_pos - 1
                count = count + 1
                
            while isinstance(self.current_item(), Empty):
                if self.pointer.h_pos > 0:
                    self.pointer.h_pos = self.pointer.h_pos - 1
                    count = count + 1
                elif self.pointer.h_pos == 0:
                    self.pointer.h_pos = self.pointer.h_pos + count
                    count = 0

            self.play_fx()

        if navkey_hRIGHT:
            count = 0
            if self.pointer.h_pos < len(self.items)-1:
                self.pointer.h_pos = self.pointer.h_pos + 1
                count = count + 1
                
            while isinstance(self.current_item(), Empty):
                if self.pointer.h_pos < len(self.items)-1:
                    self.pointer.h_pos = self.pointer.h_pos + 1
                    count = count + 1
                elif self.pointer.h_pos == len(self.items)-1:
                    self.pointer.h_pos = self.pointer.h_pos - count
                    count = 0

            self.play_fx()
                
        if navkey_ok:
            self.current_item().press()
            self.current_item().play_fx()
        
