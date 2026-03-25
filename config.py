import os
from datetime import datetime

# --- Bot Credentials ---
API_ID = 33603336
API_HASH = "c9683a8ec3b886c18219f650fc8ed429"
BOT_TOKEN = "8596765113:AAE0P2S5mis_cEVdi2G7Jk9mzamSwI6d74M"
SESSION_STRING = "BQE-4i0AVPV35mkI1BqgaEEfuzvz5ASTnP1DHbJ9JQbv0Ue-M2d2BZAktDico03TEuCfC85PLPYW27YnxAIAu_XyFeCQOKULjlm3cQqV_VE34NcEzA5Syl74wWW0Rcu6W-vdQTqsEUUSZV59CCohUlGeWpvSsdRqThrF6ObM9uwPa38W1JvzZK2f4aRCwaOpXzuNMK7kP0Gqc83Ogmpu2h9In--B73jkC_EJwUOkBxr1n_-wzM8uCb_Fq3fTkQ0ov8D81xKxz_xX3rkqM-JBDVsmwYSfxmOjoY2XreSbP3tEqwcTyUJXrbmVD5KVVZ9sY-IWCiLAAYipDfjTPhSx7XjHhBBM3QAAAAHKarFXAA"
OWNER_ID = 8566803656
# config.py mein ye lines honi chahiye
API_KEY = "pePKYb9ltY"
API_URL = "http://api.nubcoder.com/info"

# --- Global Tracking ---
queues = {}
playing_messages = {} # {chat_id: message_id} - Timer edit karne ke liye
current_playing = {} # {chat_id: song_details} - Currently playing track ke liye
BOT_START_TIME = datetime.now()
