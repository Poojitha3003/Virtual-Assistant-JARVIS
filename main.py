import os
import eel
from engine.features import *
from engine.command import *


def start():
    eel.init("www")
    playAssistantSound()
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host='localhost', block=True)


# Add this line to actually run the assistant
if __name__ == "__main__":
    start()