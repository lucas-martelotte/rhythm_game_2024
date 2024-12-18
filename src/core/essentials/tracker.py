from math import floor
from time import time

from ..utils.auxiliary import mean


class TimeTracker:
    def __init__(self) -> None:
        self._last_checked_time: float | None = None

    def get_time_passed(self) -> float:
        if not self._last_checked_time:
            self._last_checked_time = time()
            return 0
        curr_time = time()
        time_passed = curr_time - self._last_checked_time
        self._last_checked_time = curr_time
        return time_passed


class FPSTracker:
    def __init__(self, fps: int):
        self._fps = fps
        self._last_checked_time: float | None = None
        self._leftover_time = 0.0

    def get_frames_passed(self) -> int:
        if not self._last_checked_time:
            self._last_checked_time = time()
            return 0
        curr_time = time()
        time_passed = (curr_time - self._last_checked_time) + self._leftover_time
        frames_passed_float = time_passed * self._fps
        frames_passed_int = floor(frames_passed_float)
        self._leftover_time = (frames_passed_float - frames_passed_int) / self._fps
        self._last_checked_time = curr_time
        return frames_passed_int


class FPSAnalyzer(FPSTracker):
    def __init__(self, fps: int):
        super().__init__(fps)
        self._last_fps_values: list[float] = []
        self._last_frame_loss_values: list[float] = []
        self._fps_mean = 0
        self._frame_loss_mean = 0

    def get_frames_passed(self):
        frames_passed_int = super().get_frames_passed()
        curr_time = time()
        try:
            self._last_fps_values.append(1 / (curr_time - self._last_checked_time))
            self._last_frame_loss_values.append(frames_passed_int - 1)
        except:
            pass
        if len(self._last_fps_values) > 100:
            self._fps_mean = int(mean(self._last_fps_values))
            self._frame_loss_mean = int(mean(self._last_frame_loss_values))
            self._last_fps_values = []
            self._last_frame_loss_values = []
        self._last_checked_time = curr_time
        return frames_passed_int

    @property
    def fps_mean(self) -> int:
        return self._fps_mean

    @property
    def frame_loss_mean(self) -> int:
        return self._frame_loss_mean
