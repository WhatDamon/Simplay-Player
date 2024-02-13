import platform
from lib import log_init
log_init.logging.info("Basic libs imported at platform_check.py")

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
                    log_init.logging.info("Find 'microsoft' at /proc/version")
                    os = 'wsl'
        except:
            pass
    elif 'windows' in syst:
        os = 'windows'
    elif 'bsd' in syst:
        os = 'bsd'
    log_init.logging.info("You are using " + os)
    log_init.logging.info("Detail: " + platform.platform())
    global currentOS
    currentOS = os