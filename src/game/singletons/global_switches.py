class GlobalSwitches:
    def __init__(self) -> None:
        self.switches: set[str] = set()

    def add(self, switch: str):
        self.switches.add(switch)

    def remove(self, switch: str):
        if switch in self.switches:
            self.switches.remove(switch)

    def check(self, switch: str) -> bool:
        return switch in self.switches
