<img width="150" height="150" align="left" style="float: left; margin: 0 10px 0 0;" alt="Simplay Player Logo" src="https://github.com/WhatDamon/Simplay-Player/blob/main/asset/simplay.png">  

# Simplay Player

> [!IMPORTANT]  
> WIP! 大部分功能还在开发中, 并且目前也存在着非常严重的恶性 BUG 需要修复, 基本处于不可用状态

这是一个 __闲得发慌时__ 开发出来的小作品

支持 `MP3`、`OGG`、`M4A`、`FLAC`、`WAV` 格式 (不在这里的部分格式也是可以用的吧,建议各位测试一下)

如果喜欢可以点个 Star, 当然目前我还是更希望各位可以为项目开发添砖加瓦, 多来点 PR

## 要求

__Python 3.8 及更高版本__, 推荐 3.10 及更高版本以保障其正常运行

开发前需要先执行...

~~~Bash
pip install -r requirements.txt
~~~

___注：`Windows-Toasts` 库只能在 Windows 下生效!___

## TODO

- [x] 基本逻辑
- [x] 吐司通知 (Windows 独占性功能)
- [ ] 设置 (目前已有占位按钮 `settings_btn`)
- [ ] 歌词显示与滚动 (已预留了歌词路径变量 `lyricFile` 和读取函数 `lyricExistAndRead`)
- [ ] 歌单 (目前已有占位按钮 `audioList_btn`)
- [ ] 日志输出
- [ ] 系统托盘
- [ ] 检查更新 (基于 __Github API__)
- [ ] 界面自动取色
- [ ] 混音器
- [ ] 在线获取歌曲 (__网易云__) (目前已有占位菜单按钮)
- [ ] GitHub Actions 自动编译工作流 (使用 __Nuitka__ 实现)

## BUG 列表

以下内容不一定完全, 可能存在更多不在这个列表的 BUG!

- [ ] 读取存在封面的歌曲后再打开无封面歌曲不会替换成占位的 `track.png`
- [ ] `Ctrl` + `H` 快捷键后歌曲进度条无法工作
- [ ] 更换歌曲后可能会有些不是特别影响的报错
- [ ] 打开歌曲后需要连续点击三次播放键才可以进入播放状态

## 急切的任务

- [ ] 代码整理与注释, 功能分单独代码文件

## 使用到的第三方项目

- [flet](https://github.com/flet-dev/flet) (Apache-2.0 license)
- [TinyTag](https://github.com/devsnd/tinytag) (MIT license)
- [Windows-Toasts](https://github.com/DatGuy1/Windows-Toasts) (Apache-2.0 license)