# music-player

用 pygame 写的音乐播放器（黑白框界面，经支持热键）

快速使用：

安装 python，用 pip 安装 keyboard, pygame。

运行 MusicPlayer.py 生成 data.json，在 data.json 中 loadList 项里写入文件夹或文件的路径，可以写多个。

- 注意反斜杠 `\` 需要用 `\\` 表示，或换成斜杠 `/`。
- 文件夹末尾不能有斜杠或反斜杠。
- 只会加载 mp3 文件。
- 例如：`"loadList": ["./music/a.mp3", "D:\\music"]`。

hotkey 表示所有的全局热键，值用 `ctrl+s` 的形式表示，键的含义：

- play 重新播放当前音乐
- next 播放目录的下一首
- prev 播放目录的上一首
- random 播放随机的下一首（仅仅不会两遍播放同一首音乐）
- pause 暂停或继续
- quit 退出
- volumeDown 调低音量
- volumeUp 调高音量

initialize 项表示启动时运行的命令（命令参考 hotkey 配置项）

- 例如 `initialize: ["pause"]` 表示程序启动后暂停播放。

finish 项表示一首音乐播放完后运行的命令（命令参考 hotkey 配置项），例如：

- `finish: ["next"]` 切目录的下一首歌。
- `finish: ["next", "pause"]` 切目录的下一首歌并暂停（注意有先后顺序）。
- `finish: ["random"]` 切随机的下一首歌。
- `finish: ["play"]` 重新播放（单曲循环）.
