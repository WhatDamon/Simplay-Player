import requests
from lib import log_init, platform_check
log_init.logging.info("Basic libs imported at update.py")

from i18n import lang

log_init.logging.info("Languages imported at update.py")

# 全局化变量
api = None
allInfo = None
latestVer = None

# API更新
def update_api():
    # API定义
    global api
    if lang.langInfo["code"] == "zh_CN": 
        api = requests.get("https://api.kkgithub.com/repos/WhatDamon/Simplay-Player/releases", timeout = 10, verify = False) # SSL禁用
        log_init.logging.info("Using KKGitHub mirror")
    else:
        api = requests.get("https://api.github.com/repos/WhatDamon/Simplay-Player/releases", timeout = 10, verify = False) # SSL禁用
        log_init.logging.info("Using official source")
    log_init.logging.info("API Update")
    global allInfo
    allInfo = api.json() # 获取Json
    log_init.logging.info("API infomation get")

# 版本检查
def version_check(ver):
    update_api()
    global latestVer
    latestVer = allInfo[0]['tag_name'] # 获取最新版本
    log_init.logging.info("Versions in the server: " + latestVer)
    log_init.logging.info("Comparing versions...")
    if "v" + ver == latestVer:
        return False
    else:
        return True

# 更新程序
def update(ver):
    # 主体
    update_api()
    log_init.logging.info("Testing...")
    try:
        response = api.text # 用于是否可以连接
        if version_check(ver) == False:
            log_init.logging.info("You are using the latest version")
            return "NUL"
        else:
            log_init.logging.info("Getting the change log...")
            detail = allInfo[0]['body'] # 获取更新日志
            log_init.logging.info("Checking if it is a pre-release version...")
            prerelease = allInfo[0]['prerelease'] # 获取是否为预览版本
            prereleaseContent = ""
            if prerelease == "false":
                prereleaseContent = lang.update["attention"] # 内容添加
                log_init.logging.info(latestVer + "is a pre-release version")
            scContent = ""
            if platform_check.currentOS == "darwin":
                scContent = lang.update["darwinCompatibility"] # 内容添加
            if platform_check.currentOS == "linux":
                scContent = lang.update["linuxCompatibility"] # 内容添加
            updContent = lang.update["contentCurrentVer"] + "v" + ver + lang.update["contentLatestVer"] + latestVer + lang.update["contentMore"] + detail  + prereleaseContent + scContent # 弹窗内容
            return updContent
    except requests.exceptions.RequestException as e:
        log_init.logging.error("Check for update failure")
        return "ERR"

# 获取下载链接  
def get_link():
    log_init.logging.info("Getting the download link...")
    if platform_check.currentOS == "windows":
        downloadUrl = "https://github.com/WhatDamon/Simplay-Player/releases"
    elif platform_check.currentOS == "darwin" or platform_check.currentOS == "linux":
        downloadUrl = "https://github.com/WhatDamon/Simplay-Player/actions"
    else:
        downloadUrl = allInfo[0]['tarball_url']
        log_init.logging.info("Set tarball as download url")
    log_init.logging.info("Link: " + downloadUrl)
    return downloadUrl