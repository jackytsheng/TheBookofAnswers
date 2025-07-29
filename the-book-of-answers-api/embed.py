from BibleClient import BibleClient
from Config import Config

import warnings
# Disable warning from model internally

warnings.filterwarnings("ignore", category=FutureWarning)

# init config
config = Config()

# get client
client = BibleClient(config)

client.embed()
