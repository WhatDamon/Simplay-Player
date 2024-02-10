import flet as ft
import tinytag, time, base64, os, platform, logging

logging.basicConfig(filename = 'player.log', format = ' %(asctime)s | %(levelname)s | %(funcName)s | %(message)s', level = logging.INFO)

logging.info("Basic libs imported")

from i18n import lang

logging.info("Languages imported")

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
audioAlbumText = None
currentOS = None

logging.info("Variable initialization complete")

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
                    logging.info("Find 'microsoft' at /proc/version")
                    os = 'wsl'
        except:
            pass
    elif 'windows' in syst:
        os = 'windows'
    elif 'bsd' in syst:
        os = 'bsd'
    logging.info("You are using " + os)
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
    logging.info("Window created")

    page.fonts = {
        "Inter": "./asset/Inter.ttc"
    }

    page.theme = ft.Theme(
        font_family = "Inter", color_scheme_seed = ft.colors.BLUE
    )
    logging.info("Assets loaded")

    def keyboardEventTrack(e: ft.KeyboardEvent):
        logging.info("Keyboard event")
        if f"{e.key}" == " ":
            playOrPauseMusic(0)
            logging.info("Press Ctrl-H to hide/show menu bar")
        if f"{e.ctrl}" == "True" and f"{e.key}" == "H":
            hideShowMenuBar(0)
            logging.info("Press space bar to play/pause audio")

    page.on_keyboard_event = keyboardEventTrack
    logging.info("keyboardEventTrack loaded")

    def windowEvent(e):
        if e.data == "close":
            closeWindow(0)

    page.window_prevent_close = True
    page.on_window_event = windowEvent
    logging.info("windowEvent loaded")

    def closeWindow(e):
        page.window_destroy()
        logging.info("Window destoryed")

    def hideShowMenuBar(e):
        if menuBar.visible == True:
            menuBar.visible = False
            logging.info("Made menu bar disappeared")
            # page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["resetMenuBar"]))
            # page.snack_bar.open = True
            # logging.info("Snack Bar loaded - resetMenuBar")
        elif menuBar.visible == False:
            menuBar.visible = True
            logging.info("Made menu bar shown")
        page.update()
        logging.info("Page updated")

    def alwaysOnTop(e):
        if page.window_always_on_top == False:
            page.window_always_on_top = True
            windowOnTop_btn.icon = ft.icons.PUSH_PIN
            windowOnTop_btn.tooltip = lang.tooltips["cancelAlwaysOnTop"]
            # page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenTop"]))
            # page.snack_bar.open = True
        elif page.window_always_on_top == True:
            page.window_always_on_top = False
            windowOnTop_btn.icon = ft.icons.PUSH_PIN_OUTLINED
            windowOnTop_btn.tooltip = lang.tooltips["alwaysOnTop"]
            # page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenUntop"]))
            # page.snack_bar.open = True
        page.update()
        logging.info("Page updated")

    def secondConvert(sec):
        return(time.strftime("%M:%S", time.gmtime(sec)))

    def audioInfoUpdate():
        global audioTag
        audioTag = tinytag.TinyTag.get(audioFile, image = True)
        if audioTag.get_image() != None:
            global audioCoverBase64
            audioCoverBase64 = base64.b64encode(audioTag.get_image())
            logging.info("Audio cover transcoded to base64")
            audioCover.src_base64 = audioCoverBase64.decode('utf-8')
            logging.info("Audio cover loaded")
        else:
            audioCoverBase64 = None
            audioCover.src_base64 = None
            audioCover.src = './asset/track.png'
            logging.info("Placeholder cover loaded")
        audioCover.update()
        logging.info("audioCover updated")
        global audioTitleText, audioArtistText, audioAlbumText
        if audioTag.title != None:
            audioTitleText = audioTag.title
            logging.info("Set audio title: " + audioTitleText)
        else:
            audioTitleText = lang.mainMenu["unknownMusic"]
            logging.info("Unknown audio title")
        if audioTag.artist != None:
            audioArtistText = audioTag.artist
            logging.info("Set audio artist: " + audioArtistText)
        else:
            audioArtistText = lang.mainMenu["unknownArtist"]
            logging.info("Unknown audio artist")
        if audioTag.album != None:
            audioAlbumText = audioTag.album
            logging.info("Find audio album and loaded: " + audioAlbumText)
        else:
            audioAlbumText = None
            logging.info("Clean audioAlbumText")
        global audioInfo
        audioInfo = "Album: " + str(audioTag.album) + "\nAlbumist: " + str(audioTag.albumartist) + "\nArtist: " + str(audioTag.artist) + "\nAudio Offset: " + str(audioTag.audio_offset) + "\nBitrate: " + str(audioTag.bitrate) + "\nBitdepth: " + str(audioTag.bitdepth) + "\nChannels: " + str(audioTag.channels) + "\nComment: " + str(audioTag.comment)+ "\nComposer: " + str(audioTag.composer) + "\nDisc: " + str(audioTag.disc) + "\nDisc Total: " + str(audioTag.disc_total) + "\nDuration: " + str(audioTag.duration) + "\nFilesize: " + str(audioTag.filesize) + "\nGenre: " + str(audioTag.genre) + "\nSamplerate: " + str(audioTag.samplerate) + "\nTitle: " + str(audioTag.title) + "\nTrack: " + str(audioTag.track) + "\nTrack Total: " + str(audioTag.track_total) + "\nYear: " + str(audioTag.year)
        logging.info("Set audio info")
        audioTitle.value = audioTitleText
        if audioAlbumText == None:
            audioArtistAndAlbum.value = audioArtistText
            logging.info("No album text loaded")
        else:
            audioArtistAndAlbum.value = audioArtistText + " · " + audioAlbumText
            logging.info("Album text loaded")
        logging.info("Load audio info to interface")
        page.update()
        logging.info("Page updated")

    def windowsToastNotify():
        toaster = WindowsToaster('Simplay Player')
        sysToast = Toast()
        if os.path.exists("./asset/simplay.png"):
            logging.info("./asset/simplay.png exist")
            sysToast.AddImage(ToastDisplayImage.fromPath('./asset/simplay.png'))
            logging.info("Toast image loaded")
        else:
            logging.warning("Cannot load toast image")
        sysToast.text_fields = [lang.mainMenu["songLoaded"], audioArtistText + " - " + audioTitleText]
        toaster.show_toast(sysToast)
        logging.info("Toast Notify")

    def pickFileResult(e: ft.FilePickerResultEvent):
        page.splash = ft.ProgressBar()
        logging.info("Splash progress bar enabled")
        page.update()
        logging.info("Page updated")
        audioPathTemp = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else None
        )
        global audioFile, lyricFile, firstPlay
        if audioPathTemp == None:
            logging.warning("Nothing Loaded")
        else:
            audioFile = audioPathTemp
            lyricFile = audioPathTemp[:-3] + "lrc"
            logging.info("File path loaded")
            logging.info("Audio path: " + audioFile)
            logging.info("Lyric path: " + lyricFile)
            if firstPlay == True:
                page.overlay.append(playAudio)
                logging.info("Append playAudio")
                firstPlay = False
            playAudio.src = audioFile
            logging.info("Set playAudio.src as audioFile")
            audioPathTemp = None
            audioInfoUpdate()
            page.title = audioArtistText + " - " + audioTitleText + "- Simplay Player"
            logging.info("Window title changed")
            global currentOS
            if currentOS == 'windows':
                windowsToastNotify()
                logging.info("Load Windows toast")
            else:
                page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["songLoaded"] + "\n" + audioArtistText+ " - " + audioTitleText))
                page.snack_bar.open = True
                logging.info("Snack Bar loaded - resetMenuBar")
        page.splash = None
        logging.info("Splash progress bar disabled")
        page.update()
        logging.info("Page updated")
        logging.info("File picked")
        
    pickFilesDialog = ft.FilePicker(on_result = pickFileResult)
    page.overlay.append(pickFilesDialog)
    logging.info("Append pickFilesDialog")

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
                logging.info("Audio Play/Resume")
                playPause_btn.icon = ft.icons.PAUSE_CIRCLE_FILLED_OUTLINED
                page.title = "▶️ " + audioArtistText + " - " + audioTitleText + "- Simplay Player"
                logging.info("Window title changed")
            elif playStatus == True:
                playStatus = False
                playAudio.pause()
                logging.info("Audio Pause")
                playPause_btn.icon = ft.icons.PLAY_CIRCLE_FILL_OUTLINED
                page.title = audioArtistText + " - " + audioTitleText + "- Simplay Player"
                logging.info("Window title changed")
            page.update()
            logging.info("Page updated")
        else:
            logging.warning("No audio file")

    def audioForward10sec(e):
        if playAudio.get_current_position() + 10000 > playAudio.get_duration():
            logging.warning("More than the total length of the song")
            playAudio.seek(playAudio.get_duration())
            logging.info("Setting position to the end of the song")
        else:
            playAudio.seek(playAudio.get_current_position() + 10000)
            logging.info("Successful forward 10sec")

    def audioBack10sec(e):
        if playAudio.get_current_position() - 10000 < 0:
            logging.warning("Less than the start of the song")
            playAudio.seek(0)
            logging.info("Setting position to the start of the song")
        else:
            playAudio.seek(playAudio.get_current_position() - 10000)
            logging.info("Successful back 10sec")

    def rateChangeTo05(e):
        playAudio.playback_rate = 0.5
        logging.info("Set audio rate to 0.5x")
        playAudio.update()
        logging.info("playAudio updated")
    
    def rateChangeTo10(e):
        playAudio.playback_rate = 1.0
        logging.info("Set audio rate to 1x")
        playAudio.update()
        logging.info("playAudio updated")

    def rateChangeTo15(e):
        playAudio.playback_rate = 1.5
        logging.info("Set audio rate to 1.5x")
        playAudio.update()
        logging.info("playAudio updated")

    def rateChangeTo20(e):
        playAudio.playback_rate = 2.0
        logging.info("Set audio rate to 2.0x")
        playAudio.update()
        logging.info("playAudio updated")

    def autoKeepAudioProgress(e):
        if progressChanging == False:
            audioProgressBar.value = playAudio.get_current_position() / playAudio.get_duration() * 1000
        currentLength = secondConvert(playAudio.get_current_position() // 1000)
        totalLength = secondConvert(playAudio.get_duration() // 1000)
        audioProgressStatus.value = currentLength + "/" + totalLength
        page.update()

    def enableOrDisableLoop(e):    
        global loopOpen
        if loopOpen == False:
            loopOpen = True
            playAudio.release_mode = ft.audio.ReleaseMode.LOOP
            playInLoop_btn.icon = ft.icons.REPEAT_ONE_ON
            logging.info("Loop enabled")
        elif loopOpen == True:
            loopOpen = False
            playAudio.release_mode = ft.audio.ReleaseMode.RELEASE
            playInLoop_btn.icon = ft.icons.REPEAT_ONE
            logging.info("Loop disabled")
        page.update()
        logging.info("Page updated")
    
    def autoStopKeepAudioProgress(e):
        global progressChanging
        progressChanging = True
        logging.info("Set progressChanging as True")

    def progressCtrl(e):
        global progressChanging
        progressChanging = False
        logging.info("Set progressChanging as False")
        playAudio.seek(int(playAudio.get_duration() * (audioProgressBar.value / 1000)))
        logging.info("Audio seek completed")

    def openVolumePanel(e):
        if volume_panel.visible == True:
            volume_panel.visible = False
            logging.info("Volume panel not visiable")
        elif volume_panel.visible == False:
            volume_panel.visible = True
            logging.info("Volume panel visiable")
        page.update()
        logging.info("Page updated")

    def volumeChange(e):
        playAudio.volume = volume_silder.value / 100
        playAudio.update()
        logging.info("playAudio updated")
        if volume_silder.value >= 50:
            volume_btn.icon = ft.icons.VOLUME_UP_OUTLINED
        elif volume_silder.value == 0:
            volume_btn.icon = ft.icons.VOLUME_MUTE_OUTLINED
        elif volume_silder.value < 50:
            volume_btn.icon = ft.icons.VOLUME_DOWN_OUTLINED
        page.update()
        logging.info("Page updated")

    def audioListCtrl(e):
        if audioListShown == False:
            showAudioList(0)
        elif audioListShown == True:
            hideAudioList(0)

    def showAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(0, 0)
        audioListShown = True
        logging.info("Audio list shown")
        audioList_menu.update()
        logging.info("audioList_menu updated")

    def hideAudioList(e):
        global audioListShown
        audioList_menu.offset = ft.transform.Offset(-2, 0)
        audioListShown = False
        logging.info("Audio list disappeared")
        audioList_menu.update()
        logging.info("audioList_menu updated")

    def openAudioInfoDlg(e):
        audioInfo_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["moreInfo"]),
            content = ft.Text(value = audioInfo, size = 10)
        )
        page.dialog = audioInfo_dlg
        audioInfo_dlg.open = True
        logging.info("Dialog audioInfo_dlg opened")
        page.update()
        logging.info("Page updated")

    def openAboutDlg(e):
        about_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["about"]),
            content = ft.Text("Simplay Player by What_Damon\n\nVersion: 1.0.0\nPowered by: Flet, Tinytag\n\nRuning under Python " + platform.python_version() + "\nOS: " + platform.platform())
        )
        page.dialog = about_dlg
        about_dlg.open = True
        logging.info("Dialog about_dlg opened")
        page.update()
        logging.info("Page updated")

    def stereoBalanceNotSupport():
        logging.warning("Not support with macOS")
        page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["notSupportMacOS"]))
        page.snack_bar.open = True
        logging.info("Snack Bar loaded - notSupportMacOS")

    def balanceLeft(e):
        if currentOS == "darwin":
            stereoBalanceNotSupport()
        else:
            playAudio.balance -= 0.1
            logging.info("Channel left shift to " + str(playAudio.balance))
            playAudio.update()
            logging.info("playAudio updated")

    def balanceRight(e):
        if currentOS == "darwin":
            stereoBalanceNotSupport()
        else:
            playAudio.balance += 0.1
            logging.info("Channel right shift to " + str(playAudio.balance))
            playAudio.update()
            logging.info("playAudio updated")

    def balanceMiddle(e):
        if currentOS == "darwin":
            stereoBalanceNotSupport()
        else:
            playAudio.balance = 0
            logging.info("Channel set banlace to 0")
            playAudio.update()
            logging.info("playAudio updated")

    playAudio = ft.Audio(
        autoplay = False,
        volume = 1,
        balance = 0,
        on_loaded = lambda _: logging.info("Audio loaded: " + audioFile + " => " + audioArtistText + " - " + audioTitleText),
        on_duration_changed = lambda e: logging.info("Duration changed:" + e.data),
        on_position_changed = autoKeepAudioProgress,
        on_state_changed = lambda e: logging.info("State changed:" + e.data),
        on_seek_complete = lambda _: logging.info("Seek complete"),
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
                            on_click = lambda _: pickFilesDialog.pick_files(allowed_extensions = ["mp3", "flac", "m4a", "wav", "aac"]),
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
    audioArtistAndAlbum = ft.Text(audioArtistText, size = 18, opacity = 90)
    audioProgressStatus = ft.Text("00:00/00:00", size = 15, opacity = 90)
    audioDetail = ft.Column(controls = [audioTitle, audioArtistAndAlbum, audioProgressStatus])
    audioBasicInfo = ft.Row(controls = [audioCover, audioDetail])

    audioProgressBar = ft.Slider(min = 0, max = 1000, tooltip = lang.tooltips["audioPosition"], on_change_start = autoStopKeepAudioProgress, on_change_end = progressCtrl)

    playPause_btn = ft.IconButton(
        icon = ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
        tooltip = lang.tooltips["playOrPause"],
        icon_size = 30,
        on_click = playOrPauseMusic
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
    
    playInLoop_btn = ft.IconButton(
        icon = ft.icons.REPEAT_ONE_OUTLINED,
        tooltip = lang.tooltips["playInLoop"],
        icon_size = 20,
        on_click = enableOrDisableLoop
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

    playbackCtrl_row = ft.Row(controls = [playPause_btn, volume_btn, volume_panel])
    moreBtns_row = ft.Row(controls = [playInLoop_btn, audioList_btn, audioInfo_btn, settings_btn])
    btns_row = ft.Row(controls = [playbackCtrl_row, moreBtns_row], alignment = ft.MainAxisAlignment.SPACE_BETWEEN)

    page.overlay.append(audioList_menu)
    logging.info("Append audioList_menu")
    page.add(ft.Column(controls = [ft.Row(controls = [menuBar]), audioBasicInfo, audioProgressBar, btns_row, lyric_text]))
    logging.info("Window initialization complete")

if __name__ == '__main__':
    logging.info("Program start")
    detectOS()
    lang.loadLang()
    if currentOS == 'wsl':
        print(lang.infomation["wslWarning"])
        logging.warning("Using WSL")
    if currentOS == 'cygwin':
        print(lang.infomation["cygwinWarning"])
        logging.warning("Using Cygwin")
    if currentOS == "windows":
        from windows_toasts import Toast, ToastDisplayImage, WindowsToaster
        logging.info("Lib Windows-Toasts imported")
    else:
        print(lang.infomation["nonTestWarning"])
        logging.warning("Non-test OS")
    if currentOS == "bsd" or currentOS == "unknown":
        print(lang.mainMenu("unsupportWithYourOS"))
        logging.error("Unsupport with the current os: " + currentOS)
        exit()
    audioArtistText = lang.mainMenu["unknownArtist"]
    audioTitleText = lang.mainMenu["unknownMusic"]
    audioInfo = lang.mainMenu["none"]
    logging.info("Basic initialization complete")
    ft.app(target = main)