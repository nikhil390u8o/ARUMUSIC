import os
from datetime import datetime

# --- Bot Credentials ---
API_ID = 33603336
API_HASH = "c9683a8ec3b886c18219f650fc8ed429"
BOT_TOKEN = "8596765113:AAHBcxK0z-n53S0tCRT0oAZQqec8o6cgbO4"
SESSION_STRING = "BQE-4i0AubxlhDrH0QCZEEktdoHfmns6FTPk0s2ztOKDyKHkY5SO8dHgwOeSig7P8A3W5u9oXB3eTE8O0PtKYH9COpkRfZpkCkLjUVlee17q_lffkIl8dfV3c86vmjNR3QgdLJV8Zp9SHZfmLDnEVlZ7y7o_vdieIlSL70AjxlP_9JR4lXB67SvuoNwBFoGwZDYJ6xBdnr1I_hgDSED_JfggJcnOfG5s9uDKNlFLOJDj7-Giwqel2KW1RLBy3ms4XFs7V0PxAK8dVi12MW7eCkVyRWqXShksbhbDr4pvTDAsmwLWP79lW3ZuzYAaAOkBkgqYEAKHKMoQ5Rv5h5lIbXDfh_c4VAAAAAHKarFXAA"
OWNER_ID = 8566803656
# config.py mein ye lines honi chahiye
API_KEY = "pePKYb9ltY"
API_URL = "http://api.nubcoder.com/info"

# --- Global Tracking ---
queues = {}
playing_messages = {} # {chat_id: message_id} - Timer edit karne ke liye
current_playing = {} # {chat_id: song_details} - Currently playing track ke liye
BOT_START_TIME = datetime.now()
