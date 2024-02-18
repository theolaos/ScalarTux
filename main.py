import os, sys
# ensuring support for conversion to an .exe (PyInstaller)
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

import pygame
from tleng2 import *
from tleng2.utils.debug import DebugTags
from tleng2.utils.colors import RED, BLACK
# from tleng2.utils.debug import debug_print

pygame.init()

DebugTags.import_tags(['Coordinates', "Collision"])

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
        self.tux_player = Entity(700,100,20,20,"PLAYER")
        self.tux_player.hitbox.set_outline(5, RED)

        self.tux_movement = ObjectMovement()
        self.forces_tux = pygame.math.Vector2(0,0)
        self.move_tux =  pygame.math.Vector2(0,0)
        self.final_move = pygame.math.Vector2(0,0)

        self.TUX_VEL = 16

        self.tux_player.anim_service.current_anim = "images"
        self.tux_player.anim_service.current_image_anim = "default_surf"

        self.floor = Area(100,400,200,200,BLACK)
        self.floor2 = Area(600,400,200,200,BLACK)

        self.list_tiles = [self.floor,self.floor2]

        self.GRAVITY = 0.8

        self.on_ground = False
    

    def event_handling(self,keys_pressed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.tux_movement.keyboard_nm(keys_pressed=keys_pressed)


    def horizontal_collision_static(self, list_tiles, rect, move_x):
        temp_rect = rect.copy()
        temp_rect.x += move_x

        for tile in list_tiles:

            if tile.colliderect(temp_rect):
                debug_print("collided with floor on x", tags=["Collision"])
                if move_x > 0:
                    return tile.rect.left
                elif move_x < 0:
                    return tile.rect.right + rect.left
            else:
                # self.tux_player.new_hitbox_left(self.tux_player.core_x + self.final_move.x)
                debug_print("updating x", self.tux_player.core_x, tags=["Collision"])
                self.on_ground = False
                return move_x


    def horizontal_collision(self):
        temp_rect = self.tux_player.hitbox.rect.copy() 
        temp_rect.x += self.final_move.x
        collision = False
        debug_print("horizontal collision",temp_rect, tags=['Collision'])

        #tile = self.floor
        for tile in self.list_tiles:

            if tile.rect.colliderect(temp_rect):
                print(tile.rect, "collided")
                debug_print("collided with floor on x", tags=["Collision"])
                collision = True
                if self.final_move.x > 0:
                    self.tux_player.new_hitbox_right(tile.rect.left)

                elif self.final_move.x < 0:
                    self.tux_player.new_hitbox_left(tile.rect.right)

        if collision != True:
            self.tux_player.core_x += self.final_move.x
            self.on_ground = False



    def vertical_collision(self):
        temp_rect = self.tux_player.hitbox.rect.copy()
        temp_rect.y += self.final_move.y
        collision = False

        debug_print("vertical collision",temp_rect, tags=['Collision'])
        # if self.floor.rect.collidepoint(self.tux_player.core_x, self.tux_player.core_y + self.tux_player.get_hitbox_height() + self.final_move.y):
        # tile = self.floor
        for tile in self.list_tiles:

            if tile.rect.colliderect(temp_rect):
                debug_print(tile.rect, "collided", tags=['Collision'])
                debug_print("collided with floor on y", tags=["Collision"])
                collision = True
                if self.final_move.y > 0:
                    self.tux_player.new_hitbox_bottom(tile.rect.top)
                    self.move_tux.y = 0
                    self.forces_tux.y = 0
                    self.on_ground = True

                elif self.final_move.y < 0:
                    self.tux_player.new_hitbox_top(tile.rect.bottom)
                    self.move_tux.y = 0
                    self.forces_tux.y = 0

        if collision != True:
            self.tux_player.core_y += self.final_move.y
            self.on_ground = False


    def update(self):
        self.forces_tux.y += 0.5
        if self.tux_movement.direction.y < -0.5 and self.on_ground:
            self.forces_tux.y += -9

        # self.horizontal_collision()
        # self.vertical_collision()
        self.move_tux += self.forces_tux

        # forces movement (accelaration)
        self.final_move.x +=  (self.move_tux.x + self.tux_movement.direction.x * self.TUX_VEL)
        self.final_move.y += (1* self.move_tux.y)

        debug_print("Starting Debug _______",tags=['Coordinates'])
        debug_print("key direction", self.tux_movement.direction, tags=['Coordinates'])
        debug_print("move", self.move_tux,tags=['Coordinates'])
        debug_print("forces", self.forces_tux,tags=['Coordinates'])
        debug_print("Coords PLH", self.tux_player.hitbox.rect ,tags=['Coordinates'])
        debug_print("Coords PL ", self.tux_player.core_x, self.tux_player.core_y ,tags=['Coordinates'])
        debug_print("final_move", self.final_move ,tags=['Coordinates'])
        debug_print("on_ground", self.on_ground ,tags=['Coordinates'])
        
        
        # self.tux_player.core_y += self.tux_movement.direction.y * self.TUX_VEL * GlobalProperties._dt
        # list_tiles = [self.floor.rect,self.floor2.rect]
        # self.tux_player.new_hitbox_left(self.horizontal_collision(list_tiles, self.tux_player.hitbox.rect))
        # self.tux_player.new_hitbox_top(self.vertical_collision())

        self.horizontal_collision()
        self.vertical_collision()

        
        self.forces_tux.x = 0
        self.forces_tux.y = 0
        self.final_move.x = 0
        self.final_move.y = 0

        # self.tux_player.update()
        self.tux_player.update_area()


    def render(self):
        GlobalProperties.fill_display((200,255,200))
        # self.tux_player.hitbox.render()
        self.tux_player.anim_service.anim_dict["images"]["default_surf"].fill(RED)
        self.tux_player.render()
        self.floor.render()
        self.floor2.render()
        #self.tux_player.hitbox.render_outline()  
        #print("%.2f %.2f" % (self.tux_player.core_x , self.tux_player.core_y))
        
        debug_print("render from menu done", tags=["Rendering"])

        

class ObjectMovement():
    def __init__(self,):
        self.direction = pygame.math.Vector2(0,0)

    def keyboard_nm(self, 
            keys_pressed:tuple,
            movement_map:tuple[int, int, int, int] = (1,-1,-1,1),
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

        if keys_pressed[pygame.K_SPACE]: # up
            self.direction.y += movement_map[2] 

        if self.direction.x != 0 and self.direction.y != 0:
            self.direction = self.direction.normalize()

        return self.direction
    
if __name__ == '__main__':
    menu = Menu('menu')
    SM = SceneManager()
    SM.current_scene = 'menu'
    while True:
        SM.render_current_scene()
        # debug_print(SceneCatcher.scenes, tags=["Rendering"])


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