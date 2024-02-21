import flet as ft
from lib import log_init

log_init.logging.info("Basic libs imported at settingsPage.py")

from i18n import lang

log_init.logging.info("Languages imported at settingsPage.py")

appBar = ft.AppBar(title = ft.Row(controls = [ft.Icon(ft.icons.SETTINGS_OUTLINED), ft.Text(value = lang.sets["settings"])]))

constructionNotice = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.CONSTRUCTION_OUTLINED, size = 40, color = ft.colors.AMBER)], alignment = ft.MainAxisAlignment.CENTER),
                ft.Row(controls = [ft.Text(value = lang.sets["construction"], size = 15, color = ft.colors.AMBER, weight = ft.FontWeight.BOLD)], alignment = ft.MainAxisAlignment.CENTER)
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

languageSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.LANGUAGE_OUTLINED), ft.Text(value = lang.sets["language"], size = 18)]),
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

appearancesSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.BRUSH_OUTLINED), ft.Text(value = lang.sets["appearances"], size = 18)]),
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

playSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.PLAY_ARROW_OUTLINED), ft.Text(value = lang.sets["play"], size = 18)]),
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

lyricsSetCard = ft.Card(
    content = ft.Container(
        content = ft.Column(controls = [
                ft.Row(controls = [ft.Icon(ft.icons.LYRICS_OUTLINED), ft.Text(value = lang.sets["lyrics"], size = 18)]),
            ]
        ),
        padding = 15
    ),
    elevation = 0.5,
    disabled = True
)

settings_pageView = ft.View("/settings", controls = [appBar, constructionNotice, languageSetCard, appearancesSetCard, playSetCard, lyricsSetCard])