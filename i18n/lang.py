import locale
from lib import log_init

log_init.logging.info("Basic libs imported at lang.py")

from i18n import en_US, zh_CN

log_init.logging.info("Imported language files")

langCode = locale.getdefaultlocale()[0]

log_init.logging.info("Get default locale: " + langCode)

langInfo = {}
infomation = {}
menuBar = {}
mainMenu = {}
tooltips = {}
songList = {}
dialog = {}
update = {}
sets = {}

def loadLang(): 
    global langCode, langInfo, infomation, menuBar, mainMenu, tooltips, songList, dialog, update, sets
    if langCode == 'zh_CN':
        langInfo = zh_CN.langInfo
        infomation = zh_CN.infomation
        menuBar = zh_CN.menuBar
        mainMenu = zh_CN.mainMenu
        tooltips = zh_CN.tooltips
        songList = zh_CN.songList
        dialog = zh_CN.dialog
        update = zh_CN.update
        sets = zh_CN.sets
    else:
        langInfo = en_US.langInfo
        infomation = en_US.infomation
        menuBar = en_US.menuBar
        mainMenu = en_US.mainMenu
        tooltips = en_US.tooltips
        songList = en_US.songList
        dialog = en_US.dialog
        update = en_US.update
        sets = en_US.sets
