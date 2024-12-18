from math import pi

from numpy import zeros
from pygame.event import Event
from pygame.surface import Surface

from src.core.collision import polar_angle
from src.core.entity import Camera
from src.core.essentials import FPos, Pos, Scene
from src.game.singletons import GameSettings

from .game_object import GameObject
from .game_objects import MainCharacter


class MainScene(Scene):
    def __init__(self, name: str, mc: MainCharacter, game_objects: set[GameObject]):
        super().__init__(name)
        self.camera = Camera(Pos(0, 0), GameSettings().screen_center().inv())
        self.game_objs = {g.name: g for g in game_objects}
        self.game_objs["mc"] = mc
        self.mc = mc

    def update(self):
        super().update()
        self.camera.target_pos = self.mc.fpos
        self.camera.update()
        for game_obj in self.game_objs.values():
            game_obj.update()
        self._handle_collisions()

    def _handle_collisions(self):
        # Standard mc collisions
        collidables, mc = self.collidable_game_objs, self.mc
        for game_obj in collidables:
            if mdv := mc.collide(game_obj):
                mc.fpos -= mdv * 1.0001
                v_angle = polar_angle(zeros(2), mdv.to_array())
                if -pi / 4 > v_angle > -3 * pi / 4:
                    mc.falling = False
        # Check if mc still on ground
        if not any(mc.collide(o, offset=FPos(0, -10)) for o in collidables):
            mc.falling = True

    def on_event(self, event: Event):
        super().on_event(event)
        for game_obj in self.game_objs.values():
            game_obj.on_event(event)

    def render(self, screen: Surface):
        super().render(screen)
        screen.fill((255, 255, 255))
        for game_obj in self.game_objs.values():
            self.camera.render(screen, game_obj)

    @property
    def collidable_game_objs(self) -> set[GameObject]:
        return {o for o in self.game_objs.values() if o.collidable}

    @property
    def interactable_game_objs(self) -> set[GameObject]:
        return {o for o in self.game_objs.values() if o.interactable}
