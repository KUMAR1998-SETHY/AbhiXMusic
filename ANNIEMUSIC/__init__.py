from ANNIEMUSIC.core.bot import JARVIS
from ANNIEMUSIC.core.dir import dirr
from ANNIEMUSIC.core.git import git
from ANNIEMUSIC.core.userbot import Userbot
from ANNIEMUSIC.misc import dbb, heroku
from .logging import LOGGER

# Safe startup initializations
try:
    dirr()
except Exception as e:
    LOGGER(__name__).warning(f"Directory setup skipped: {e}")

try:
    git()
except Exception as e:
    LOGGER(__name__).warning(f"Git setup skipped: {e}")

try:
    dbb()
except Exception as e:
    LOGGER(__name__).warning(f"Database init skipped: {e}")

try:
    heroku()
except Exception as e:
    LOGGER(__name__).warning(f"Heroku setup skipped: {e}")

# Main clients
app = JARVIS()
userbot = Userbot()

# Platform APIs
from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
