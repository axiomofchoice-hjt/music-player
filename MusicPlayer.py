import json
import keyboard
import threading
import time
import pygame
import os
pygame.init()
pygame.mixer.init()

sta = {}
isPlaying = True
musicList = []
musicIndex = 0

def replay():
    pygame.mixer.music.load(musicList[musicIndex])
    pygame.mixer.music.play()

def nextMusic():
    global musicIndex
    musicIndex = (musicIndex + 1) % len(musicList)
    replay()

def prevMusic():
    global musicIndex
    musicIndex = (musicIndex - 1) % len(musicList)
    replay()

def checkEnd():  # 检查播放完毕，并下一首
    global musicList, musicIndex
    if not pygame.mixer.music.get_busy() and isPlaying:
        nextMusic()

class MainLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while pygame.mixer.get_init():
            checkEnd()
            time.sleep(1)


mainLoop = MainLoop()
# mainLoop()


def mixerPause():  # 暂停 / 继续播放
    global isPlaying
    if isPlaying:
        print("暂停播放")
        pygame.mixer.music.pause()
    else:
        print("继续播放")
        pygame.mixer.music.unpause()
    isPlaying ^= True


def mixerVolumeUp():  # 调高音量
    sta["volume"] = min(1.0, sta["volume"] + 0.05)
    pygame.mixer.music.set_volume(sta["volume"])
    print(f"""当前音量：{sta["volume"]:.2f}""")


def mixerVolumeDown():  # 调低音量
    sta["volume"] = max(0.0, sta["volume"] - 0.05)
    pygame.mixer.music.set_volume(sta["volume"])
    print(f"""当前音量：{sta["volume"]:.2f}""")


def stateSave():
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(sta))
    pygame.mixer.quit()
    exit()


def addMusic(file):
    if os.path.isfile(file):
        musicList.append(file)


def stateLoad():
    global sta, musicList, musicIndex
    with open("data.json", "r", encoding="utf-8") as f:
        sta = json.loads(f.read())
    pygame.mixer.music.set_volume(sta["volume"])
    print(sta["playing"])
    for path in sta["list"]:
        if os.path.isdir(path):
            for i in os.listdir(path):
                addMusic(path + "\\" + i)
        else:
            addMusic(path)
    for index, file in enumerate(musicList):
        print(index, file)
        if os.path.samefile(file, sta["playing"]):
            musicIndex = index
    replay()
    mainLoop.start()


stateLoad()

keyboard.add_hotkey("ctrl+alt+space", mixerPause)
keyboard.add_hotkey("ctrl+alt+up", mixerVolumeUp)
keyboard.add_hotkey("ctrl+alt+down", mixerVolumeDown)
keyboard.add_hotkey("ctrl+alt+right", nextMusic)
keyboard.add_hotkey("ctrl+alt+left", prevMusic)
keyboard.add_hotkey("ctrl+alt+esc", stateSave)
