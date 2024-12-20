from src.game.singletons import GlobalSwitches

from .action import Action
from .game_object import GameObject


class Trigger:
    def __init__(self, required_switches: set[str], actions: list[Action]):
        self.required_switches = required_switches
        self.actions = actions


class TriggerSheet:
    def __init__(
        self,
        instant_triggers: list[Trigger],
        obj_trigger_dict: dict[tuple[str, str], list[Trigger]],
    ):
        self.instant_triggers = instant_triggers
        self.obj_trigger_dict = obj_trigger_dict

    def get_obj_trigger(self, game_obj: GameObject) -> Trigger | None:
        name, local_switch = game_obj.name, game_obj.local_switch
        if triggers := self.obj_trigger_dict.get((name, local_switch)):
            global_switches = GlobalSwitches()
            for trigger in triggers:
                if all(global_switches.check(s) for s in trigger.required_switches):
                    return trigger
        return None
