import numpy as np
import pyaudio
import threading
from utils import *

class Sender:
    def __init__(self, start_freq=18500):
        # initialize frequency related variables with default values
        self.start_freq = start_freq
        self.freq_range = 500
        self.sampling_rate = 44100
        self.bytes_per_transmit = 1

        # initialize stream variables
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)

    def transmit_string(self, data):
        data_list = string_to_binary(data)
        play_data(data_list, self.start_freq, self.freq_range, self.bytes_per_transmit, self.stream)

    def send_data(self):
        while True:
            user_input = input("Enter data to send: ")
            if user_input == "exit" or user_input == "q":
                self.stream.stop_stream()
                self.stream.close()
                break
            self.transmit_string(user_input)


def main():
    sender = Sender()

    # Create a thread for sending data
    send_thread = threading.Thread(target=sender.send_data)

    # Start the threads
    send_thread.start()


if __name__ == "__main__":
    main()
