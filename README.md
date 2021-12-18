# music-player

快速使用：

安装 python，用 pip 安装 keyboard, pygame。

运行 MusicPlayer.py 生成 data.json，在 data.json 中 loadList 项里写入文件夹或文件的路径，可以写多个，例如：

```json
{
    "loadList": [
        "./music"
    ],
}
```

注意反斜杠 `\` 需要用 `\\` 表示，或换成斜杠 `/`。

hotkey 表示所有的热键，其中：

- play 重新播放当前音乐
- next 播放目录的下一首
- prev 播放目录的上一首
- random 播放随机的下一首（仅仅不会两遍播放同一首音乐）
- pause 暂停或继续
- quit 退出
- volumeDown 调低音量
- volumeUp 调高音量

initialize 项表示启动时运行的命令（命令参考 hotkey 配置项），可以写 `initialize: ["pause"]` 表示程序启动后暂停播放。

finish 项表示一首音乐播放完后运行的命令（命令参考 hotkey 配置项），例如：

- `finish: ["next"]` 切目录的下一首歌。
- `finish: ["next", "pause"]` 切目录的下一首歌并暂停（注意有先后顺序）。
- `finish: ["random"]` 切随机的下一首歌。
- `finish: ["play"]` 重新播放（单曲循环）.
