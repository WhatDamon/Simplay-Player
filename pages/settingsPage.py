import flet as ft
from lib import log_init, cfg, platform_check
log_init.logging.info("Basic libs imported at settingsPage.py")

import i18n
log_init.logging.info("Languages imported at settingsPage.py")

page = None

def transferPage(pg):
    global page
    page = pg

appBar = ft.AppBar(title = ft.Row(controls = [ft.Icon(ft.icons.SETTINGS_OUTLINED), ft.Text(value = i18n.lang.sets["settings"])]))

constructionNotice = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.CONSTRUCTION_OUTLINED, size = 40, color = ft.colors.AMBER)], alignment = ft.MainAxisAlignment.CENTER),
                ft.Row(controls = [ft.Text(value = i18n.lang.sets["construction"], size = 15, color = ft.colors.AMBER, weight = ft.FontWeight.BOLD)], alignment = ft.MainAxisAlignment.CENTER)
            ]
        ),
        padding = 15
    ),
    elevation = 0.5
)

settingsNotice = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.NOTE_OUTLINED), ft.Text(value = i18n.lang.sets["note"])])
            ]
        ),
        padding = 15
    ),
    elevation = 0.5
)

langSelect_dropd = ft.Dropdown(
    label = i18n.lang.sets["pleaseSelect"],
    value = "sys",
    options = [
        ft.dropdown.Option(key = "sys", text = i18n.lang.sets["systemDefault"]),
        ft.dropdown.Option(key = "zh_CN", text = i18n.zh_CN.langInfo["orgiName"]),
        ft.dropdown.Option(key = "en_US", text = i18n.en_US.langInfo["engName"])
    ]
)

langInfoText = "· " + i18n.lang.sets["langNameEng"] + i18n.lang.langInfo["engName"]
if i18n.lang.langInfo["orgiName"] != "":
    langInfoText += "\n· " + i18n.lang.sets["langNameOrigial"] + i18n.lang.langInfo["orgiName"]
langInfoText += "\n· " + i18n.lang.sets["langCode"] + i18n.lang.langInfo["code"]
if i18n.lang.langInfo["font"] == "":
    langInfoText += "\n· " + i18n.lang.sets["langFont"] + "Default"
else:
    if platform_check.currentOS == "windows":
        langInfoText += "\n· " + i18n.lang.sets["langFont"] + i18n.lang.langInfo["font"][0]["windows"]
    elif platform_check.currentOS == "darwin":
        langInfoText += "\n· " + i18n.lang.sets["langFont"] + i18n.lang.langInfo["font"][0]["macos"]
    else:
        langInfoText += "\n· " + i18n.lang.sets["langFont"] + i18n.lang.langInfo["font"][0]["linux"]
langInfoText += "\n· " + i18n.lang.sets["langRTL"] + str(i18n.lang.langInfo["rtl"])
if i18n.lang.langInfo["machineTranslated"] == True:
    langInfoText += "\n· " + i18n.lang.infomation["machineTranslate"]
if i18n.lang.langInfo["useKKGithub"] == True:
    langInfoText += "\n· " + i18n.lang.infomation["updateUseKKGithubMirror"]

languageSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.LANGUAGE_OUTLINED), ft.Text(value = i18n.lang.sets["language"], size = 18)]),
                langSelect_dropd,
                ft.Text(langInfoText)
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

def colorModeWrite(e):
    global page
    if colorMode_dropd.value == "sys":
        cfg.cfgData["appearances"][0]["mode"] = "sys"
        log_init.logging.info("Set mode at appearances as 'sys'")
        page.theme_mode = ft.ThemeMode.SYSTEM
    elif colorMode_dropd.value == "light":
        cfg.cfgData["appearances"][0]["mode"] = "light"
        log_init.logging.info("Set mode at appearances as 'sys'")
        page.theme_mode = ft.ThemeMode.LIGHT
    elif colorMode_dropd.value == "sys":
        cfg.cfgData["appearances"][0]["mode"] = "dark"
        log_init.logging.info("Set mode at appearances as 'dark'")
        page.theme_mode = ft.ThemeMode.DARK
    page.update()
    cfg.saveConfig()

colorMode_dropd = ft.Dropdown(
    label = i18n.lang.sets["pleaseSelect"],
    value = "sys",
    options = [
        ft.dropdown.Option(key = "sys", text = i18n.lang.sets["systemDefault"]),
        ft.dropdown.Option(key = "light", text = i18n.lang.sets["colorLight"]),
        ft.dropdown.Option(key = "dark", text = i18n.lang.sets["colorDark"])
    ],
    on_change = colorModeWrite,
    disabled = True
)

