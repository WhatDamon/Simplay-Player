import flet as ft
from lib import log_init

log_init.logging.info("Basic libs imported at settingsPage.py")

import i18n

log_init.logging.info("Languages imported at settingsPage.py")

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
    langInfoText += "\n· " + i18n.lang.sets["langFont"] + i18n.lang.langInfo["font"]
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

colorMode_dropd = ft.Dropdown(
    label = i18n.lang.sets["pleaseSelect"],
    value = "sys",
    options = [
        ft.dropdown.Option(key = "sys", text = i18n.lang.sets["systemDefault"]),
        ft.dropdown.Option(key = "light", text = i18n.lang.sets["colorLight"]),
        ft.dropdown.Option(key = "dark", text = i18n.lang.sets["colorDark"])
    ]
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
    )
)

appearancesSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.BRUSH_OUTLINED), ft.Text(value = i18n.lang.sets["appearances"], size = 18)]),
                ft.Text(value = i18n.lang.sets["colorMode"]),
                colorMode_dropd,
                ft.Text(value = i18n.lang.sets["colorSchemes"]),
                colorSchemes_radio
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

playImmediatelyAfterLoaded_switch = ft.Switch(label = i18n.lang.sets["immediatelyPlay"])
defaultPlayInLoop_switch = ft.Switch(label = i18n.lang.sets["defaultLoop"])
defaultVolume_slider = ft.Slider(min = 0, max = 100, divisions = 100, label = "{value}", value = 100)

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
    elevation = 0.5,
    disabled = True
)

lyricsDefaultVisible_switch = ft.Switch(label = i18n.lang.sets["lyricsDefaultVis"], value = True)

lyricsSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.LYRICS_OUTLINED), ft.Text(value = i18n.lang.sets["lyrics"], size = 18)]),
                lyricsDefaultVisible_switch
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

onlineAPI_tf = ft.TextField(label = i18n.lang.sets["inputAPI"], value = "https://music.dsb.ink/api/")

onlineSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.MUSIC_NOTE_OUTLINED), ft.Text(value = i18n.lang.sets["webMusic"], size = 18)]),
                onlineAPI_tf,
                ft.Text(value = i18n.lang.sets["webAPIInfo"], selectable = True)
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

smtcEnable_switch = ft.Switch(label = i18n.lang.sets["enableSMTC"], value = False)

systemSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.DISPLAY_SETTINGS_OUTLINED), ft.Text(value = i18n.lang.sets["systemIntegration"], size = 18)]),
                smtcEnable_switch
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

settings_pageView = ft.View("/settings", controls = [appBar, constructionNotice, settingsNotice, languageSetCard, appearancesSetCard, playSetCard, lyricsSetCard, onlineSetCard, systemSetCard, feedbackSetCard], scroll = ft.ScrollMode.AUTO)