import pygame
from pygame.surface import Surface

from src.core.essentials import Scene, SceneTransitionState

from .singletons import GameSettings


class Control:
    def __init__(self, display: Surface, initial_scene: Scene) -> None:
        settings = GameSettings()
        self.display = display
        self.screen = Surface(settings.screen_size)
        self.clock = pygame.time.Clock()
        self.active_scene = initial_scene
        self.scene_dict = {initial_scene.name: initial_scene}

    def main_loop(self):
        while True:
            self.clock.tick(GameSettings().fps)
            self.render()
            pygame.display.update()
            self.active_scene.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                self.active_scene.on_event(event)
            self.handle_scene_transition()

    def render(self):
        settings = GameSettings()
        self.active_scene.render(self.screen)
        scaled = self.screen
        scaled = pygame.transform.smoothscale(self.screen, settings.display_size)
        scaled_rect = scaled.get_rect(center=settings.display_center.to_tuple())
        self.display.blit(scaled, scaled_rect)
        pygame.display.update()

    def set_active_scene(self, scene: Scene):
        self.active_scene = scene

    def handle_scene_transition(self):
        scene = self.active_scene
        match scene.transition_state:
            case SceneTransitionState.CLOSE_AND_MOVE_TO_EXISTING_SCENE:
                assert isinstance(scene.next_scene, str)
                del self.scene_dict[scene.name]
                self.active_scene = self.scene_dict[scene.next_scene]
            case SceneTransitionState.CLOSE_AND_MOVE_TO_NEW_SCENE:
                assert isinstance(scene.next_scene, Scene)
                del self.scene_dict[scene.name]
                self.active_scene = scene.next_scene
                self.scene_dict[self.active_scene.name] = self.active_scene
            case SceneTransitionState.MOVE_TO_EXISTING_SCENE:
                assert isinstance(scene.next_scene, str)
                self.active_scene = self.scene_dict[scene.next_scene]
            case SceneTransitionState.MOVE_TO_NEW_SCENE:
                assert isinstance(scene.next_scene, Scene)
                self.active_scene = scene.next_scene
                self.scene_dict[self.active_scene.name] = self.active_scene