colorSchemes_radio = ft.RadioGroup(
    value = "blue",
    content = ft.Row(controls = [
            ft.Radio(value = "blue", label = i18n.lang.sets["blue"], fill_color = ft.colors.BLUE_800),
            ft.Radio(value = "pink", label = i18n.lang.sets["pink"], fill_color = ft.colors.PINK_700),
            ft.Radio(value = "green", label = i18n.lang.sets["green"], fill_color = ft.colors.GREEN_700),
            ft.Radio(value = "brown", label = i18n.lang.sets["brown"], fill_color = ft.colors.BROWN),
            ft.Radio(value = "purple", label = i18n.lang.sets["purple"], fill_color = ft.colors.DEEP_PURPLE),
        ]
    ),
    disabled = True
)

appearancesSystemSets_switch = ft.Switch(label = i18n.lang.sets["appearancesSys"], value = False, disabled = True)

def enableRTLWrite(e):
    if rtlEnable_switch.value == True:
        cfg.cfgData["appearances"][0]["rtl"] = True
        log_init.logging.info("Set rtl at appearances as True")
    else:
        cfg.cfgData["appearances"][0]["rtl"] = False
        log_init.logging.info("Set rtl at appearances as False")
    cfg.saveConfig()

rtlEnable_switch = ft.Switch(label = i18n.lang.sets["rtl"], value = cfg.cfgData["appearances"][0]["rtl"], on_change = enableRTLWrite)

appearancesSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.BRUSH_OUTLINED), ft.Text(value = i18n.lang.sets["appearances"], size = 18)]),
                ft.Text(value = i18n.lang.sets["colorMode"]),
                colorMode_dropd,
                ft.Text(value = i18n.lang.sets["colorSchemes"]),
                colorSchemes_radio,
                ft.Divider(),
                appearancesSystemSets_switch,
                rtlEnable_switch
            ]
        ),
        padding = 15
    ),
    elevation = 0.5
)

def playImmediatelyAfterLoadedWrite(e):
    if playImmediatelyAfterLoaded_switch.value == True:
        cfg.cfgData["play"][0]["immediatelyPlay"] = True
        log_init.logging.info("Set immediatelyPlay at play as True")
    else:
        cfg.cfgData["play"][0]["immediatelyPlay"] = False
        log_init.logging.info("Set immediatelyPlay at play as False")
    cfg.saveConfig()

playImmediatelyAfterLoaded_switch = ft.Switch(label = i18n.lang.sets["immediatelyPlay"], value = cfg.cfgData["play"][0]["immediatelyPlay"], on_change = playImmediatelyAfterLoadedWrite)

def defaultPlayInLoopWrite(e):
    if defaultPlayInLoop_switch.value == True:
        cfg.cfgData["play"][0]["defaultPlayInLoop"] = True
        log_init.logging.info("Set defaultPlayInLoop at play as True")
    else:
        cfg.cfgData["play"][0]["defaultPlayInLoop"] = False
        log_init.logging.info("Set defaultPlayInLoop at play as False")
    cfg.saveConfig()

defaultPlayInLoop_switch = ft.Switch(label = i18n.lang.sets["defaultLoop"], value = cfg.cfgData["play"][0]["defaultPlayInLoop"], on_change = defaultPlayInLoopWrite)

def defaultVolumeWrite(e):
    cfg.cfgData["play"][0]["defaultVolume"] = defaultVolume_slider.value
    log_init.logging.info("Set defaultVolume at play as " + defaultVolume_slider.value)
    cfg.saveConfig()

defaultVolume_slider = ft.Slider(min = 0, max = 100, divisions = 100, label = "{value}", value = cfg.cfgData["play"][0]["defaultVolume"], on_change_end = defaultVolumeWrite)

playSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.PLAY_ARROW_OUTLINED), ft.Text(value = i18n.lang.sets["play"], size = 18)]),
                playImmediatelyAfterLoaded_switch,
                defaultPlayInLoop_switch,
                ft.Text(value = i18n.lang.sets["defaultVolume"]),
                defaultVolume_slider
            ]
        ),
        padding = 15
    ),
    elevation = 0.5
)

def lyricsDefaultVisibleWrite(e):
    if lyricsDefaultVisible_switch.value == True:
        cfg.cfgData["lyrics"][0]["lyricsDefaultVisible"] = True
        log_init.logging.info("Set lyricsDefaultVisible at lyrics as True")
    else:
        cfg.cfgData["lyrics"][0]["lyricsDefaultVisible"] = False
        log_init.logging.info("Set lyricsDefaultVisible at lyrics as False")
    cfg.saveConfig()

lyricsDefaultVisible_switch = ft.Switch(label = i18n.lang.sets["lyricsDefaultVis"], on_change = lyricsDefaultVisibleWrite, value = cfg.cfgData["lyrics"][0]["lyricsDefaultVisible"])

