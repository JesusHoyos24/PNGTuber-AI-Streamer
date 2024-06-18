import threading
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play
import google.generativeai as genai
from Images import MortyLoop
from Images import readMorty
from Images import NormalMorty
from TwitchBot import BotReadMessages
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)  # Speed of speech
engine.setProperty('volume', 1)

#Add your google AI token here
genai.configure(api_key="TOKEN GOES HERE")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config = generation_config,
)
#Your prompt for the Ai to act like when reading and responding twitch messages
initial_prompt = "You are Morty Smith from the animated series 'Rick and Morty.' You are a nervous but good-hearted teenager who often finds himself dragged into crazy adventures by your genius yet reckless grandfather, Rick. You have a high-pitched, somewhat stuttery way of speaking, and you tend to worry a lot but ultimately want to do the right thing. You use phrases like 'Geez, Rick,' and 'Oh man,' frequently. You should respond to questions and messages in a way that reflects your personality from the show."


chat_session = model.start_chat(
    history=[{"role": "model", "parts": [{"text": initial_prompt}]}]
)

#Function to to change text to speech and alter pitch
def audio(stop_event):
    response = chat_session.send_message(Ainput)
    texto = response.text

    #Add path to a folder that you created to store audio, the audio stored here is the unmodified pitch one
    engine.save_to_file(texto, 'C:/OBS AUDIOS/test1.mp3')
    engine.runAndWait()
    audio = AudioSegment.from_file("C:/OBS AUDIOS/test1.mp3")

    pitch_shift_factor = 0.5

    pitched_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * (2.0 ** pitch_shift_factor))
    })
    output_file = "C:/OBS AUDIOS/test1.mp3"
    pitched_audio.export(output_file, format="mp3")
    TunedAudio = AudioSegment.from_mp3("C:/OBS AUDIOS/test1.mp3")
    play(TunedAudio)

    stop_event.set()



while True:
    new = BotReadMessages()

    if new is None :
        print("Nothing in chat")
    else:
        print(new)
        Ainput = new
        readMorty()

        stop_event = threading.Event()

        thread1 = threading.Thread(target=audio, args=(stop_event,))
        thread2 = threading.Thread(target=MortyLoop, args=(stop_event,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        NormalMorty()
