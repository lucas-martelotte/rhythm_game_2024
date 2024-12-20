from pygame.mixer import Channel, Sound, music

from src.core.utils import SingletonMetaclass


class Mixer(metaclass=SingletonMetaclass):

    MUSIC_BASE_PATH = "src/data/resources/sound/music/"
    SFX_BASE_PATH = "src/data/resources/sound/sfx/"
    BLIP_BASE_PATH = "src/data/resources/sound/blip/"

    SFX_CHANNEL = 1
    BLIP_CHANNEL = 2

    def play_sfx(self, sound_name: str, volume: float = 0.01):
        channel = Channel(self.SFX_CHANNEL)
        sound_dir = self.BLIP_BASE_PATH + sound_name
        self._play_from_directory(sound_dir, channel, volume=volume)

    def play_blip(self, sound_name: str, volume: float = 0.01):
        channel = Channel(self.BLIP_CHANNEL)
        sound_dir = self.BLIP_BASE_PATH + sound_name
        self._play_from_directory(sound_dir, channel, volume=volume)

    def play_music(self, music_name: str, volume: float = 0.01):
        music_dir = self.MUSIC_BASE_PATH + music_name
        music.set_volume(volume)
        music.load(music_dir)
        music.play()

    def _play_from_directory(
        self, sound_directory: str, channel: Channel, volume: float = 0.01
    ):
        channel.set_volume(volume)
        channel.play(Sound(sound_directory))
