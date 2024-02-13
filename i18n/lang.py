import locale
from i18n import en_US, zh_CN

langCode = locale.getdefaultlocale()[0]

langInfo = {}
infomation = {}
menuBar = {}
mainMenu = {}
tooltips = {}
songList = {}
dialog = {}

def loadLang(): 
    global langCode, langInfo, infomation, menuBar, mainMenu, tooltips, songList, dialog
    if langCode == 'zh_CN':
        langInfo = zh_CN.langInfo
        infomation = zh_CN.infomation
        menuBar = zh_CN.menuBar
        mainMenu = zh_CN.mainMenu
        tooltips = zh_CN.tooltips
        songList = zh_CN.songList
        dialog = zh_CN.dialog
    else:
        langInfo = en_US.langInfo
        infomation = en_US.infomation
        menuBar = en_US.menuBar
        mainMenu = en_US.mainMenu
        tooltips = en_US.tooltips
        songList = en_US.songList
        dialog = en_US.dialog
