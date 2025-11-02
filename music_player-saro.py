import pygame
import os
import time
import numpy as np
import librosa
from colorama import init, Fore, Style
import sys

# ✅ Fix: ensure UTF-8 output for emojis
sys.stdout.reconfigure(encoding='utf-8')

# Initialize colorama
init(autoreset=True)

# Music folder and song
MUSIC_FOLDER = r"D:\Music-on"
SONG_FILE = "Saro.mp3"

# Lyrics text
LYRICS_TEXT = [
    "Oxygen alavavan 🌬️",
    "Yaar Ava Yaar Ava 🤔",
    "Oor solum Star Ava 🌟",
    "Ava than Ennavanaa 🎵",
    "Oru Alai Ava 🌊",
    "Kalai Ava 🌅",
    "Azhagiya Nilavava 🌕",
    "Nizalilum jolikkira 🌿",
    "Niranthara oli ava 💡",
    "Sari ava ✅",
    "Thavarava ❌",
    "Sirikira siripukku 😄",
    "Avanthaa kaaranamaa 🤔"
]

# Rainbow colors
RAINBOW_COLORS = [
    Fore.RED, Fore.LIGHTRED_EX, Fore.YELLOW, Fore.LIGHTYELLOW_EX,
    Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.CYAN, Fore.LIGHTCYAN_EX,
    Fore.BLUE, Fore.LIGHTBLUE_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX
]


def auto_generate_beat_times(song_path, num_lines):
    """Generate beat-aligned start times for lyrics using librosa."""
    print(Fore.CYAN + "\n🎵 Analyzing song beats...")
    y, sr = librosa.load(song_path, sr=None)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    total_time = librosa.get_duration(filename=song_path)

    # Split song evenly across lyrics if beats are too few
    if len(beat_times) < num_lines + 1:
        beat_times = np.linspace(0, total_time, num_lines + 1)
    else:
        # pick evenly spaced beats
        idxs = np.linspace(0, len(beat_times) - 1, num_lines + 1, dtype=int)
        beat_times = beat_times[idxs]

    print(Fore.GREEN + "✅ Beat times generated!\n")
    return beat_times


def blink_emoji(emoji, color, times=3, interval=0.2):
    """Blink emoji in place."""
    for _ in range(times):
        print(color + emoji, end='', flush=True)
        time.sleep(interval)
        print('\b' * len(emoji) + ' ' * len(emoji) + '\b' * len(emoji), end='', flush=True)
        time.sleep(interval)
    print(color + emoji, end=' ', flush=True)


def print_lyric(line):
    """Colorful animated lyric printing."""
    words = line.split(" ")
    for j, word in enumerate(words):
        color = RAINBOW_COLORS[j % len(RAINBOW_COLORS)]
        emoji = ""
        new_word = ""
        for char in word:
            if ord(char) > 10000:
                emoji = char
            else:
                new_word += char
        for c in new_word:
            print(color + c, end='', flush=True)
            time.sleep(0.03)
        print(' ', end='', flush=True)
        if emoji:
            blink_emoji(emoji, color)
    print()  # new line


def play_song(song_file):
    """Play song and show synced lyrics."""
    song_path = os.path.join(MUSIC_FOLDER, song_file)
    beat_times = auto_generate_beat_times(song_path, len(LYRICS_TEXT))

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    start_time = time.time()
    paused_time = 0
    lyric_index = 0

    print(Fore.CYAN + Style.BRIGHT + f"\n🎧 Now Playing: '{song_file}' 🎵\n")
    print(Fore.YELLOW + "Controls: p = pause | r = resume | s = skip | q = stop\n")

    while pygame.mixer.music.get_busy():
        current_time = time.time() - start_time - paused_time

        if lyric_index < len(LYRICS_TEXT) and current_time >= beat_times[lyric_index]:
            print_lyric(LYRICS_TEXT[lyric_index])
            lyric_index += 1

        # Keyboard controls (Windows only)
        if os.name == "nt":
            import msvcrt
            if msvcrt.kbhit():
                command = msvcrt.getwch().lower()
                if command == "p":
                    pygame.mixer.music.pause()
                    pause_start = time.time()
                    print(Fore.GREEN + "⏸ Paused")
                elif command == "r":
                    pygame.mixer.music.unpause()
                    paused_time += time.time() - pause_start
                    print(Fore.GREEN + "▶️ Resumed")
                elif command == "s":
                    pygame.mixer.music.stop()
                    print(Fore.CYAN + "⏭ Skipped to next song")
                    break
                elif command == "q":
                    pygame.mixer.music.stop()
                    print(Fore.RED + "⏹ Stopped playback")
                    exit()

        time.sleep(0.01)


def main():
    pygame.mixer.init()
    song_path = os.path.join(MUSIC_FOLDER, SONG_FILE)
    if not os.path.exists(song_path):
        print(Fore.RED + f"⚠️ Song not found: {song_path}")
        return
    play_song(SONG_FILE)
    print(Fore.LIGHTGREEN_EX + "\n🎵 All lyrics finished! Goodbye!")


if __name__ == "__main__":
    main()
