import flet as ft
import platform, logging, os
from lib import work # 工作模块
logging.basicConfig(filename = 'player.log', format = ' %(asctime)s | %(levelname)s | %(funcName)s | %(message)s', level = logging.INFO)
from i18n import lang
logging.info("Variable initialization complete")

audioFile = None
audioListShown = False
firstPlay = True

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
            work.playOrPauseMusic(0)
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
            '''
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenTop"]))
            page.snack_bar.open = True
            '''
        elif page.window_always_on_top == True:
            page.window_always_on_top = False
            windowOnTop_btn.icon = ft.icons.PUSH_PIN_OUTLINED
            windowOnTop_btn.tooltip = lang.tooltips["alwaysOnTop"]
            '''
            page.snack_bar = ft.SnackBar(ft.Text(value = lang.mainMenu["beenUntop"]))
            page.snack_bar.open = True
            '''
        page.update()
        logging.info("Page updated")
    
    def windowsToastNotify():
        from windows_toasts import Toast, ToastDisplayImage, WindowsToaster    
        toaster = WindowsToaster('Simplay Player')
        sysToast = Toast()
        if os.path.exists("./asset/simplay.png"):
            logging.info("./asset/simplay.png exist")
            sysToast.AddImage(ToastDisplayImage.fromPath('./asset/simplay.png'))
            logging.info("Toast image loaded")
        else:
            logging.warning("Cannot load toast image")
        sysToast.text_fields = [lang.mainMenu["songLoaded"], work.audioArtistText + " - " + work.audioTitleText]
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
                page.overlay.append(work.playAudio)
                logging.info("Append playAudio")
                firstPlay = False
            work.playAudio.src = audioFile
            logging.info("Set playAudio.src as audioFile")
            audioPathTemp = None
            audioInfoUpdate()
            page.title = audioArtistText + " - " + audioTitleText + "- Simplay Player"
            logging.info("Window title changed")
            if work.currentOS == 'windows':
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

    def audioInfoUpdate():
        work.audioInfoUpdate(audioFile)
        if work.audioCoverBase64 != None:
            audioCover.src_base64 = work.audioCoverBase64.decode('utf-8')
        audioCover.src = work.audioCover_src
        audioTitle.value = work.audioTitleText
        audioArtist.value = work.audioArtistText
        audioAlbum.value = work.audioAlbumText
        audioCover.update()
        page.update()
  
    def playOrPauseMusic(e):
        if audioFile != None:
            work.playOrPauseMusic(audioFile)
            playPause_btn.icon = work.playPause_btn_icon
            page.title = work.page_title
        page.update()
    
    def autoStopKeepAudioProgress(e):
        work.autoStopKeepAudioProgress
        page.update()

    def autoKeepAudioProgress(e):
        work.autoKeepAudioProgress(e)
        audioProgressBar.value = work.audioProgressBar_value
        audioProgressStatus.value = work.audioProgressStatus_value
        page.update()

    def progressCtrl(e):
        work.progressCtrl(audioProgressBar.value)       
        page.update()

    """
    def lyricExistAndRead():
        if os.path.exists(lyricFile):
            with open(lyricFile,'r',encoding = 'utf-8') as f:
                content = f.read()
        else:
            pass
    """

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
        logging.info("Page updated")
    """
    
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
        work.volumeChange(volume_silder.value)
        volume_btn.icon = work.volume_btn
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
            content = ft.Text(value = work.audioInfo, size = 10)
        )
        page.dialog = audioInfo_dlg
        audioInfo_dlg.open = True
        logging.info("Dialog audioInfo_dlg opened")
        page.update()
        logging.info("Page updated")

    def openAboutDlg(e):
        about_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["about"]),
            content = ft.Text("Simplay Player by What_Damon\n\nVersion: 1.1.0_experimentalTest\nPowered by: Flet, Tinytag\n\nRuning under Python " + platform.python_version() + "\nOS: " + platform.platform())
        )
        page.dialog = about_dlg
        about_dlg.open = True
        logging.info("Dialog about_dlg opened")
        page.update()
        logging.info("Page updated")
    
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
                                    on_click = work.balanceMiddle
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shiftLeft"]),
                                    leading = ft.Icon(ft.icons.ARROW_BACK_OUTLINED),
                                    on_click = work.balanceLeft
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shiftRight"]),
                                    leading = ft.Icon(ft.icons.ARROW_FORWARD_OUTLINED),
                                    on_click = work.balanceRight
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
                                    on_click = work.audioForward10sec
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["back10s"]),
                                    leading = ft.Icon(ft.icons.ARROW_BACK_OUTLINED),
                                    on_click = work.audioBack10sec
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
                                    on_click = work.rateChangeTo05
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["1x"]),
                                    leading = ft.Icon(ft.icons.STOP_OUTLINED),
                                    on_click = work.rateChangeTo10
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["1.5x"]),
                                    leading = ft.Icon(ft.icons.ARROW_FORWARD_OUTLINED),
                                    on_click = work.rateChangeTo15
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["2x"]),
                                    leading = ft.Icon(ft.icons.ROCKET_LAUNCH_OUTLINED),
                                    on_click = work.rateChangeTo20
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
    audioAlbum = ft.Text(audioAlbumText, size = 18, opacity = 90)
    audioProgressStatus = ft.Text("00:00/00:00", size = 15, opacity = 90)
    audioDetail = ft.Column(controls = [audioTitle, audioArtist, audioAlbum, audioProgressStatus])
    audioBasicInfo = ft.Row(controls = [audioCover, audioDetail])
    audioProgressBar = ft.Slider(min = 0, max = 1000, tooltip = lang.tooltips["audioPosition"], on_change_start = autoStopKeepAudioProgress, on_change_end = progressCtrl)
    work.playAudio.on_loaded = lambda _: logging.info("Audio loaded: " + audioFile + " => " + audioArtistText + " - " + audioTitleText)
    work.playAudio.on_position_changed = autoKeepAudioProgress
    
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
        icon = ft.icons.LOOP_OUTLINED,
        tooltip = lang.tooltips["playInLoop"],
        icon_size = 20,
        visible = True
        # on_click = enableOrDisableLoop
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
        top = 20,
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
    work.detectOS()
    lang.loadLang()
    if work.currentOS == 'wsl':
        print(lang.infomation["wslWarning"])
        logging.warning("Using WSL")
    if work.currentOS == 'cygwin':
        print(lang.infomation["cygwinWarning"])
        logging.warning("Using Cygwin")
    if work.currentOS == "windows":
        logging.info("Lib Windows-Toasts imported")
    else:
        print(lang.infomation["nonTestWarning"])
        logging.warning("Non-test OS")
    
    audioTitleText = lang.mainMenu["unknownMusic"]
    audioArtistText = lang.mainMenu["unknownArtist"]
    audioAlbumText = lang.mainMenu["unknownAlbum"]
    audioInfo = lang.mainMenu["none"]
    logging.info("Basic initialization complete")
    ft.app(target = main)