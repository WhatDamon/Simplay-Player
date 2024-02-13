import flet as ft
import platform, logging, os
from lib import work # 工作模块
logging.basicConfig(filename = 'player.log', format = ' %(asctime)s | %(levelname)s | %(funcName)s | %(message)s', level = logging.info)
from i18n import lang
logging.info("Languages imported")
logging.info("Variable initialization complete")

ver = "2.0.0_experimentaltest"
audioFile = None
lyricFile = ""
audioListShown = False
firstPlay = True
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

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

    page.scroll = ft.ScrollMode.AUTO

    #快捷键
    def keyboardEventTrack(e: ft.KeyboardEvent):
        logging.info("Keyboard event")
        if f"{e.key}" == " ":
            playOrPauseMusic(0)  
            logging.info("Press space bar to play/pause audio")
        if f"{e.ctrl}" == "True" and f"{e.key}" == "H":
            hideShowMenuBar(0)           
            logging.info("Press Ctrl-H to hide/show menu bar")

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
        global audioPathTemp
        audioPathTemp = (
            ", ".join(map(lambda f: f.path, e.files)) if e.files else None
        )
        if audioPathTemp == None:
            logging.warning("Nothing Loaded")
            pass
        else:
            songlist_tiles.controls.append(audioTile(audioPathTemp))
            readSong(audioPathTemp)

    def readSong(audioPathTemp):
        global audioFile, lyricFile, firstPlay, getReturn
        page.splash = ft.ProgressBar()
        logging.info("Splash progress bar enabled")
        page.update()
        logging.info("Page updated")
        getReturn = False  
        audioFile = audioPathTemp
        lyricFile = ''.join(audioPathTemp.split('.')[:-1]) + ".lrc"
        lyrics_before.value = ""
        lyrics_text.value = ""
        lyrics_after.value = ""
        logging.info("File path loaded")
        logging.info("Audio path: " + audioFile)
        logging.info("Lyric path: " + lyricFile)
        if firstPlay == True:
            page.overlay.append(work.playAudio)
            logging.info("Append playAudio")
            firstPlay = False
        audioPathTemp = None
        audioInfoUpdate()
        page.title = work.audioArtistText + " - " + audioTitleText + " - Simplay Player"
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
    
    def pickFolderResult(e: ft.FilePickerResultEvent):
        allowed_extensions = ['mp3']
        songList = []
        songlistPathTemp = e.path if e.path else None
        if songlistPathTemp != None:
            for root, dirs, files in os.walk(songlistPathTemp):
                for f in files:
                    if f.split('.')[-1] in allowed_extensions:
                        file_path = os.path.join(root, f)
                        songList.append(file_path)
            readSong(songList[0])
            songListTiles(songList)
        
    pickFilesDialog = ft.FilePicker(on_result = pickFileResult)
    logging.info("Append pickFilesDialog")  
    pickSonglistDialog = ft.FilePicker(on_result = pickFolderResult) 
    page.overlay.extend([pickFilesDialog, pickSonglistDialog])

    #本地音频信息更新
    def audioInfoUpdate():
        work.audioInfoUpdate(audioFile)
        audioCover.src_base64 = work.audioCoverBase64
        audioCover.src = work.audioCover_src
        audioTitle.value = work.audioTitleText
        audioArtist.value = work.audioArtistText
        audioAlbum.value = work.audioAlbumText
        audioCover.update()
        page.update()

    #网络音频信息更新
    def audioFromUrlInfo(e):
        global audioFile, lyricFile, getReturn, firstPlay
        songID_text = songID_input.value
        songID = songID_text
        getReturn = work.audioFromUrlInfo(songID)
        if getReturn == True:        
            if firstPlay == True:
                page.overlay.append(work.playAudio)
                logging.info("Append playAudio")
                firstPlay = False
            audioFile = work.audioUrl
            lyricFile = ""
            audioCover.src_base64 = ""
            audioCover.src = work.audioCover_src
            audioTitle.value = work.audioTitleText
            audioArtist.value = work.audioArtistText
            audioAlbum.value = work.audioAlbumText
            songID_input.error_text = ""
            audioCover.update()
            lyricUrlRead(songID)
            closeSongWeb_dlg(e)
        elif getReturn == "notSuptSong":
            songID_input.error_text = lang.dialog["vipAlert"]
        elif getReturn == False:
            songID_input.error_text = lang.dialog["errorPrompt"]
        page.update()

    #播放列表类
    class audioTile(ft.UserControl):
        def __init__(self, song):
            super().__init__()
            self.song = song
            self.song_name = song.split('\\')[-1]

        def playSong(self,e):
            readSong(self.song)
            playOrPauseMusic(e)
            self.update()

        def build(self):
            return ft.Row(controls=[
                ft.Icon(name=ft.icons.MUSIC_NOTE_OUTLINED),
                ft.Text(self.song_name,width=200),
                ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
                              on_click=self.playSong)],width=300)
        
    def songListTiles(songList):
        for song in songList:
            songlist_tiles.controls.append(audioTile(song))

    #本地歌词读取    
    def lyricExistAndRead():
        if os.path.exists(lyricFile):
            work.lyricRead(lyricFile)
            lyrics_before.value = work.lyricsBefore
            lyrics_text.value = work.lyricsText
            lyrics_after.value = work.lyricsAfter
        else:
            pass
    
    #网络歌词读取
    def lyricUrlRead(songID):
        readRes = work.lyricUrlRead(songID)
        if readRes == True:
            lyrics_before.value = work.lyricsBefore
            lyrics_text.value = work.lyricsText
            lyrics_after.value = work.lyricsAfter
        if readRes == False:
            lyrics_before.value = ""
            lyrics_text.value = ""
            lyrics_after.value = ""
            
    
    #网络歌词处理（主要部分在work.py）
    def lyricsProcess():
        work.lyricsProcess()
        lyrics_before.value = work.lyricsBefore
        lyrics_text.value = work.lyricsText
        lyrics_after.value = work.lyricsAfter

    #歌词显示/隐藏
    def lyricShow(e):
        if lyrics_text.visible == True:
            lyrics_before.visible = False
            lyrics_text.visible = False
            lyrics_after.visible = False
            lyrics_btn.icon = ft.icons.LYRICS_OUTLINED
        elif lyrics_text.visible == False:
            lyrics_before.visible = True
            lyrics_text.visible = True
            lyrics_after.visible = True
            lyrics_btn.icon = ft.icons.LYRICS
        page.update()
  
    #歌曲播放/暂停
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
        if lyricFile != "":
            lyricExistAndRead()
        elif getReturn == True:
            lyricsProcess()
        page.update()

    def progressCtrl(e):
        work.progressCtrl(audioProgressBar.value)     
        page.update()

    #单曲循环设置
    def enableOrDisableRepeat(e):
        work.enableOrDisableRepeat(e)
        if work.loopOpen == False:
            playInRepeat_btn.icon = ft.icons.REPEAT_ONE_OUTLINED
        elif work.loopOpen == True:
            playInRepeat_btn.icon = ft.icons.REPEAT_ONE_ON_OUTLINED
        page.update()
        logging.info("Page updated")
    
    #打开音量面板
    def openVolumePanel(e):
        if volume_panel.visible == True:
            volume_panel.visible = False
            logging.info("Volume panel not visiable")
        elif volume_panel.visible == False:
            volume_panel.visible = True
            logging.info("Volume panel visiable")
        page.update()
        logging.info("Page updated")

    #改变音量
    def volumeChange(e):
        work.volumeChange(volume_silder.value)
        volume_btn.icon = work.volume_btn
        page.update()

    #播放列表
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
   
    #关闭窗口
    def closeSongWeb_dlg(e):
        songWeb_dlg.open = False
        page.update()

    songID_hint = ft.Text(value=lang.dialog["songIdHint"]) 
    songID_input = ft.TextField(label="",error_text = "")
    songWeb_dlg = ft.AlertDialog(
            adaptive = True,
            title = ft.Text(value=lang.dialog["songIdInput"]),
            content = ft.Column(controls=[
                songID_hint,
                songID_input,],
                height = 100,
                width = 400,),
                actions=[
                ft.TextButton("取消",on_click=closeSongWeb_dlg),
                ft.TextButton("确定",on_click=audioFromUrlInfo),
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )

    def getSongFromWebsite(e):
        page.dialog = songWeb_dlg
        songWeb_dlg.open = True
        logging.info("Dialog songWeb_dlg opened")
        page.update()
        logging.info("Page updated")

    #媒体信息
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
    
    #关于信息
    def openAboutDlg(e):
        about_dlg = ft.AlertDialog(
            title = ft.Text(value = lang.mainMenu["about"]),
            content = ft.Text("Simplay Player by What_Damon\n\nVersion: "+ver+"\nPowered by: Flet, Tinytag\n\nRuning under Python " + platform.python_version() + "\nOS: " + platform.platform())
        )
        page.dialog = about_dlg
        about_dlg.open = True
        logging.info("Dialog about_dlg opened")
        page.update()
        logging.info("Page updated")

    #窗口置顶按钮
    windowOnTop_btn = ft.IconButton(
                    icon = ft.icons.PUSH_PIN_OUTLINED,
                    tooltip = lang.tooltips["alwaysOnTop"],
                    on_click = alwaysOnTop
                )

    #菜单栏
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
                            content = ft.Text(value = lang.menuBar["openSonglist"]),
                            leading = ft.Icon(ft.icons.PLAYLIST_ADD_OUTLINED),
                            on_click = lambda _: pickSonglistDialog.get_directory_path(),
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["getFromMusicWebsite"]),
                            leading = ft.Icon(ft.icons.TRAVEL_EXPLORE_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text("获取歌曲"),
                                    leading = ft.Icon(ft.icons.MUSIC_NOTE_OUTLINED),
                                    on_click = getSongFromWebsite
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text("获取专辑/歌单"),
                                    leading = ft.Icon(ft.icons.ALBUM_OUTLINED)
                                )
                            ]
                        ),
                        ft.MenuItemButton(
                            content = ft.Text(value = lang.menuBar["exit"]),
                            leading = ft.Icon(ft.icons.EXIT_TO_APP_OUTLINED),
                            on_click = closeWindow
                        )
                    ]
                ),
                ft.SubmenuButton(
                    content = ft.Text(value = lang.menuBar["play"]),
                    controls = [
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["channels"]),
                            leading = ft.Icon(ft.icons.TUNE_OUTLINED),
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
                            content = ft.Text(value = lang.menuBar["speed"]),
                            leading = ft.Icon(ft.icons.SPEED_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["0.5x"]),
                                    leading = ft.Icon(ft.icons.ARROW_BACK_OUTLINED),
                                    on_click = work.rateChangeTo05
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["1x"]),
                                    leading = ft.Icon(ft.icons.ONE_X_MOBILEDATA_OUTLINED),
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
                            content = ft.Text(value = lang.menuBar["lyrics"]),
                            leading = ft.Icon(ft.icons.LYRICS_OUTLINED),
                        ),
                        ft.SubmenuButton(
                            content = ft.Text(value = lang.menuBar["mode"]),
                            leading = ft.Icon(ft.icons.PLAYLIST_PLAY_OUTLINED),
                            controls = [
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["playInOrder"]),
                                    leading = ft.Icon(ft.icons.PLAYLIST_PLAY_OUTLINED),
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["loop"]),
                                    leading = ft.Icon(ft.icons.REPEAT_OUTLINED),
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["repeat"]),
                                    leading = ft.Icon(ft.icons.REPEAT_ONE_OUTLINED),
                                ),
                                ft.MenuItemButton(
                                    content = ft.Text(value = lang.menuBar["shuffle"]),
                                    leading = ft.Icon(ft.icons.SHUFFLE_OUTLINED),
                                )
                            ]
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

    audioCover = ft.Image(src = "./asset/track.png", width = 128, height = 128, border_radius = 5)
    audioTitle = ft.Text(audioTitleText, weight = ft.FontWeight.BOLD, size = 25, overflow = ft.TextOverflow.ELLIPSIS)
    audioArtist = ft.Text(audioArtistText, size = 18, opacity = 90)
    audioAlbum = ft.Text(audioAlbumText, size = 18, opacity = 90)
    audioProgressStatus = ft.Text("00:00/00:00", size = 15, opacity = 90)
    audioDetail = ft.Column(controls = [audioTitle, audioArtist, audioAlbum, audioProgressStatus])
    audioBasicInfo = ft.Row(controls = [audioCover, audioDetail])
    audioProgressBar = ft.Slider(min = 0, max = 1000, tooltip = lang.tooltips["audioPosition"], on_change_start = autoStopKeepAudioProgress, on_change_end = progressCtrl)
    work.playAudio.on_loaded = lambda _: logging.info("Audio loaded: " + audioFile + " => " + audioArtistText + " - " + audioTitleText)
    work.playAudio.on_position_changed = autoKeepAudioProgress
    
    skipPrevious_btn = ft.IconButton(
        icon = ft.icons.SKIP_PREVIOUS_OUTLINED,
        tooltip = lang.tooltips["skipPrevious"],
        icon_size = 25,
        #on_click = playOrPauseMusic
    )

    playPause_btn = ft.IconButton(
        icon = ft.icons.PLAY_CIRCLE_FILLED_OUTLINED,
        tooltip = lang.tooltips["playOrPause"],
        icon_size = 35,
        on_click = playOrPauseMusic
    )

    skipNext_btn = ft.IconButton(
        icon = ft.icons.SKIP_NEXT_OUTLINED,
        tooltip = lang.tooltips["skipNext"],
        icon_size = 25,
        #on_click = playOrPauseMusic
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
    
    lyrics_btn = ft.IconButton(
        icon = ft.icons.LYRICS,
        tooltip = lang.tooltips["lyrics"],
        icon_size = 20,
        visible = True,
        on_click = lyricShow
    )

    playInRepeat_btn = ft.IconButton(
        icon = ft.icons.REPEAT_ONE_OUTLINED,
        tooltip = lang.tooltips["playRepeat"],
        icon_size = 20,
        visible = True,
        on_click = enableOrDisableRepeat
    )

    audioList_btn = ft.IconButton(
            icon = ft.icons.LIBRARY_MUSIC_OUTLINED,
            tooltip = lang.tooltips["songList"],
            icon_size = 20,
            on_click = audioListCtrl
        )
    songlist_tiles = ft.Column(controls=[],
                          height = 380,
                          spacing = 0,
                          scroll = ft.ScrollMode.AUTO,)
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
                songlist_tiles,
            ],
        ),
        left = 10,
        top = 70,
        width = 300,
        height = 450,
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
    
    lyrics_before = ft.Text(size = 20,visible=True,color=ft.colors.GREY)
    lyrics_text = ft.Text(size = 20,visible=True)
    lyrics_after = ft.Text(size = 20,visible=True,color=ft.colors.GREY)

    playbackCtrl_row = ft.Row(controls = [skipPrevious_btn, playPause_btn, skipNext_btn, volume_btn, volume_panel],spacing=1)
    moreBtns_row = ft.Row(controls = [lyrics_btn, playInRepeat_btn, audioList_btn, audioInfo_btn, settings_btn])
    btns_row = ft.Row(controls = [playbackCtrl_row, moreBtns_row], alignment = ft.MainAxisAlignment.SPACE_BETWEEN)

    page.overlay.append(audioList_menu)
    logging.info("Append audioList_menu")
    page.add(ft.Column(controls = [ft.Row(controls = [menuBar]), audioBasicInfo, audioProgressBar, btns_row, lyrics_before, lyrics_text, lyrics_after]))
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
