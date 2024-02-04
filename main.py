import flet as ft
import tinytag, time, base64, os, platform

audioFile = None
lyricFile = None
firstPlay = True
playStatus = False
progressChanging = False
audioTag = None
audioCoverBase64 = None
audioInfo = "无"
audioTitleText = "未知歌曲"
audioArtistText = "未知作曲家"
currentOS = None

def detectOS():
    syst = platform.system().lower()
    os = 'unknown'
    if 'cygwin' in syst:
        os = 'cygwin'
    elif 'darwin' in syst:
        os = 'darwin'
    elif 'linux' in syst:
        os = 'linux'
        try:
            with open('/proc/version', 'r') as f:
                if 'microsoft' in f.read().lower():
                    os = 'wsl'
        except: pass
    elif 'windows' in syst:
        os = 'windows'
    elif 'bsd' in syst:
        os = 'bsd'
    global currentOS
    currentOS = os

def main(page: ft.Page):
    page.window_left = 200
    page.window_top = 100
    page.window_height = 600
    page.window_width = 800
    page.window_min_height = 350
    page.window_min_width = 500
    page.padding = 10
    page.title = "Simplay Player"

    page.fonts = {
        "Inter": "./asset/Inter.ttc"
    }

    page.theme = ft.Theme(
        font_family = "Inter", color_scheme_seed = ft.colors.BLUE
    )

    def keyboardEventTrack(e: ft.KeyboardEvent):
        if f"{e.key}" == " ":
            playOrPauseMusic(0)
        if f"{e.ctrl}" and f"{e.key}" == "H":
            hideShowMenuBar(0)

    page.on_keyboard_event = keyboardEventTrack

    def closeWindow(e):
        page.window_close()

    def hideShowMenuBar(e):
        if menuBar.visible == True:
            menuBar.visible = False
            page.snack_bar = ft.SnackBar(ft.Text("按下 Ctrl+H 复原顶栏!"))
            page.snack_bar.open = True
        elif menuBar.visible == False:
            menuBar.visible = True
        page.update()

    def alwaysOnTop(e):
        if page.window_always_on_top == False:
            page.window_always_on_top = True
            windowOnTop_btn.icon = ft.icons.PUSH_PIN
            windowOnTop_btn.tooltip = "取消置顶"
            page.snack_bar = ft.SnackBar(ft.Text("已置顶"))
            page.snack_bar.open = True
        elif page.window_always_on_top == True:
            page.window_always_on_top = False
            windowOnTop_btn.icon = ft.icons.PUSH_PIN_OUTLINED
            windowOnTop_btn.tooltip = "置顶"
            page.snack_bar = ft.SnackBar(ft.Text("已取消置顶"))
            page.snack_bar.open = True
        page.update()

    def secondConvert(sec):
        return(time.strftime("%M:%S", time.gmtime(sec)))

    def audioInfoUpdate():
        global audioTag
        audioTag = tinytag.TinyTag.get(audioFile, image = True)
        if audioTag.get_image() != None:
            global audioCoverBase64
            audioCoverBase64 = base64.b64encode(audioTag.get_image())
            audioCover.src_base64 = audioCoverBase64.decode('utf-8')
        else:
            audioCoverBase64 = None
            audioCover.src = './asset/track.png'
        audioCover.update()
        global audioTitleText, audioArtistText
        if audioTag.title != None:
            audioTitleText = audioTag.title
        else:
            audioTitleText = "未知歌曲"
        if audioTag.artist != None:
            audioArtistText = audioTag.artist
        else:
            audioArtistText = "未知作曲家"
        global audioInfo
        audioInfo = "Album: " + str(audioTag.album) + "\nAlbumist: " + str(audioTag.albumartist) + "\nArtist: " + str(audioTag.artist) + "\nAudio Offset: " + str(audioTag.audio_offset) + "\nBitrate: " + str(audioTag.bitrate) + "\nBitdepth: " + str(audioTag.bitdepth) + "\nChannels: " + str(audioTag.channels) + "\nComment: " + str(audioTag.comment)+ "\nComposer: " + str(audioTag.composer) + "\nDisc: " + str(audioTag.disc) + "\nDisc Total: " + str(audioTag.disc_total) + "\nDuration: " + str(audioTag.duration) + "\nFilesize: " + str(audioTag.filesize) + "\nGenre: " + str(audioTag.genre) + "\nSamplerate: " + str(audioTag.samplerate) + "\nTitle: " + str(audioTag.title) + "\nTrack: " + str(audioTag.track) + "\nTrack Total: " + str(audioTag.track_total) + "\nYear: " + str(audioTag.year)
        audioTitle.value = audioTitleText
        audioArtist.value = audioArtistText
        page.update()

    def windowsToastNotify():
        toaster = WindowsToaster('Simplay Player')
        sysToast = Toast()
        sysToast.AddImage(ToastDisplayImage.fromPath('./asset/simplay.png'))
        sysToast.text_fields = ["已加载歌曲: ", audioArtistText + " - " + audioTitleText]
        toaster.show_toast(sysToast)

    def pickFileResult(e: ft.FilePickerResultEvent):
        audioPathTemp = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )
        global audioFile, lyricFile
        if audioPathTemp == None:
            pass
        else:
            audioFile = audioPathTemp
            lyricFile = audioPathTemp[:-3] + "lrc"
        audioPathTemp = None
        playAudio.src = audioFile
        audioInfoUpdate()
        global currentOS
        if currentOS == 'windows':
            windowsToastNotify()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("已加载歌曲：\n" + audioArtistText+ " - " + audioTitleText))
            page.snack_bar.open = True
        page.update()
        
    pickFilesDialog = ft.FilePicker(on_result=pickFileResult)
    page.overlay.append(pickFilesDialog)

    """
    def lyricExistAndRead():
        if os.path.exists(lyricFile):
            with open(lyricFile,'r',encoding='utf-8') as f:
                content = f.read()
        else:
            pass
    """

    def playOrPauseMusic(e):
        global firstPlay, audioFile
        if audioFile != None:
            if firstPlay == True:
                page.overlay.append(playAudio)
                firstPlay = False
            audioInfoUpdate()
            global playStatus
            if playStatus == False:
                playStatus = True
                playAudio.resume()
                playPause_btn.icon = ft.icons.PAUSE_CIRCLE_FILLED_OUTLINED
                page.title = "▶️ " + audioArtistText + " - " + audioTitleText + "- Simplay Player"
            elif playStatus == True:
                playStatus = False
                playAudio.pause()
                playPause_btn.icon = ft.icons.PLAY_CIRCLE_FILL_OUTLINED
                page.title = audioArtistText + " - " + audioTitleText + "- Simplay Player"
            page.update()

    def autoKeepAudioProgress(e):
        if progressChanging == False:
            audioProgressBar.value = playAudio.get_current_position() / playAudio.get_duration() * 1000
        currentLength = secondConvert(playAudio.get_current_position() // 1000)
        totalLength = secondConvert(playAudio.get_duration() // 1000)
        audioProgressStatus.value = currentLength + "/" + totalLength
        page.update()

    def autoStopKeepAudioProgress(e):
        global progressChanging
        progressChanging = True

    def progressCtrl(e):
        global progressChanging
        progressChanging = False
        playAudio.seek(int(playAudio.get_duration() * (audioProgressBar.value / 1000)))

    def openVolumePanel(e):
        if volume_panel.visible == True:
            volume_panel.visible = False
        elif volume_panel.visible == False:
            volume_panel.visible = True
        page.update()

    def volumeChange(e):
        playAudio.volume = volume_silder.value / 100
        playAudio.update()
        if volume_silder.value >= 50:
            volume_btn.icon = ft.icons.VOLUME_UP_OUTLINED
        elif volume_silder.value == 0:
            volume_btn.icon = ft.icons.VOLUME_MUTE_OUTLINED
        elif volume_silder.value < 50:
            volume_btn.icon = ft.icons.VOLUME_DOWN_OUTLINED
        page.update()

    def openAudioInfoDlg(e):
        audioInfo_dlg = ft.AlertDialog(
            title = ft.Text("详细信息"),
            content = ft.Text(value = audioInfo, size = 10)
        )
        page.dialog = audioInfo_dlg
        audioInfo_dlg.open = True
        page.update()

    def openAboutDlg(e):
        about_dlg = ft.AlertDialog(
            title = ft.Text("关于"),
            content = ft.Text("Simplay Player by What_Damon\n\nVersion: 1.0.0_experimentalTest\nPowered by: Flet, Tinytag\n\nRuning under Python " + platform.python_version() + "\nOS: " + platform.platform())
        )
        page.dialog = about_dlg
        about_dlg.open = True
        page.update()

    def balanceLeft(e):
        playAudio.balance -= 0.1
        playAudio.update()

    def balanceRight(e):
        playAudio.balance += 0.1
        playAudio.update()

    def balanceMiddle(e):
        playAudio.balance = 0.5
        playAudio.update()

    playAudio = ft.Audio(
        autoplay = False,
        volume = 1,
        balance = 0,
        on_loaded = lambda _: print("Loaded"),
        on_duration_changed = lambda e: print("Duration changed:", e.data),
        on_position_changed = autoKeepAudioProgress,
        on_state_changed = lambda e: print("State changed:", e.data),
        on_seek_complete = lambda _: print("Seek complete"),
    )

    windowOnTop_btn = ft.IconButton(
                    icon = ft.icons.PUSH_PIN_OUTLINED,
                    tooltip = "置顶",
                    on_click = alwaysOnTop
                )

    menuBar = ft.MenuBar(
        expand = True,
        controls = [
            ft.Row(controls = [
                ft.SubmenuButton(
                    content = ft.Text("文件"),
                    controls = [
                        ft.MenuItemButton(
                            content = ft.Text("打开"),
                            leading = ft.Icon(ft.icons.FILE_OPEN_OUTLINED),
                            on_click = lambda _: pickFilesDialog.pick_files(allowed_extensions=["mp3", "ogg", "flac", "m4a", "wav"]),
                        ),
                        ft.MenuItemButton(
                            content = ft.Text("从网易云中获取"),
                            leading = ft.Icon(ft.icons.MUSIC_NOTE_OUTLINED)
                        ),
                        ft.MenuItemButton(
                            content = ft.Text("退出"),
                            leading = ft.Icon(ft.icons.EXIT_TO_APP_OUTLINED),
                            on_click = closeWindow
                        )
                    ]
                ),
                ft.SubmenuButton(
                    content = ft.Text("媒体"),
                    controls = [
                        ft.SubmenuButton(
                            content = ft.Text("左右声道"),
                            leading = ft.Icon(ft.icons.SPEAKER_GROUP_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text("平衡"),
                                    leading = ft.Icon(ft.icons.WIDTH_NORMAL),
                                    on_click = balanceMiddle
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text("向左移"),
                                    leading = ft.Icon(ft.icons.ARROW_BACK_OUTLINED),
                                    on_click = balanceLeft
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text("向右移"),
                                    leading = ft.Icon(ft.icons.ARROW_FORWARD_OUTLINED),
                                    on_click = balanceRight
                                ),
                            ]
                        ),
                        ft.MenuItemButton(
                            content = ft.Text("音量"),
                            leading = ft.Icon(ft.icons.VOLUME_UP_OUTLINED),
                            on_click = openVolumePanel
                        ),
                        ft.MenuItemButton(
                            content = ft.Text("媒体信息"),
                            leading = ft.Icon(ft.icons.INFO_OUTLINE),
                            on_click = openAudioInfoDlg
                        )
                    ]
                ),
                ft.SubmenuButton(
                    content = ft.Text("帮助"),
                    controls = [
                        ft.MenuItemButton(
                            content = ft.Text("关于"),
                            leading = ft.Icon(ft.icons.QUESTION_MARK_OUTLINED),
                            on_click = openAboutDlg
                        )
                    ]
                ),
                windowOnTop_btn,
                ft.IconButton(
                        icon = ft.icons.KEYBOARD_ARROW_UP_OUTLINED,
                        tooltip = "隐藏顶栏",
                        on_click = hideShowMenuBar
                )
                ]
            )
        ],
        visible = True
    )

    audioCover = ft.Image(src = './asset/track.png', width = 128, height = 128, border_radius = 6)
    audioTitle = ft.Text(audioTitleText, weight = ft.FontWeight.BOLD, size = 25, overflow = ft.TextOverflow.ELLIPSIS)
    audioArtist = ft.Text(audioArtistText, size = 18, opacity = 90)
    audioProgressStatus = ft.Text("00:00/00:00", size = 15, opacity = 90)
    audioDetail = ft.Column(controls = [audioTitle, audioArtist, audioProgressStatus])
    audioBasicInfo = ft.Row(controls = [audioCover, audioDetail])

    audioProgressBar = ft.Slider(min = 0, max = 1000, tooltip = "歌曲进度", on_change_start = autoStopKeepAudioProgress, on_change_end = progressCtrl)

    playPause_btn = ft.IconButton(
        icon = ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
        tooltip = "播放/暂停",
        icon_size = 30,
        on_click = playOrPauseMusic
    )

    volume_btn = ft.IconButton(
        icon = ft.icons.VOLUME_UP_OUTLINED,
        tooltip = "音量",
        icon_size = 20,
        on_click = openVolumePanel
    )

    volume_silder = ft.Slider(min = 0, max = 100, divisions = 100, label = "{value}%", value = 100, on_change = volumeChange)

    volume_panel = ft.Card(
            content = volume_silder,
            visible = False,
            height = 46,
            width = 200
        )

    audioList_btn = ft.IconButton(
            icon = ft.icons.LIBRARY_MUSIC_OUTLINED,
            tooltip = "歌单",
        )
    
    audioInfo_btn = ft.IconButton(
            icon = ft.icons.INFO_OUTLINE,
            tooltip = "歌曲信息",
            on_click = openAudioInfoDlg
        )

    settings_btn = ft.IconButton(
            icon = ft.icons.SETTINGS_OUTLINED,
            tooltip = "设置",
        )
    
    lyric_text = ft.Text(size = 20)

    playbackCtrl_row = ft.Row(controls = [playPause_btn, volume_btn, volume_panel])
    moreBtns_row = ft.Row(controls = [audioList_btn, audioInfo_btn, settings_btn])
    btns_row = ft.Row(controls = [playbackCtrl_row, moreBtns_row], alignment = ft.MainAxisAlignment.SPACE_BETWEEN)

    page.add(ft.Column(controls = [ft.Row(controls = [menuBar]), audioBasicInfo, audioProgressBar, btns_row, lyric_text]))

if __name__ == '__main__':
    detectOS()
    if currentOS == 'wsl':
        print("发现您正在使用 WSL, 实际上, 我们更推荐您直接使用 Windows 版本以避免潜在的 BUG")
    if currentOS == "windows":
        from windows_toasts import Toast, ToastDisplayImage, WindowsToaster
    else:
        print("除 Windows 外, 该软件没有做过稳定性测试, 可能会存在一些开发者也不清楚的 BUG 需要修复")
    ft.app(target = main)