if cfg.cfgData["lyrics"][0]["lyricsDefaultVisible"] == True:
    lyricsDefaultVisible_switch.value = True

lyricsSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.LYRICS_OUTLINED), ft.Text(value = i18n.lang.sets["lyrics"], size = 18)]),
                lyricsDefaultVisible_switch
            ]
        ),
        padding = 15
    ),
    elevation = 0.5
)

def onlineAPIWrite(e):
    cfg.cfgData["online"][0]["onlineAPI"] = onlineMusicAPI_tf.value
    log_init.logging.info("Set onlineAPI at online as " + onlineMusicAPI_tf.value)
    cfg.saveConfig()

onlineMusicAPI_tf = ft.TextField(label = i18n.lang.sets["inputAPI"], value = cfg.cfgData["online"][0]["onlineAPI"], on_change = onlineAPIWrite)

def setMusicAPIToDefault(e):
    onlineMusicAPI_tf.value = "https://music.dsb.ink/api/"

onlineSystemSets_switch = ft.Switch(label = i18n.lang.sets["onlineSys"], value = True, disabled = True)
onlineUpdateAPI_tf = ft.TextField(label = i18n.lang.sets["inputAPI"], visible = False)

onlineSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.MUSIC_NOTE_OUTLINED), ft.Text(value = i18n.lang.sets["online"], size = 18)]),
                ft.Text(value = i18n.lang.sets["onlineMusic"]),
                ft.ResponsiveRow(controls = [onlineMusicAPI_tf, ft.FilledTonalButton(text = i18n.lang.sets["setToDefault"], icon = ft.icons.REFRESH_OUTLINED, on_click = setMusicAPIToDefault, disabled = True)]),
                ft.Text(value = i18n.lang.sets["webAPIInfo"], selectable = True),
                ft.Divider(),
                ft.Text(value = i18n.lang.sets["webUpdate"]),
                onlineSystemSets_switch,
                ft.ResponsiveRow(controls = [onlineUpdateAPI_tf, ft.FilledTonalButton(text = i18n.lang.sets["setToDefault"], icon = ft.icons.REFRESH_OUTLINED, on_click = setMusicAPIToDefault, disabled = True, visible = False)]),
                ft.Text(value = i18n.lang.sets["webAPIInfo"], selectable = True, visible = False) # need strings
            ]
        ),
        padding = 15
    ),
    elevation = 0.5
)

smtcEnable_switch = ft.Switch(label = i18n.lang.sets["enableSMTC"], value = False)
toastNotifyEnable_switch = ft.Switch(label = i18n.lang.sets["enableToastNotify"], value = True)

systemSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.DISPLAY_SETTINGS_OUTLINED), ft.Text(value = i18n.lang.sets["systemIntegration"], size = 18)]),
                smtcEnable_switch,
                toastNotifyEnable_switch
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

advanceSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.DANGEROUS_OUTLINED), ft.Text(value = i18n.lang.sets["advance"], size = 18)]),
                ft.Row(controls = [
                    ft.ElevatedButton(text = i18n.lang.sets["delConfigAndClose"], icon = ft.icons.DELETE_FOREVER_OUTLINED, bgcolor = ft.colors.RED, color = ft.colors.WHITE, elevation = 0, disabled = True),
                    ft.ElevatedButton(text = i18n.lang.sets["delLogFile"], icon = ft.icons.DELETE_OUTLINE, bgcolor = ft.colors.RED, color = ft.colors.WHITE, elevation = 0, disabled = True)
                ],
                wrap = True
                )
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

feedbackSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.FEEDBACK_OUTLINED), ft.Text(value = i18n.lang.sets["feedback"], size = 18)]),
                ft.Row(controls = [
                    ft.FilledTonalButton(text = i18n.lang.sets["bugReport"], icon = ft.icons.BUG_REPORT_OUTLINED, url = "https://github.com/WhatDamon/Simplay-Player/issues"),
                    ft.FilledTonalButton(text = i18n.lang.sets["shareIdeas"], icon = ft.icons.STAR_OUTLINE, url = r"https://github.com/WhatDamon/Simplay-Player/discussions/categories/%E6%83%B3%E6%B3%95"),
                    ft.FilledTonalButton(text = i18n.lang.sets["discussion"], icon = ft.icons.CHAT_OUTLINED, url = "https://github.com/WhatDamon/Simplay-Player/discussions"),
                ],
                wrap = True
                )
            ]
        ),
        padding = 15
    ),
    elevation = 0.5
)

settings_pageView = ft.View("/settings", controls = [appBar, constructionNotice, settingsNotice, languageSetCard, appearancesSetCard, playSetCard, lyricsSetCard, onlineSetCard, systemSetCard, advanceSetCard, feedbackSetCard], scroll = ft.ScrollMode.AUTO)