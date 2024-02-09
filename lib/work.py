import flet as ft
import tinytag, time, base64, os, platform, logging
logging.info("Basic libs imported")
from i18n import lang
logging.info("Languages imported")

audioFile = None
lyricFile = None
firstPlay = True
playStatus = False
loopOpen = False
progressChanging = False
audioTag = None
audioCoverBase64 = None
audioInfo = None
audioTitleText = None
audioArtistText = None
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

def secondConvert(sec):
    return(time.strftime("%M:%S", time.gmtime(sec)))

def audioInfoUpdate(audioFile):
    global audioTag, audioTitleText, audioArtistText, audioAlbumText, audioInfo, audioCoverBase64, audioCover_src
    audioTag = tinytag.TinyTag.get(audioFile, image = True)
    if audioTag.get_image() != None:
        audioCoverBase64 = base64.b64encode(audioTag.get_image())
        audioCover_src = audioTag.get_image()
        logging.info("Audio cover transcoded to base64")
        logging.info("Audio cover loaded")
    else:
        audioCoverBase64 = None
        audioCover_src = './asset/track.png'
        logging.info("Placeholder cover loaded")
    logging.info("audioCover updated")
    if audioTag.title != None:
        audioTitleText = audioTag.title
        logging.info("Set audio title")
    else:
        audioTitleText = audioFile
        logging.info("Unknown audio title")
    if audioTag.artist != None:
        audioArtistText = audioTag.artist
        logging.info("Set audio artist")
    else:
        audioArtistText = lang.mainMenu["unknownArtist"]
        logging.info("Unknown audio artist")
    if audioTag.album != None:
        audioAlbumText = audioTag.album
        logging.info("Set audio album")
    else:
        audioAlbumText = lang.mainMenu["unknownAlbum"]
        logging.info("Unknown audio album")
    audioInfo = "Album: " + str(audioTag.album) + "\nAlbumist: " + str(audioTag.albumartist) + "\nArtist: " + str(audioTag.artist) + "\nAudio Offset: " + str(audioTag.audio_offset) + "\nBitrate: " + str(audioTag.bitrate) + "\nBitdepth: " + str(audioTag.bitdepth) + "\nChannels: " + str(audioTag.channels) + "\nComment: " + str(audioTag.comment)+ "\nComposer: " + str(audioTag.composer) + "\nDisc: " + str(audioTag.disc) + "\nDisc Total: " + str(audioTag.disc_total) + "\nDuration: " + str(audioTag.duration) + "\nFilesize: " + str(audioTag.filesize) + "\nGenre: " + str(audioTag.genre) + "\nSamplerate: " + str(audioTag.samplerate) + "\nTitle: " + str(audioTag.title) + "\nTrack: " + str(audioTag.track) + "\nTrack Total: " + str(audioTag.track_total) + "\nYear: " + str(audioTag.year)
    logging.info("Set audio info")
    logging.info("Page updated")

"""
def lyricExistAndRead():
    if os.path.exists(lyricFile):
        with open(lyricFile,'r',encoding = 'utf-8') as f:
            content = f.read()
    else:
        pass
"""

def playOrPauseMusic(audioFile):
    global playStatus, playPause_btn_icon, page_title
    if audioFile != None:
        audioInfoUpdate(audioFile)
        if playStatus == False:
            playStatus = True
            playAudio.resume()
            logging.info("Audio Play/Resume")
            playPause_btn_icon = ft.icons.PAUSE_CIRCLE_FILLED_OUTLINED
            page_title = "♫ " + audioArtistText + " - " + audioTitleText + "- Simplay Player"
            logging.info("Window title changed")
        elif playStatus == True:
            playStatus = False
            playAudio.pause()
            logging.info("Audio Pause")
            playPause_btn_icon = ft.icons.PLAY_CIRCLE_FILL_OUTLINED
            page_title = "▶️ " + audioArtistText + " - " + audioTitleText + "- Simplay Player"
            logging.info("Window title changed")
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
    global loopOpen, audioProgressBar_value, audioProgressStatus_value
    if progressChanging == False:
        audioProgressBar_value = playAudio.get_current_position() / playAudio.get_duration() * 1000
    if playAudio.get_current_position() == playAudio.get_duration() and loopOpen == True:
        playAudio.seek(0)
    currentLength = secondConvert(playAudio.get_current_position() // 1000)
    totalLength = secondConvert(playAudio.get_duration() // 1000)
    audioProgressStatus_value = currentLength + "/" + totalLength
    return audioProgressBar_value, audioProgressStatus_value

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

def autoStopKeepAudioProgress(e):
    global progressChanging
    progressChanging = True
    logging.info("Set progressChanging as True")

def progressCtrl(audioProgressBar):
    global progressChanging
    progressChanging = False
    logging.info("Set progressChanging as False")
    playAudio.seek(int(playAudio.get_duration() * (audioProgressBar / 1000)))
    logging.info("Audio seek completed")

def volumeChange(volume_silder):
    global volume_btn
    playAudio.volume = volume_silder / 100
    if audioFile != None:
        playAudio.update()
        logging.info("playAudio updated")
    if volume_silder >= 50:
        volume_btn = ft.icons.VOLUME_UP_OUTLINED
    elif volume_silder == 0:
        volume_btn = ft.icons.VOLUME_MUTE_OUTLINED
    elif volume_silder < 50:
        volume_btn = ft.icons.VOLUME_DOWN_OUTLINED
    logging.info("Page updated")

def balanceLeft(e):
    playAudio.balance -= 0.1
    logging.info("Channel left shift to " + str(playAudio.balance))
    playAudio.update()
    logging.info("playAudio updated")

def balanceRight(e):
    playAudio.balance += 0.1
    logging.info("Channel right shift to " + str(playAudio.balance))
    playAudio.update()
    logging.info("playAudio updated")

def balanceMiddle(e):
    playAudio.balance = 0
    logging.info("Channel set banlace to 0")
    playAudio.update()
    logging.info("playAudio updated")

playAudio = ft.Audio(
    autoplay = False,
    volume = 1,
    balance = 0,
    on_duration_changed = lambda e: logging.info("Duration changed:" + e.data),
    on_state_changed = lambda e: logging.info("State changed:" + e.data),
    on_seek_complete = lambda _: logging.info("Seek complete"),
    )