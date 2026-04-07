import os
from datetime import datetime

# --- Bot Credentials ---
API_ID = 33603336
API_HASH = "c9683a8ec3b886c18219f650fc8ed429"
BOT_TOKEN = "8596765113:AAHBcxK0z-n53S0tCRT0oAZQqec8o6cgbO4"
SESSION_STRING = "BQE-4i0ANjyQ-A_OhgjBxmFES4INSXzeWBCR2WSk4Wm5h--rVYwm901Ub2JWEppMk_Me_rkmA09EZUtnkWP1dT1bWhsvNd5DqEG5qXfdBwEwl40NfKnIvKU_maLP5La5IiUs2UjGSCudXUwti5FJCegVlz3WQxh0OTWXCYqRoWaModJIV14toSrqAZmLEB1E0dP147qLnhOTZvqYid_RqiN7Lb0gCen4tjq771v21fSQKrJmu7ynmw_eoj-sm1mjF2MlspwhAeS89vslAbEvoXdoXgO7ANz8N_APw3JLhmLZHtJ4mh8J9OAkyrM1mm86unY4YJ-pnErnw9BdwkpLQGHHtg5ylQAAAAHKarFXAA"
OWNER_ID = 8566803656
# config.py mein ye lines honi chahiye
API_KEY = "pePKYb9ltY"
API_URL = "http://api.nubcoder.com/info"

# --- Global Tracking ---
queues = {}
playing_messages = {} # {chat_id: message_id} - Timer edit karne ke liye
current_playing = {} # {chat_id: song_details} - Currently playing track ke liye
BOT_START_TIME = datetime.now()
