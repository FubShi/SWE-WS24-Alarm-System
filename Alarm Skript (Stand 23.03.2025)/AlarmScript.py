import os
import rospy
import argparse
from std_msgs.msg import String
from threading import Thread
import pygame  # Pygame für Soundausgabe

class AlarmMode:
    def __init__(self, command):
        rospy.init_node("alarmmodus_script")
        self.alarm_mode = False
        self.alarm_active = False
        self.sound_file = "/home/ubuntu/alarm_sound_annoying.wav"

        # Pygame initialisieren
        pygame.mixer.init()

        # Subscriber für das Topic "alarm_trigger"
        rospy.Subscriber("alarm_trigger", String, self.alarm_callback)

        rospy.loginfo("Alarmmodus-Skript gestartet.")

        if command == "alarm ein":
            self.enable_alarm()
        elif command == "alarm aus":
            self.disable_alarm()

    def alarm_callback(self, msg):
        if not self.alarm_mode:
            rospy.loginfo("Alarmmodus ist ausgeschaltet. Signal ignoriert.")
            return

        rospy.loginfo(f"Signal empfangen: {msg.data}")
        self.trigger_alarm(msg.data)

    def trigger_alarm(self, signal):
        if self.alarm_active:
            rospy.loginfo("Alarm ist bereits aktiv.")
            return

        if signal == "undefiniert":
            rospy.loginfo("Undefiniertes Signal empfangen. Alarm wird aktiviert.")
            self.alarm_active = True
            Thread(target=self.play_alarm_sound, daemon=True).start()

    def play_alarm_sound(self):
        if not os.path.exists(self.sound_file):
            rospy.logwarn(f"Sounddatei nicht gefunden: {self.sound_file}")
            return

        while self.alarm_active:
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() and self.alarm_active:
                pygame.time.wait(100)

    def stop_alarm(self):
        rospy.loginfo("Alarm wird gestoppt.")
        self.alarm_active = False
        pygame.mixer.music.stop()

    def enable_alarm(self):
        self.alarm_mode = True
        rospy.loginfo("Alarmmodus eingeschaltet.")

    def disable_alarm(self):
        self.alarm_mode = False
        self.stop_alarm()
        rospy.loginfo("Alarmmodus ausgeschaltet.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Steuere den Alarmmodus. Nutze "alarm ein" oder "alarm aus".')
    parser.add_argument('command', type=str, choices=['alarm ein', 'alarm aus'], help='Befehl zur Steuerung des Alarmmodus')

    args = parser.parse_args()
    command = args.command

    try:
        AlarmMode(command)
    except rospy.ROSInterruptException:
        pass
