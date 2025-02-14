import sys
from pygame import mixer
import threading

VOLUME = 0.9
running = True

def play_sound():
    mixer.init()
    sound1 = mixer.Sound('/home/ubuntu/alarm_sound_annoying.wav')
    sound1.set_volume(VOLUME)

    while running:
        if not mixer.get_busy():
            sound1.play()

def main():
    global running

#Start the sound in a separate thread
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.daemon = True
    sound_thread.start()

    print("Eingabe 'alarman' zum Starten des Alarms und 'alarmaus' zum Beenden des Scripts.")
    while True:
        command = input("Befehl eingeben: ").strip().lower()

        if command == "alarmaus":
            running = False
            mixer.quit()
            print("Alarm gestoppt und Script beendet.")
            sys.exit()
        elif command == "alarman":
            print("Alarm läuft bereits.")
        else:
            print("Unbekannter Befehl. Verwenden Sie 'alarman' oder 'alarmaus'.")

if __name__ == "main":
    main()