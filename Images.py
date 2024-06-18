import time
import obswebsocket
from obswebsocket import requests

# Define the connection details for the OBS WebSocket server
host = "192.168.0.24"
port = 4444
password = "Jesus"

# Initialize the OBS WebSocket client with the specified connection details
ws = obswebsocket.obsws(host, port, password)
ws.connect()

# Define the name of the source in OBS that will be controlled
source_name = "Morty"

# Define the file paths for the different images of Morty
MortyLookingDown = "C:/Users/Jesús/Downloads/luffy images OBS/morty looking down.png"
MortyNormal = "C:/Users/Jesús/Downloads/luffy images OBS/morty normal (1).jpg"

# List of images to cycle through when Morty is talking
MortyImagesTalking = [
    "C:/Users/Jesús/Downloads/luffy images OBS/morty 1.png",
    "C:/Users/Jesús/Downloads/luffy images OBS/morty5.png",
    "C:/Users/Jesús/Downloads/luffy images OBS/morty3.png",
    "C:/Users/Jesús/Downloads/luffy images OBS/morty4.png",
    "C:/Users/Jesús/Downloads/luffy images OBS/morty 2.png"
]

# Function to set Morty's image to "looking down" for 1 second, then back to normal
def readMorty():
    response = ws.call(requests.SetSourceSettings(sourceName=source_name, sourceSettings={"file": MortyLookingDown}))
    time.sleep(1)
    response = ws.call(requests.SetSourceSettings(sourceName=source_name, sourceSettings={"file": MortyNormal}))

# Function to set Morty's image to "normal"
def NormalMorty():
    response = ws.call(requests.SetSourceSettings(sourceName=source_name, sourceSettings={"file": MortyNormal}))

# Function to continuously cycle through the talking images in a loop
# The loop stops when the stop_event is set
def MortyLoop(stop_event):
    time.sleep(1.3)

    while not stop_event.is_set():
        for item in MortyImagesTalking:
            if stop_event.is_set():
                break
            time.sleep(0.1)
            response = ws.call(requests.SetSourceSettings(sourceName=source_name, sourceSettings={"file": item}))

if __name__ == "__main__":
    pass
