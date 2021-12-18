import random
import json
import keyboard
import threading
import time
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
if True:  # 防止代码格式化时被排到 environ 赋值前
    import pygame

# data.json 的内容
saveKey = {"volume", "loadList",
           "playing", "hotkey", "initialize", "finish"}

# 命令行重定向
cmdRedirects = {
    "ls": "musicList",
    "exit": "quit",
}

# 默认 sta 内容
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

# 状态
sta = {}


class Methods:
    def run(self, cmd):  # 运行命令
        spt = cmd.split()
        method = spt[0]
        if method in cmdRedirects:
            method = cmdRedirects[method]
        args = spt[1:]
        self.__getattribute__(method)(args)

    def play(self, args=None):  # 加载并播放
        sta["playing"] = sta["musicList"][sta["musicIndex"]]
        pygame.mixer.music.load(sta["playing"])
        pygame.mixer.music.play()
        sta["isPlaying"] = True
        print(f"""开始播放 {sta["playing"]}""")
        stateSave()

    def next(self, args=None):  # 下一首
        sta["musicIndex"] = (sta["musicIndex"] + 1) % len(sta["musicList"])
        print("下一首")
        self.play()

    def prev(self, args=None):  # 上一首
        sta["musicIndex"] = (sta["musicIndex"] - 1) % len(sta["musicList"])
        print("上一首")
        self.play()

    def random(self, args=None):  # 随机跳歌
        nextIndex = random.randint(0, len(sta["musicList"]) - 1)
        while len(sta["musicList"]) >= 2 and nextIndex == sta["musicIndex"]:
            nextIndex = random.randint(0, len(sta["musicList"]) - 1)
        sta["musicIndex"] = nextIndex
        print("随机跳歌")
        self.play()

    def pause(self, args=None):  # 暂停 / 继续播放
        if sta["isPlaying"]:
            pygame.mixer.music.pause()
            print("暂停播放")
        else:
            pygame.mixer.music.unpause()
            print("继续播放")
        sta["isPlaying"] ^= True

    def quit(self, args=None):  # 退出
        pygame.mixer.quit()
        exit()

    def volumeUp(self, args=None):  # 调高音量
        sta["volume"] = min(100, sta["volume"] + 5)
        pygame.mixer.music.set_volume(sta["volume"] / 100)
        print(f"""当前音量 {sta["volume"] / 100 :.2f}""")
        stateSave()

    def volumeDown(self, args=None):  # 调低音量
        sta["volume"] = max(0, sta["volume"] - 5)
        pygame.mixer.music.set_volume(sta["volume"] / 100)
        print(f"""当前音量 {sta["volume"] / 100 :.2f}""")
        stateSave()

    def musicList(self, args=None):  # 显示音乐列表
        for (index, i) in enumerate(sta["musicList"]):
            print(f"""({index + 1}) {i}""")

    def to(self, args=None):  # 播放指定序号的音乐
        if type(args) != list or len(args) < 1 or int(args[0]) - 1 < 0 or int(args[0]) - 1 >= len(sta["musicList"]):
            print("参数错误")
            return
        sta["musicIndex"] = int(args[0]) - 1
        self.play()

    def setFinish(self, args=[]):  # 修改 Finish 配置项
        sta["finish"] = list(args)
        stateSave()

    def setInitialize(self, args=[]):  # 修改 initialize 配置项
        sta["initialize"] = list(args)
        stateSave()

    # def setHotkey(self, args=[]):  # 修改热键，不写了，摆烂了
    #     if type(args) != list or len(args) < 1:
    #         print("参数错误")
    #         return
    #     if len(args) == 1:
    #         sta["hotkey"][args[0]] = None
    #     else:
    #         sta["hotkey"][args[0]] = args[1]


class CheckFinish(threading.Thread):  # 一个线程，在音乐结束后执行 finish 命令，每秒检查一次
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while pygame.mixer.get_init():
            if not pygame.mixer.music.get_busy() and sta["isPlaying"]:
                for i in sta["finish"]:
                    methods.run(i)
            time.sleep(1)


methods = Methods()
checkFinish = CheckFinish()


def addMusic(file):  # 添加音乐
    if os.path.isfile(file) and file[-4:].lower() == ".mp3":
        sta["musicList"].append(file)
        print(f"""添加音乐 ({len(sta["musicList"])}) {file}""")


def stateSave():  # 保存为 data.json
    out = {}
    for i in saveKey:
        out[i] = sta[i]
    with open("data.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(out, sort_keys=True,
                indent=4, separators=(',', ': ')))


def stateLoad():  # 加载 data.json
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
        elif os.path.isfile(path):
            addMusic(path)
        else:
            print(f"""error: {path} 不是文件或目录""")
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
            print(f"""error: 未找到音乐 {sta["playing"]}""")
    pygame.mixer.music.set_volume(sta["volume"] / 100)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    # 加载 data.json
    stateLoad()

    # 加载热键
    for i in sta["hotkey"]:
        if sta["hotkey"][i] is not None:
            keyboard.add_hotkey(
                sta["hotkey"][i], methods.__getattribute__(i))

    # 执行 initialize 命令
    methods.play()
    for i in sta["initialize"]:
        methods.run(i)

    # 启动检查结束线程
    checkFinish.start()

    # 命令行输入
    while True:
        cmd = input()
        try:
            methods.run(cmd)
        except AttributeError:
            print(f"""未知命令 "{cmd}\"""")
            pass
