### import libraries
# for speech recognition
import speech_recognition as sr
# for media input
from pyautogui import press, keyDown, keyUp, hotkey, typewrite
# for normal key input
from pynput.keyboard import Key, Controller
# for webbrowser handling
import webbrowser
# to shut down the script
import sys
# for media playback
import pyaudio
import wave

class AudioFile:
    def __init__(self, ):

        print(">> audio file created")

    def play(self, path):
        chunk = 1024
        # open a wav format music  
        f = wave.open(path,"rb")  
        # instantiate PyAudio  
        p = pyaudio.PyAudio()  
        # open stream  
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                        channels = f.getnchannels(),  
                        rate = f.getframerate(),  
                        output = True)  
        # read data  
        data = f.readframes(chunk)  

        # play stream  
        while data:  
            stream.write(data)  
            data = f.readframes(chunk)  

        # stop stream  
        stream.stop_stream()  
        stream.close()  

        # close PyAudio  
        p.terminate()  

# set up so we can use google to actual process what we said
r = sr.Recognizer()
# create handle so we can actually simulate keystrokes through this thing
keyboard = Controller()
# is program awake/ready to take commands?
speaking = False
# media playback
media = AudioFile()
# state checking, so we dont get audio that doubles up sometimes
was_idle = True 

### functions
# google search things
def google(query):
	webbrowser.open('https://www.google.com/search?q=' + query)
# search for a video on youtube
def youtube(query):
	webbrowser.open('https://www.youtube.com/results?search_query=' + query)

### main
def main(data):
	if not speaking:
		if ("shutdown" in data) or ("shut" in data) or ("turn off" in data) or ("be quiet" in data) or ("goodnight" in data) or ("hush" in data.lower()):
			sys.exit('goodnight')
		elif ("hey buddy" in data) or ("ok buddy" in data) or ("Peabody" in data) or ("ok body" in data):
			media.play(r'media\whatsapp message.wav')
			return True
	else:
		# commodities
		if ("what" in data):
			if ("time" in data):
				google('what time is it')
			elif ("day" in data) or ("date" in data):
				google("what\'s the date " + ('today', 'tomorrow')["tomorrow" in data])
			elif ("weather" in data):
				google("what\'s the weather like " + ('today', 'tomorrow')["tomorrow" in data])
			else:
				google(data)
		elif ("define " in data):
			google(data)
		elif ("type " in data):
			typewrite(data[5:])
			press('enter')

		# windows
		elif ("open" in data):
			keyboard.press(Key.cmd_l)
			press('s')
			keyboard.release(Key.cmd_l)
			typewrite(data[5:])
			press('enter')

		# media
		elif ("media" in data) or ("song" in data) or ("Spotify" in data) or ("music" in data):
			if ("skip" in data) or ("next" in data):
				press('nexttrack')
			elif ("pause" in data) or ("play" in data) or ("resume" in data):
				press('playpause')
			elif ("restart" in data):
				press('prevtrack')
			elif ("previous" in data) or ("back" in data):
				press('prevtrack')
				press('prevtrack')

		# discord
		elif ("discord" in data) or ("Discord" in data):
			if ("deafen" in data) or ("undeafen" in data):
				keyboard.press(Key.ctrl_r)
				keyboard.press(Key.shift_r)
				keyboard.release(Key.ctrl_r)
				keyboard.release(Key.shift_r)
			elif ("mute" in data) or ("unmute" in data):
				keyboard.press(Key.ctrl_r)
				keyboard.press(Key.alt_r)
				keyboard.release(Key.ctrl_r)
				keyboard.release(Key.alt_r)

		# google
		elif ("google" in data) or ("Google" in data) or ("search" in data):
			if ("YouTube" in data):
				youtube(data[15:])
			else:
				google(data[7:])

		# back out of the command stage
		elif ("thanks buddy" in data) or ("cheers buddy" in data) or ("dismiss" in data) or ("cancel" in data) or ("nevermind" in data):
			media.play(r'media\google blip.wav')
			return False

		return True

while (True):
	with sr.Microphone() as src:
		r.adjust_for_ambient_noise(src)

		if speaking:
			print("ready")
			if was_idle:
				media.play(r'media\s9 twinkle.wav')
		else:
			print("idle")

		was_idle = speaking

		try:
			audio = r.listen(src)
			log = r.recognize_google(audio, None, "en-AU")
			print("{}".format(log))
			speaking = main(log)
		except sr.UnknownValueError:
			print("huh?")
		except sr.RequestError as e:
   			print("couldnt connect to service {0}".format(e))
