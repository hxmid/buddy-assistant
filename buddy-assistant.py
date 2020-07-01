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

# set up so we can use google to actual process what we said
r = sr.Recognizer()
# create handle so we can actually simulate keystrokes through this thing
keyboard = Controller()
# is program awake/ready to take commands?
speaking = False

### functions
# google search things
def google(query):
	webbrowser.open('https://www.google.com/search?q=' + query)
# search for a video on youtube
def youtube(query):
	webbrowser.open('https://www.youtube.com/results?search_query=' + query)
### main
def main():
	if not speaking:
		if ("shutdown" in log) or ("shut" in log) or ("turn off" in log) or ("be quiet" in log) or ("goodnight" in log) or ("hush" in log.lower()):
			sys.exit('goodnight')
		elif ("hey buddy" in log) or ("ok buddy" in log) or ("Peabody" in log) or ("ok body" in log):
			return True
	else:
		# commodities
		if ("what" in log):
			if ("time" in log):
				google('what time is it')
			elif ("day" in log) or ("date" in log):
				google("what\'s the date " + ('today', 'tomorrow')["tomorrow" in log])
			elif ("weather" in log):
				google("what\'s the weather like " + ('today', 'tomorrow')["tomorrow" in log])
			else:
				google(log)
		elif ("define" in log):
			google(log)

		# windows
		elif ("open" in log):
			keyboard.press(Key.cmd_l)
			press('s')
			keyboard.release(Key.cmd_l)
			typewrite(log[5:])
			press('enter')

		# media
		elif ("media" in log) or ("song" in log) or ("Spotify" in log) or ("music" in log):
			if ("skip" in log) or ("next" in log):
				press('nexttrack')
			elif ("pause" in log) or ("play" in log) or ("resume" in log):
				press('playpause')
			elif ("restart" in log):
				press('prevtrack')
			elif ("previous" in log) or ("back" in log):
				press('prevtrack')
				press('prevtrack')

		# discord
		elif ("discord" in log) or ("Discord" in log):
			if ("deafen" in log) or ("undeafen" in log):
				keyboard.press(Key.ctrl_r)
				keyboard.press(Key.shift_r)
				keyboard.release(Key.ctrl_r)
				keyboard.release(Key.shift_r)
			elif ("mute" in log) or ("unmute" in log):
				keyboard.press(Key.ctrl_r)
				keyboard.press(Key.alt_r)
				keyboard.release(Key.ctrl_r)
				keyboard.release(Key.alt_r)

		# google
		elif ("google" in log) or ("Google" in log) or ("search" in log):
			if ("YouTube" in log):
				youtube(log[15:])
			else:
				google(log[7:])
		return False

while (True):
	with sr.Microphone() as src:
		r.adjust_for_ambient_noise(src)

		if speaking:
			print("ready")
		else:
			print("idle")

		try:
			audio = r.listen(src)
			log = r.recognize_google(audio)
			print("{}".format(log))
			speaking = main()
		except sr.UnknownValueError:
			print("huh?")
		except sr.RequestError as e:
   			print("couldnt connect to service {0}".format(e))
