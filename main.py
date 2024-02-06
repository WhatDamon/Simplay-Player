import flet as ft
import tinytag, time, base64, os, platform
from i18n import lang

audioFile = None
lyricFile = None
firstPlay = True
playStatus = False
loopOpen = False
audioListShown = False
progressChanging = False
audioTag = None
audioCoverBase64 = None
audioInfo = None
audioTitleText = None
audioArtistText = None
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
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["resetMenuBar"]))
            page.snack_bar.open = True
        elif menuBar.visible == False:
            menuBar.visible = True
        page.update()

    def alwaysOnTop(e):
        if page.window_always_on_top == False:
            page.window_always_on_top = True
            windowOnTop_btn.icon = ft.icons.PUSH_PIN
            windowOnTop_btn.tooltip = lang.tooltips["cancelAlwaysOnTop"]
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenTop"]))
            page.snack_bar.open = True
        elif page.window_always_on_top == True:
            page.window_always_on_top = False
            windowOnTop_btn.icon = ft.icons.PUSH_PIN_OUTLINED
            windowOnTop_btn.tooltip = lang.tooltips["alwaysOnTop"]
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenUntop"]))
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
            audioTitleText = lang.mainMenu["unknownMusic"]
        if audioTag.artist != None:
            audioArtistText = audioTag.artist
        else:
            audioArtistText = lang.mainMenu["unknownArtist"]
        global audioInfo
        audioInfo = "Album: " + str(audioTag.album) + "\nAlbumist: " + str(audioTag.albumartist) + "\nArtist: " + str(audioTag.artist) + "\nAudio Offset: " + str(audioTag.audio_offset) + "\nBitrate: " + str(audioTag.bitrate) + "\nBitdepth: " + str(audioTag.bitdepth) + "\nChannels: " + str(audioTag.channels) + "\nComment: " + str(audioTag.comment)+ "\nComposer: " + str(audioTag.composer) + "\nDisc: " + str(audioTag.disc) + "\nDisc Total: " + str(audioTag.disc_total) + "\nDuration: " + str(audioTag.duration) + "\nFilesize: " + str(audioTag.filesize) + "\nGenre: " + str(audioTag.genre) + "\nSamplerate: " + str(audioTag.samplerate) + "\nTitle: " + str(audioTag.title) + "\nTrack: " + str(audioTag.track) + "\nTrack Total: " + str(audioTag.track_total) + "\nYear: " + str(audioTag.year)
        audioTitle.value = audioTitleText
        audioArtist.value = audioArtistText
        page.update()

    def windowsToastNotify():
        toaster = WindowsToaster('Simplay Player')
        sysToast = Toast()
        if os.path.exists("./asset/simplay.png"):
            sysToast.AddImage(ToastDisplayImage.fromPath('./asset/simplay.png'))
        sysToast.text_fields = [lang.mainMenu["songLoaded"], audioArtistText + " - " + audioTitleText]
        toaster.show_toast(sysToast)

    def pickFileResult(e: ft.FilePickerResultEvent):
        page.splash = ft.ProgressBar()
        page.update()
        audioPathTemp = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else "Cancelled!"
        )
        global audioFile, lyricFile, firstPlay
        if audioPathTemp == None:
            pass
        else:
            audioFile = audioPathTemp
            lyricFile = audioPathTemp[:-3] + "lrc"
            if firstPlay == True:
                page.overlay.append(playAudio)
                firstPlay = False
            playAudio.src = audioFile
        audioPathTemp = None
        audioInfoUpdate()
        page.title = audioArtistText + " - " + audioTitleText + "- Simplay Player"
        global currentOS
        if currentOS == 'windows':
            windowsToastNotify()
        else:
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.menuBar["songLoaded"] + "\n" + audioArtistText+ " - " + audioTitleText))
            page.snack_bar.open = True
        page.splash = None
        page.update()
        
    pickFilesDialog = ft.FilePicker(on_result = pickFileResult)
    page.overlay.append(pickFilesDialog)

    """
    def lyricExistAndRead():
        if os.path.exists(lyricFile):
            with open(lyricFile,'r',encoding = 'utf-8') as f:
                content = f.read()
        else:
            pass
    """

    def playOrPauseMusic(e):
        global audioFile
        if audioFile != None:
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

    def audioForward10sec(e):
        if playAudio.get_current_position() + 10000 > playAudio.get_duration():
            playAudio.seek(playAudio.get_duration())
        else:
            playAudio.seek(playAudio.get_current_position() + 10000)

    def audioBack10sec(e):
        if playAudio.get_current_position() - 10000 < 0:
            playAudio.seek(0)
        else:
            playAudio.seek(playAudio.get_current_position() - 10000)

    def rateChangeTo05(e):
        playAudio.playback_rate = 0.5
        playAudio.update()
    
    def rateChangeTo10(e):
        playAudio.playback_rate = 1.0
        playAudio.update()

    def rateChangeTo15(e):
        playAudio.playback_rate = 1.5
        playAudio.update()

    def rateChangeTo20(e):
        playAudio.playback_rate = 2.0
        playAudio.update()

    def autoKeepAudioProgress(e):
        if progressChanging == False:
            audioProgressBar.value = playAudio.get_current_position() / playAudio.get_duration() * 1000
        global loopOpen
        if playAudio.get_current_position() == playAudio.get_duration() and loopOpen == True:
            playAudio.seek(0)
        currentLength = secondConvert(playAudio.get_current_position() // 1000)
        totalLength = secondConvert(playAudio.get_duration() // 1000)
        audioProgressStatus.value = currentLength + "/" + totalLength
        page.update()

    """
    def enableOrDisableLoop(e):
        global loopOpen
        if loopOpen == False:
            loopOpen = True
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["enableLoop"]))
            page.snack_bar.open = True
        elif loopOpen == True:
            loopOpen = False
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["disableLoop"]))
            page.snack_bar.open = True
        page.update()
    """
    
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

    def audioListCtrl(e):
        if audioListShown == False:
            showAudioList(0)
        elif audioListShown == True:
            hideAudioList(0)

    def showAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(0, 0)
        audioListShown = True
        audioList_menu.update()

    def hideAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(-2, 0)
        audioListShown = False
        audioList_menu.update()

    def openAudioInfoDlg(e):
        audioInfo_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["moreInfo"]),
            content = ft.Text(value = audioInfo, size = 10)
        )
        page.dialog = audioInfo_dlg
        audioInfo_dlg.open = True
        page.update()

    def openAboutDlg(e):
        about_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["about"]),
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
                    tooltip = lang.tooltips["alwaysOnTop"],
                    on_click = alwaysOnTop
                )

    menuBar = ft.MenuBar(
        expand = True,
        controls = [
            ft.Row(controls = [
                ft.SubmenuButton(
                    content = ft.Text(value = lang.menuBar["files"]),
                    controls = [
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["openFile"]),
                            leading = ft.Icon(ft.icons.FILE_OPEN_OUTLINED),
                            on_click = lambda _: pickFilesDialog.pick_files(allowed_extensions=["mp3", "flac", "m4a", "wav", "aac"]),
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["getFromNeteaseMusic"]),
                            leading = ft.Icon(ft.icons.MUSIC_NOTE_OUTLINED)
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["exit"]),
                            leading = ft.Icon(ft.icons.EXIT_TO_APP_OUTLINED),
                            on_click = closeWindow
                        )
                    ]
                ),
                ft.SubmenuButton(
                    content = ft.Text(value = lang.menuBar["media"]),
                    controls = [
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["channels"]),
                            leading = ft.Icon(ft.icons.SPEAKER_GROUP_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["balance"]),
                                    leading = ft.Icon(ft.icons.WIDTH_NORMAL),
                                    on_click = balanceMiddle
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shiftLeft"]),
                                    leading = ft.Icon(ft.icons.ARROW_BACK_OUTLINED),
                                    on_click = balanceLeft
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shiftRight"]),
                                    leading = ft.Icon(ft.icons.ARROW_FORWARD_OUTLINED),
                                    on_click = balanceRight
                                )
                            ]
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["position"]),
                            leading = ft.Icon(ft.icons.TIMER_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["forward10s"]),
                                    leading = ft.Icon(ft.icons.ARROW_FORWARD_OUTLINED),
                                    on_click = audioForward10sec
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["back10s"]),
                                    leading = ft.Icon(ft.icons.ARROW_BACK_OUTLINED),
                                    on_click = audioBack10sec
                                )
                            ]
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["times"]),
                            leading = ft.Icon(ft.icons.SLOW_MOTION_VIDEO_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["0.5x"]),
                                    leading = ft.Icon(ft.icons.ARROW_BACK_OUTLINED),
                                    on_click = rateChangeTo05
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["1x"]),
                                    leading = ft.Icon(ft.icons.STOP_OUTLINED),
                                    on_click = rateChangeTo10
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["1.5x"]),
                                    leading = ft.Icon(ft.icons.ARROW_FORWARD_OUTLINED),
                                    on_click = rateChangeTo15
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["2x"]),
                                    leading = ft.Icon(ft.icons.ROCKET_LAUNCH_OUTLINED),
                                    on_click = rateChangeTo20
                                )
                            ]
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["volume"]),
                            leading = ft.Icon(ft.icons.VOLUME_UP_OUTLINED),
                            on_click = openVolumePanel
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["audioInfo"]),
                            leading = ft.Icon(ft.icons.INFO_OUTLINE),
                            on_click = openAudioInfoDlg
                        )
                    ]
                ),
                ft.SubmenuButton(
                    content = ft.Text(value = lang.menuBar["help"]),
                    controls = [
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["about"]),
                            leading = ft.Icon(ft.icons.QUESTION_MARK_OUTLINED),
                            on_click = openAboutDlg
                        )
                    ]
                ),
                windowOnTop_btn,
                ft.IconButton(
                        icon = ft.icons.KEYBOARD_ARROW_UP_OUTLINED,
                        tooltip = lang.tooltips["hideMenuBar"],
                        on_click = hideShowMenuBar
                )
                ]
            )
        ],
        visible = True
    )

    audioCover = ft.Image(src = './asset/track.png', width = 128, height = 128, border_radius = 5)
    audioTitle = ft.Text(audioTitleText, weight = ft.FontWeight.BOLD, size = 25, overflow = ft.TextOverflow.ELLIPSIS)
    audioArtist = ft.Text(audioArtistText, size = 18, opacity = 90)
    audioProgressStatus = ft.Text("00:00/00:00", size = 15, opacity = 90)
    audioDetail = ft.Column(controls = [audioTitle, audioArtist, audioProgressStatus])
    audioBasicInfo = ft.Row(controls = [audioCover, audioDetail])

    audioProgressBar = ft.Slider(min = 0, max = 1000, tooltip = lang.tooltips["audioPosition"], on_change_start = autoStopKeepAudioProgress, on_change_end = progressCtrl)

    playPause_btn = ft.IconButton(
        icon = ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
        tooltip = lang.tooltips["playOrPause"],
        icon_size = 30,
        on_click = playOrPauseMusic
    )

    playInLoop = ft.IconButton(
        icon = ft.icons.LOOP_OUTLINED,
        tooltip = lang.tooltips["playInLoop"],
        icon_size = 20,
        visible = False
        # on_click = enableOrDisableLoop
    )

    volume_btn = ft.IconButton(
        icon = ft.icons.VOLUME_UP_OUTLINED,
        tooltip = lang.tooltips["volume"],
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
            tooltip = lang.tooltips["songList"],
            icon_size = 20,
            on_click = audioListCtrl
        )
    
    audioList_menu = ft.Container(
        content = ft.Column(
            [
                ft.Row(
                    controls = [
                        ft.Text(value = lang.songList["songList"], size = 20, weight = ft.FontWeight.BOLD),
                        ft.IconButton(icon = ft.icons.CLOSE, on_click = hideAudioList)
                    ],
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.ListTile(
                    leading = ft.Icon(ft.icons.CONSTRUCTION_OUTLINED, color = ft.colors.AMBER),
                    title = ft.Text(value = lang.songList["construction"], color = ft.colors.AMBER)
                )
            ],
        ),
        left = 10,
        top = 10,
        width = 250,
        height = 400,
        bgcolor = ft.colors.SURFACE_VARIANT,
        border_radius = 5,
        padding = 8,
        offset = ft.transform.Offset(-2, 0),
        animate_offset = ft.animation.Animation(200, ft.AnimationCurve.EASE_IN),
    )
    
    audioInfo_btn = ft.IconButton(
            icon = ft.icons.INFO_OUTLINE,
            tooltip = lang.tooltips["audioInfo"],
            icon_size = 20,
            on_click = openAudioInfoDlg
        )

    settings_btn = ft.IconButton(
            icon = ft.icons.SETTINGS_OUTLINED,
            tooltip = lang.tooltips["settings"],
            icon_size = 20,
            visible = False
        )
    
    lyric_text = ft.Text(size = 20)

    playbackCtrl_row = ft.Row(controls = [playPause_btn, playInLoop, volume_btn, volume_panel])
    moreBtns_row = ft.Row(controls = [audioList_btn, audioInfo_btn, settings_btn])
    btns_row = ft.Row(controls = [playbackCtrl_row, moreBtns_row], alignment = ft.MainAxisAlignment.SPACE_BETWEEN)

    page.overlay.append(audioList_menu)
    page.add(ft.Column(controls = [ft.Row(controls = [menuBar]), audioBasicInfo, audioProgressBar, btns_row, lyric_text]))

if __name__ == '__main__':
    detectOS()
    lang.loadLang()
    if currentOS == 'wsl':
        print(lang.infomation["wslWarning"])
    if currentOS == 'cygwin':
        print(lang.infomation["cygwinWarning"])
    if currentOS == "windows":
        from windows_toasts import Toast, ToastDisplayImage, WindowsToaster
    else:
        print(lang.infomation["nonTestWarning"])
    audioArtistText = lang.mainMenu["unknownArtist"]
    audioTitleText = lang.mainMenu["unknownMusic"]
    audioInfo = lang.mainMenu["none"]
    ft.app(target = main)