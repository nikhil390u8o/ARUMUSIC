import os
from datetime import datetime

# --- Bot Credentials ---
API_ID = 33603336
API_HASH = "c9683a8ec3b886c18219f650fc8ed429"
BOT_TOKEN = "8596765113:AAHBcxK0z-n53S0tCRT0oAZQqec8o6cgbO4"
SESSION_STRING = "BQE-4i0AjY51k6Ute-R_moYODSyHLtkPT4i7dvLpvc_NGe5IselUcgz8oodFp2l2i1uocClQAMhiiCt5NGy8TJn9wUdSOlnp-30vebyM1RMl6lz9S1hsNtq09FJkznWG-QF6XRy4asg8_yQKeBGrSSqALOCkXuQHTInCC2O7sFaCnRw09iMe7Uu3-BjnqHLaRYKgvHxItYClNsyFEUPJHuWxRGtdLJOSYLXfyMoOi-5DowVwke3rC1vEQggQ4IxlP6lRNOshB9lnhUQGfnlw4FWVGplqYRZCD9Cq-dggGf-OkjB_p87jxL-eHwd-s1xRBz2SQQ6VZGCKqVhoSHUdc87ebLLfiAAAAAHKarFXAA"
OWNER_ID = 8566803656
# config.py mein ye lines honi chahiye
API_KEY = "pePKYb9ltY"
API_URL = "http://api.nubcoder.com/info"

# --- Global Tracking ---
queues = {}
playing_messages = {} # {chat_id: message_id} - Timer edit karne ke liye
current_playing = {} # {chat_id: song_details} - Currently playing track ke liye
BOT_START_TIME = datetime.now()
