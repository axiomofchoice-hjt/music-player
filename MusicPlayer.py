import json
import keyboard
import threading
import time
import pygame
import os

pygame.init()
pygame.mixer.init()

sta = {"volume": 0.5, "list": [".\\music"], "playing": None}
isPlaying = True
musicList = []
musicIndex = 0

def replay():
    pygame.mixer.music.load(musicList[musicIndex])
    pygame.mixer.music.play()
    print(f"开始播放：{musicList[musicIndex]}")

def nextMusic():
    global musicIndex
    musicIndex = (musicIndex + 1) % len(musicList)
    print("下一首")
    replay()

def prevMusic():
    global musicIndex
    musicIndex = (musicIndex - 1) % len(musicList)
    print("上一首")
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
        pygame.mixer.music.pause()
        print("暂停播放")
    else:
        pygame.mixer.music.unpause()
        print("继续播放")
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
    sta["playing"] = musicList[musicIndex]
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(sta))


def quit():
    stateSave()
    pygame.mixer.quit()


def addMusic(file):
    if os.path.isfile(file):
        musicList.append(file)
        print(f"添加音乐 ({len(musicList)}) {file}")


def stateLoad():
    global sta, musicList, musicIndex
    if not os.path.isfile("data.json"):
        stateSave()
    with open("data.json", "r", encoding="utf-8") as f:
        sta = json.loads(f.read())
    for path in sta["list"]:
        if os.path.isdir(path):
            for i in os.listdir(path):
                addMusic(path + "\\" + i)
        else:
            addMusic(path)
    for index, file in enumerate(musicList):
        if sta["playing"] is not None and os.path.samefile(file, sta["playing"]):
            musicIndex = index
    replay()
    pygame.mixer.music.set_volume(sta["volume"])
    mainLoop.start()


stateLoad()

keyboard.add_hotkey("ctrl+alt+space", mixerPause)
keyboard.add_hotkey("ctrl+alt+up", mixerVolumeUp)
keyboard.add_hotkey("ctrl+alt+down", mixerVolumeDown)
keyboard.add_hotkey("ctrl+alt+right", nextMusic)
keyboard.add_hotkey("ctrl+alt+left", prevMusic)
keyboard.add_hotkey("ctrl+alt+esc", quit)
