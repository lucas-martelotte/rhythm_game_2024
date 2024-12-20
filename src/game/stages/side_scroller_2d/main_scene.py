from queue import Queue

import pygame
from pygame.event import Event
from pygame.surface import Surface

from src.core.entity import Camera
from src.core.essentials import FPos, Pos, Rect, Scene
from src.game.singletons import GameSettings

from .action import Action
from .game_object import GameObject
from .game_objects import DialogueBox, InteractButton, MainCharacter
from .trigger import TriggerSheet


class MainScene(Scene):
    def __init__(
        self,
        name: str,
        main_character: MainCharacter,
        game_objects: set[GameObject],
        trigger_sheet: TriggerSheet,
    ):
        super().__init__(name)
        self.trigger_sheet = trigger_sheet
        self.camera = Camera(main_character.pos, GameSettings().screen_center().inv())
        self.game_objs = {g.name: g for g in game_objects}
        # For executing triggers
        self._action_queue: Queue[Action] = Queue()
        self._curr_action: Action | None = None

        self._max_z_index = max(o.z_index for o in game_objects)
        self._min_z_index = min(o.z_index for o in game_objects)

        self.mc = main_character
        self.add_game_obj(main_character)
        self.camera.target_obj = self.mc

        self.interact_btn = InteractButton()
        self.add_game_obj(self.interact_btn)

        self.dialogue_box = DialogueBox((400, 200))
        self.add_game_obj(self.dialogue_box)
        self.dialogue_box.set_target_obj(self.mc)

    def update(self):
        super().update()

        if self._curr_action:  # If there is an action running
            self.interact_btn.set_hidden(True)
            if self._curr_action.done:
                self._run_next_action()
        else:
            self.dialogue_box.set_hidden(True)
            self.interact_btn.set_hidden(not bool(self.interact_btn.interacting_obj))

        self.camera.update()
        for game_obj in self.game_objs.values():
            game_obj.update()
        self._handle_collisions()

    def _handle_collisions(self):
        self.mc.handle_collisions(self.collidables)
        # Handling interactions
        self.interact_btn.set_interactable_obj(None)
        for z_index in range(self._max_z_index, self._min_z_index - 1, -1):
            for game_obj in self.get_interactable_game_objs_by_z_index(z_index):
                if self.mc.collide(game_obj):
                    self.interact_btn.set_interactable_obj(game_obj)

    def on_event(self, event: Event):
        super().on_event(event)
        if self._curr_action and not self._curr_action.done:
            self._curr_action.on_event(event)
            return
        for game_obj in self.game_objs.values():
            game_obj.on_event(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if int_obj := self.interact_btn._interacting_obj:
                    if trigger := self.trigger_sheet.get_obj_trigger(int_obj):
                        for action in trigger.actions:
                            self._action_queue.put(action)
                        self._run_next_action()

    def render(self, screen: Surface):
        super().render(screen)
        screen.fill((255, 255, 255))
        for game_obj in self.game_objs.values():
            self.camera.render(screen, game_obj)

    def _run_next_action(self):
        self._curr_action = None
        if self._action_queue.empty():
            return  # No more actions to run
        self._curr_action = self._action_queue.get()
        self._curr_action.start(self.game_objs, self.camera)

    def add_game_obj(self, game_obj: GameObject):
        self.game_objs[game_obj.name] = game_obj

    @property
    def collidables(self) -> set[GameObject]:
        return {o for o in self.game_objs.values() if o.collidable}

    @property
    def interactables(self) -> set[GameObject]:
        return {o for o in self.game_objs.values() if o.interactable}

    def get_game_objs_by_z_index(self, z_index: int) -> set[GameObject]:
        return {o for o in self.game_objs.values() if o.z_index == z_index}

    def get_interactable_game_objs_by_z_index(self, z_index: int) -> set[GameObject]:
        return {o for o in self.interactables if o.z_index == z_index}

    def get_collidable_game_objs_by_z_index(self, z_index: int) -> set[GameObject]:
        return {o for o in self.collidables if o.z_index == z_index}
