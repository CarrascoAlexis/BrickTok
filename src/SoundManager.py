"""SoundManager.py

Created on 2025-10-17

Manages sound effects and music for the game.

"""
__author__ = "carras_a"
__version__ = "1.0"

import os
import pygame


class SoundManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not SoundManager._initialized:
            self.sounds = {}
            self._load_sounds()
            SoundManager._initialized = True

    def _load_sounds(self):
        """Load all sound effects from the assets/sounds directory"""
        sounds_dir = os.path.join("assets", "sounds")

        # Create directory if it doesn't exist
        if not os.path.exists(sounds_dir):
            os.makedirs(sounds_dir)
            return

        # Load all .wav files
        for filename in os.listdir(sounds_dir):
            if filename.endswith(".wav"):
                name = os.path.splitext(filename)[0]
                try:
                    self.sounds[name] = pygame.mixer.Sound(
                        os.path.join(sounds_dir, filename))
                except Exception as e:
                    print(f"Warning: could not load sound {filename}: {e}")

    def play(self, sound_name, volume=1.0):
        """Play a sound effect by name"""
        if sound_name in self.sounds:
            sound = self.sounds[sound_name]
            sound.set_volume(volume)
            sound.play()

    def stop(self, sound_name):
        """Stop a sound effect"""
        if sound_name in self.sounds:
            self.sounds[sound_name].stop()
