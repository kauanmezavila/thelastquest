from __future__ import annotations

import os
import random
from pathlib import Path


class AudioManager:
    def __init__(self) -> None:
        self.enabled = False
        self.sounds = {}
        self.music_tracks = []
        self._last_track = None
        self._pygame = None
        audio_dir = Path(__file__).resolve().parent.parent / "assets" / "audio"
        theme_dir = Path(__file__).resolve().parent.parent / "assets" / "themes"

        try:
            os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
            import pygame

            pygame.mixer.init()
            self._pygame = pygame
            self.enabled = True
            for name in (
                "button",
                "character",
                "dialogue",
                "discovery",
                "battle",
                "magic",
                "heal",
                "hit",
                "victory",
                "retreat",
                "travel",
                "item",
            ):
                path = audio_dir / f"{name}.wav"
                if path.is_file():
                    self.sounds[name] = pygame.mixer.Sound(str(path))
            self.music_tracks = sorted(theme_dir.glob("*.mp3"))
            if not self.music_tracks:
                fallback = audio_dir / "eldoria_theme.wav"
                if fallback.is_file():
                    self.music_tracks = [fallback]
            self._play_next_music()
        except (ImportError, OSError, RuntimeError):
            # Keep the text game usable on systems without an audio device.
            self.enabled = False

    def _play_next_music(self) -> None:
        if not self.enabled or not self.music_tracks:
            return
        pygame = self._pygame
        if pygame is None:
            return
        choices = [track for track in self.music_tracks if track != self._last_track]
        track = random.choice(choices or self.music_tracks)
        try:
            pygame.mixer.music.load(str(track))
            pygame.mixer.music.set_volume(0.28)
            loops = -1 if len(self.music_tracks) == 1 and track.suffix == ".wav" else 0
            pygame.mixer.music.play(loops)
            self._last_track = track
        except (OSError, RuntimeError):
            self.music_tracks = [item for item in self.music_tracks if item != track]
            self._play_next_music()

    def update_music(self) -> None:
        pygame = self._pygame
        if self.enabled and self.music_tracks and pygame is not None and not pygame.mixer.music.get_busy():
            self._play_next_music()

    def play(self, name: str) -> None:
        sound = self.sounds.get(name)
        if sound is None:
            return
        try:
            sound.play()
        except (OSError, RuntimeError):
            pass

    def close(self) -> None:
        if self._pygame is not None and self.enabled:
            try:
                self._pygame.mixer.quit()
            except (OSError, RuntimeError):
                pass
