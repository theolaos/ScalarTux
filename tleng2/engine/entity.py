from .area import Area
from ..services.animation import LazyAnimationService
from ..services.image import ImageService
from ..services.sound import SoundService
from ..utils.settings import GlobalSettings
from ..utils.colors import RED
import pygame

class EntityCatcher:
    entity_in_scene = {}

    def __init__(self, scene_key):
        self.entity_in_scene.update({scene_key:[self]})



class Entity:
    def __init__(
            self,
            x: int | float, 
            y: int | float,  
            width: int | float, 
            height: int | float, 
            entity_type: str, 
            anim_service_name: str = "LAS"
        ) -> None:

        """
        :param anim_service_name: It's an experimental feature that is designed to hopefully 
                                  make the programmer easily assign anim_services to the entity. 
                                  The default is LAS (LazyAnimationService).
        
                                  - LAS : LazyAnimationService
                                  - IS  : ImageService (static image)
                                  - FAS : FancyAnimationService (not implemented yet)
        
        :return: It returns Nothing (None)
        """

        self.core_x = x
        self.core_y = y
        self.core_width = width
        self.core_height = height
        self.hitbox = Area(x=x, y=y, width=width, height=height)
        #self.set_outline(1,RED)

        self.anim_service_name = anim_service_name
        if anim_service_name == "LAS":
            self.anim_service = LazyAnimationService()
        elif anim_service_name == "IS":
            self.anim_service = ImageService()

        self.anim_service.anim_dict.update({"images":
                                            {"default_surf": pygame.Surface((50,50))}
                                            })
        # self.sound_service = SoundService('')
        self.entity_type = entity_type

    def load_animation(self, 
            anim_dict: dict
        )-> None:
        try:
            self.anim_service.import_animation(anim_dict=anim_dict)
        except Exception as e:
            raise Exception(f"You tried to load an animation while having the current animation_service: {self.anim_service_name}. \nAdditional Error messages{e}")

    def new_hitbox(self, hitbox_width : float, hitbox_height : float) -> None: # TODO : hitbox/coordination system
        '''
        It makes a new hitbox (it changes the width and the height of the hitbox, which is a Rect)
        :param hitbox_width: The new number of the new hitbox width (either a flot or an int)
        :param hitbox_height: The new number of the new hitbox height (either a flot or an int)
        :return: it returns nothing
        '''
        #change the hitbox of the outer box
        self.rect.width, self.rect.height = hitbox_width, hitbox_height
        self.rect.x, self.rect.y = self.coreX - self.rect.width/2, self.coreY - self.rect.height/2


    def update(self) -> None:
        '''
        It updates everything without the need of the programmer to type out every function of the entity.
        '''
        self.anim_service.update()
        self.hitbox.update()
    

    def render(self) -> None:
        if GlobalSettings._debug:
            self.hitbox.render_outline()

        self.anim_service.render()

    def update_area(self) -> None:
        self.hitbox.core_x = self.core_x
        self.hitbox.core_y = self.core_y
        self.hitbox.core_width = self.core_width
        self.hitbox.core_height = self.core_height

        # self.hitbox.round_update()
        self.hitbox.update()
