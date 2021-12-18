import random
import json
import keyboard
import threading
import time
import pygame
import os

saveKey: set = {"volume", "loadList",
                "playing", "hotkey", "initialize", "finish"}

defaultSta = {
    "volume": 50,
    "loadList": [],
    "playing": None,
    "hotkey": {
        "play": None,
        "next": "ctrl+alt+right",
        "pause": "ctrl+alt+space",
        "prev": "ctrl+alt+left",
        "quit": "ctrl+alt+esc",
        "random": "ctrl+alt+r",
        "volumeDown": "ctrl+alt+down",
        "volumeUp": "ctrl+alt+up"
    },
    "initialize": [],
    "finish": ["next"],
    "isPlaying": True,
    "musicList": [],
    "musicIndex": None
}
sta = {}


class Methods:
    def run(self, cmd):  # 运行命令
        self.__getattribute__(cmd)()

    def play(self):  # 加载并播放
        sta["playing"] = sta["musicList"][sta["musicIndex"]]
        pygame.mixer.music.load(sta["playing"])
        pygame.mixer.music.play()
        sta["isPlaying"] = True
        print(f"""开始播放 {sta["playing"]}""")
        stateSave()

    def next(self):  # 下一首
        sta["musicIndex"] = (sta["musicIndex"] + 1) % len(sta["musicList"])
        print("下一首")
        self.play()

    def prev(self):  # 上一首
        sta["musicIndex"] = (sta["musicIndex"] - 1) % len(sta["musicList"])
        print("上一首")
        self.play()

    def random(self):  # 随机跳歌
        nextIndex = random.randint(0, len(sta["musicList"]) - 1)
        while len(sta["musicList"]) >= 2 and nextIndex == sta["musicIndex"]:
            nextIndex = random.randint(0, len(sta["musicList"]) - 1)
        sta["musicIndex"] = nextIndex
        print("随机跳歌")
        self.play()

    def pause(self):  # 暂停 / 继续播放
        if sta["isPlaying"]:
            pygame.mixer.music.pause()
            print("暂停播放")
        else:
            pygame.mixer.music.unpause()
            print("继续播放")
        sta["isPlaying"] ^= True

    def quit(self):  # 退出
        pygame.mixer.quit()
        exit()

    def volumeUp(self):  # 调高音量
        sta["volume"] = min(100, sta["volume"] + 5)
        pygame.mixer.music.set_volume(sta["volume"] / 100)
        print(f"""当前音量 {sta["volume"] / 100 :.2f}""")
        stateSave()

    def volumeDown(self):  # 调低音量
        sta["volume"] = max(0, sta["volume"] - 5)
        pygame.mixer.music.set_volume(sta["volume"] / 100)
        print(f"""当前音量 {sta["volume"] / 100 :.2f}""")
        stateSave()


methods = Methods()


def checkEnd():  # 检查播放完毕，并下一首
    if not pygame.mixer.music.get_busy() and sta["isPlaying"]:
        for i in sta["finish"]:
            methods.run(i)


class MainLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while pygame.mixer.get_init():
            checkEnd()
            time.sleep(1)


mainLoop = MainLoop()
# mainLoop()


def stateSave():
    out = {}
    for i in saveKey:
        out[i] = sta[i]
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(out, sort_keys=True,
                indent=4, separators=(',', ': ')))


def addMusic(file):
    if os.path.isfile(file) and file[-4:] == ".mp3":
        sta["musicList"].append(file)
        print(f"""添加音乐 ({len(sta["musicList"])}) {file}""")


def stateLoad():
    global sta

    sta = defaultSta.copy()
    if os.path.isfile("data.json"):
        with open("data.json", "r", encoding="utf-8") as f:
            settings = json.loads(f.read())
            for i in set(settings.keys()) & saveKey:
                sta[i] = settings[i]
    else:
        stateSave()
    sta["musicList"] = []
    for path in sta["loadList"]:
        if os.path.isdir(path):
            for i in os.listdir(path):
                addMusic(path + "/" + i)
        else:
            addMusic(path)
    if len(sta["musicList"]) == 0:
        print("音乐列表为空，请在 data.json 中配置 loadList")
        input("任意键退出")
        exit()

    sta["musicIndex"] = None
    for index, file in enumerate(sta["musicList"]):
        if sta["playing"] is not None and os.path.isfile(sta["playing"]) and os.path.samefile(file, sta["playing"]):
            sta["musicIndex"] = index
    if sta["musicIndex"] is None:
        sta["musicIndex"] = 0
        if sta["playing"] is not None:
            print(f"""未找到音乐 {sta["playing"]}""")
    pygame.mixer.music.set_volume(sta["volume"] / 100)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    stateLoad()

    methods.play()
    for i in sta["initialize"]:
        methods.run(i)

    for i in sta["hotkey"]:
        if sta["hotkey"][i] is not None:
            keyboard.add_hotkey(
                sta["hotkey"][i], methods.__getattribute__(i), suppress=True)

    mainLoop.start()

    while True:
        cmd = input()
        try:
            methods.run(cmd)
        except AttributeError:
            print(f"""未知命令 "{cmd}\"""")
            pass
