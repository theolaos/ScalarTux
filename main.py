import os, sys
# ensuring support for conversion to an .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

import pygame
from tleng2 import Camera, GlobalSettings, GlobalProperties
# from tleng2.utils.debug import debug_print

pygame.init()

GlobalSettings.update_bresolution((1280,720))
GlobalProperties.load_display()
GlobalSettings._debug = False

camera = Camera()
camera_movement_map = [1,-1,-1,1]

VEL = 20

class ObjectMovement():
    def __init__(self,):
        self.direction = pygame.math.Vector2(0,0)

    def keyboard_nm(self, 
            movement_map:tuple[int, int, int, int] = [1,-1,-1,1]
        ) -> pygame.math.Vector2:
        
        """
        Normal WASD control.
        :param movement_map: Is how much should the vector move to that keystroke
                Moevement map keys are stored as, [right, left, up, down]
        :return: It returns the normalized directional vector.
        """

        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_d]: # right
            self.direction.x += movement_map[0]

        if keys_pressed[pygame.K_a]: # left
            self.direction.x += movement_map[1]

        if keys_pressed[pygame.K_w]: # up
            self.direction.y += movement_map[2] 

        if keys_pressed[pygame.K_s]: # down
            self.direction.y += movement_map[3]  

        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction.normalize()

        self.direction.x = 0
        self.direction.y = 0

        return self.direction

dt = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    GlobalProperties.fill_display((200,255,200))
    GlobalProperties.update_window()

    pygame.display.update()
    dt = GlobalProperties._clock.tick(144) / 1000