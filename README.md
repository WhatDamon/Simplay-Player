<img width="48" height="48" align="left" style="float: left; margin: 0 10px 0 0;" alt="Simplay Player Logo" src="https://github.com/WhatDamon/Simplay-Player/blob/main/asset/simplay.png">  

# Simplay Player

![Python requirement](https://img.shields.io/badge/python-≥3.8-brightgreen?logo=python)
![GitHub repo size](https://img.shields.io/github/repo-size/WhatDamon/Simplay-Player)
![GitHub repo license](https://img.shields.io/github/license/WhatDamon/Simplay-Player)
![GitHub Action #1](https://github.com/WhatDamon/Simplay-Player/actions/workflows/build.yml/badge.svg)
![GitHub Action #2](https://github.com/WhatDamon/Simplay-Player/actions/workflows/buildwin.yml/badge.svg)
![GitHub repo stars](https://img.shields.io/github/stars/WhatDamon/Simplay-Player)

> [!IMPORTANT]  
> 注意, 该软件在 macOS 和 Linux 下可能存在影响比较大的 BUG 需要注意, Windows 端基本稳定并可用. 由于一些原因该项目将会进入缓慢更新阶段, 望谅解!

这是一个 __闲得发慌时__ 开发出来的小作品, 写得很烂请见谅

最早被称为 __Simply Player__ 即 __简单的播放器__, __Simplay__ 是在码字过程中意外中得到名字

支持 `MP3`、`M4A`、`FLAC`、`WAV`、`AAC` 格式 (已测试的所有格式中, `APE`、`MP2`、`WMA`、`OGG`有不同程度的不支持, 其他格式也有可能支持)

如果喜欢可以点个 Star, 当然目前我还是更希望各位可以为项目开发添砖加瓦, 多来点 PR

## 要求

__Python 3.8 及更高版本__, 推荐 3.10 及更高版本以保障其正常运行 (Action 中我们使用了 Python 3.11 进行编译测试)

开发使用前 __*nix系统__ 需要先执行...

~~~Bash
pip install -r requirements.txt
~~~

而 __Windows__ 则需要执行...

~~~Bash
pip install -r requirements_win.txt
~~~

___注：区分的原因是 `Windows-Toasts` 库只能在 Windows 下生效!___

如果希望开发 WinRT 相关内容 (如 SMTC), 需要执行...

~~~Bash
pip install winsdk
~~~

此外, 该软件 __不能在含有 CJK 文本 (即中文、日语、韩文) 的路径下正常开发与运行__!

## TODO

- [x] 基本逻辑
- [x] 吐司通知 (Windows 独占性功能, 其它系统使用 `SnackBar` 替代)
- [x] 快进与倍速播放
- [x] GitHub Actions 自动测试编译工作流 (使用 __Nuitka__ 实现, 详见[本项目 Actions](https://github.com/WhatDamon/Simplay-Player/actions))
- [x] 多语言支持 (基本, 目前只有美式英语 `en_US` 和简体中文 `zh_CN`, 若要贡献翻译请查看 [Wiki](https://github.com/WhatDamon/Simplay-Player/wiki/%E8%BD%AF%E4%BB%B6%E7%BF%BB%E8%AF%91))
- [x] 日志输出 (注: 会产生大量日志信息保存在本地, 提交 issue 请附带该文件)
- [x] 循环播放
- [x] 歌词显示与滚动 (基本完成, 但依旧不兼容逐字歌词, 姑且算完成了)
- [x] 在线获取网易云歌曲 (还有一些 BUG, 慢慢修, 此外 API 比较玄学, 很多逻辑都可能存在问题)
- [x] 歌单 (除了不支持删除列表项和添加在线歌曲以外基本完成)
- [x] 检查更新 (基于 __GitHub API__, 允许在语言文件定义切换为 KKGitHub 镜像源)
- [ ] 进阶逻辑
- [ ] 进阶播放方式选择 (目前就只支持一个单曲循环)
- [ ] 将主界面迁移至 `pages` 中
- [ ] 设置 (施工中, 目前还需要研究 JSON 读写, 重写 `i18n/lang.py` 的部分功能才能实现自定义语言)
- [ ] 区间播放 (即 AB 点)
- [ ] 系统托盘 (预计使用 `pystray` 实现, 如果实现了就可以让 `Windows-Toasts` 退役了)
- [ ] 界面自动取色 (可能使用 __OpenCV__ 实现, 或者自己算)
- [ ] 混音器 (目前使用的组件未提供相关接口, 暂时搁置)
- [ ] SMTC 支持 (涉及 WinRT, 仅 Windows, 但实现有点麻烦, 调用代码已注释, 代码在 `lib/smtc.py`, 完成后可能会接入热词实现桌面歌词功能)
- [ ] 任务栏进度条与按键操作 (仅 Windows 支持)
- [ ] 多线程支持 (目前的想法只有独立检查更新线程, 其他还需要研究)
- [ ] 拖入文件加载或命令行加载 (命令行应该会简单一点, 另外一个主要是拖入文件找不到接口)

对于其他可能的新功能可以到[本项目 Discussions](https://github.com/WhatDamon/Simplay-Player/discussions) 提交

## BUG 列表

以下内容不一定完全, 可能存在更多不在这个列表的 BUG!

- [x] 打开歌曲后需要连续点击三次播放键才可以进入播放状态 (通过调整代码逻辑修复)
- [x] 隐藏顶栏或者 `Ctrl` + `H` 快捷键等操作以后后歌曲进度条无法工作 (已知是 `SnackBar` 导致的, 暂时注释掉了, 但是当前还有很多会造成问题的 `SnackBar` 由于一些原因尚未被注释)
- [x] 读取存在封面的歌曲后再打开无封面歌曲不会替换成占位的 `track.png`
- [x] 加载歌曲或更换歌曲后前可能会有些不是特别影响的报错 (`try` 大法成功忽略)
- [ ] 窗口标题有时不能按希望的方式显示 (实际解决很简单, 但是我希望能够整合一下)

___注: 接下来将不再这里更新 BUG, 有关 BUG 内容请看 [Releases](https://github.com/WhatDamon/Simplay-Player/releases)___

## 急切的任务

- [ ] 代码整理与注释, 功能分单独代码文件 (处理中)

## 使用到的第三方项目

- [flet](https://github.com/flet-dev/flet) (Apache-2.0 license)
- [TinyTag](https://github.com/devsnd/tinytag) (MIT license)
- [Windows-Toasts](https://github.com/DatGuy1/Windows-Toasts) (Apache-2.0 license)

___其他的都是 Python 内建库了...___