import flet as ft
from lib import log_init

log_init.logging.info("Basic libs imported at settingsPage.py")

from i18n import lang

log_init.logging.info("Languages imported at settingsPage.py")

appBar = ft.AppBar(title = ft.Text(value = lang.sets["settings"]))
constructionNotice = ft.Row(controls = [ft.Icon(ft.icons.CONSTRUCTION_OUTLINED, color = ft.colors.AMBER), ft.Text(value = lang.sets["construction"], color = ft.colors.AMBER)])

settings_pageView = ft.View("/settings", controls = [appBar, constructionNotice])