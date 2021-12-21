# music-player

用 pygame 写的轻量音乐播放器，命令行界面，支持热键操作

快速使用：

- 安装 python 和 pip
- 用 pip 安装 keyboard, pygame。
- 运行 MusicPlayer.py 生成 data.json
- 在 data.json 中 loadList 项里写入文件夹或文件的路径
- 再次运行 MusicPlayer.py

loadList 配置项，表示从哪些位置导入音乐列表。

- 注意反斜杠 `\` 需要用 `\\` 表示，或换成斜杠 `/`。
- 文件夹末尾不能有斜杠或反斜杠。
- 只会加载 mp3 文件。
- 例如：`"loadList": ["./music/a.mp3", "D:\\music"]`。

命令，可以在程序启动后输入，也可写入 finish、initialize、hotkey 中：

- 这些命令可以在 hotkey 中使用：
  - `play` 重新播放当前音乐
  - `next` 播放目录的下一首
  - `prev` 播放目录的上一首
  - `random` 播放随机音乐（仅仅不会两遍播放同一首音乐）
  - `pause` 暂停或继续
  - `quit` 退出
  - `volumeDown` 调低音量
  - `volumeUp` 调高音量
- 这些命令不可在 hotkey 中使用：
  - `ls` 显示音乐列表
  - `to 序号` 播放指定序号的音乐
  - `setFinish 命令 命令 ...` 设置 finish 配置项
  - `setInitialize 命令 命令 ...` 设置 initialize 配置项

hotkey 配置项，表示所有的全局热键，键为命令，值用 `ctrl+s` 的形式表示。

initialize 配置项，表示启动时运行的命令，例如：

- `initialize: ["pause"]` 程序启动后暂停播放。
- `initialze: ["to 1"]` 程序启动后播放列表第一个音乐。

finish 配置项，表示一首音乐播放完后运行的命令，例如：

- `finish: ["next"]` 切目录的下一首歌。
- `finish: ["next", "pause"]` 切目录的下一首歌并暂停。
- `finish: ["random"]` 切随机的下一首歌。
- `finish: ["play"]` 重新播放（单曲循环）.
