import os, sys
# ensuring support for conversion to an .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

import pygame
from tleng2 import Camera, GlobalSettings, GlobalProperties, Entity, Scene, SceneManager, SceneCatcher, debug_print
from tleng2.utils.debug import DebugTags
from tleng2.utils.colors import RED
# from tleng2.utils.debug import debug_print

pygame.init()

DebugTags.import_tags(['Rendering'])

GlobalSettings.update_bresolution((1280,720))
GlobalProperties.load_display()
GlobalProperties.set_caption("ScalarTux")

GlobalSettings._debug = True
GlobalSettings.load_settings_json()

camera = Camera()
camera_movement_map = [1,-1,-1,1]

# tux_player = Entity(100,100,20,20,"PLAYER")
# tux_player.hitbox.set_outline(5, RED)
# TUX_VEL = 20

class Menu(Scene):
    def __init__(self, scene_name):
        super().__init__(scene_name)
        self.tux_player = Entity(100,100,20,20,"PLAYER")
        self.tux_player.hitbox.set_outline(5, RED)
        self.tux_movement = ObjectMovement()
        self.TUX_VEL = 100
        self.tux_player.anim_service.current_anim = "images"
        self.tux_player.anim_service.current_image_anim = "default_surf"
    
    def event_handling(self,keys_pressed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.tux_movement.keyboard_nm(keys_pressed=keys_pressed)


    def update(self):
        self.tux_player.core_x += self.tux_movement.direction.x * self.TUX_VEL * GlobalProperties._dt
        self.tux_player.core_y += self.tux_movement.direction.y * self.TUX_VEL * GlobalProperties._dt        
        # self.tux_player.update()
        self.tux_player.update_area()


    def render(self):
        GlobalProperties.fill_display((200,255,200))
        # self.tux_player.hitbox.render()
        self.tux_player.anim_service.anim_dict["images"]["default_surf"].fill(RED)
        self.tux_player.render()
        #self.tux_player.hitbox.render_outline()  
        #print("%.2f %.2f" % (self.tux_player.core_x , self.tux_player.core_y))
        
        debug_print("render from menu done", tags=["Rendering"])

        

class ObjectMovement():
    def __init__(self,):
        self.direction = pygame.math.Vector2(0,0)

    def keyboard_nm(self, 
            movement_map:tuple[int, int, int, int] = [1,-1,-1,1],
            keys_pressed:tuple = None
        ) -> pygame.math.Vector2:
        
        """
        Normal WASD control.
        :param movement_map: Is how much should the vector move to that keystroke
                Moevement map keys are stored as, [right, left, up, down]
        :keys_pressed: if you have already assigned a variable with all keys pressed just pass it in, to not re-assign a new variable. 
        :return: It returns the normalized directional vector.
        """
        if keys_pressed != None:
            keys_pressed = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

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

        return self.direction
    
if __name__ == '__main__':
    menu = Menu('menu')
    SM = SceneManager()
    SM.current_scene = 'menu'
    while True:
        SM.render_current_scene()
        debug_print(SceneCatcher.scenes, tags=["Rendering"])


# dt = 0

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
    
#     GlobalProperties.fill_display((200,255,200))
#     # tux_player.render()
#     tux_player.hitbox.render()
#     tux_player.hitbox.render_outline()

#     GlobalProperties.update_window()

#     pygame.display.update()
#     dt = GlobalProperties._clock.tick(144) / 1000