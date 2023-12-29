import struct
import pyaudio
from utils import *

# Receiver Class: Used to continuos listen for sound waves in the corresponding frequency range
# and decode the data being sent
class Recv:
    def __init__(self, start_freq=18500):
        # initialize frequency related variables with default values
        self.start_freq = start_freq
        self.freq_range = 500
        self.sampling_rate = 44100
        self.p = pyaudio.PyAudio()
        self.bytes_per_transmit = 1

        # initialize stream variables
        self.CHUNK = 2048 * 2
        self.FORMAT = pyaudio.paInt32
        self.CHANNELS = 1
        self.RATE = 44100
        self.pause = False

        # initialize stream object
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )

    # reads and unpacks the incoming audio stream
    def read_audio_stream(self):
        data = self.stream.read(self.CHUNK)
        data_int = struct.unpack(str(self.CHUNK) + 'i', data)
        return data_int

    # checks if the byte is safe to add to the data structure
    def safe_check_byte(self, bytes_seen):
        safe_byte = []

        if len(bytes_seen) > 0:
            for col in range(len(bytes_seen[0])):
                count1s = 0
                count0s = 0
                for row in range(len(bytes_seen)):
                    bit = bytes_seen[row][col]
                    if bit == '1':
                        count1s += 1
                    else:
                        count0s += 1
                if count1s > count0s:
                    safe_byte.append('1')
                else:
                    safe_byte.append('0')

        return safe_byte

    # listens for incoming data
    # uses two extra bits to handle data transmission protocol
    def listen(self):
        prev_is_data_flag = '0'
        prev_is_new_byte_flag = '0'

        bytes_seen = []
        recv_buffer = []

        while True:
            data = self.read_audio_stream()
            bits = wave_to_bits(data, self.start_freq, self.freq_range, self.bytes_per_transmit)

            # handle the data flags
            is_data_flag = bits[-1]
            is_new_byte_flag = bits[-2]

            if prev_is_data_flag == '0' and is_data_flag == '1':
                prev_is_data_flag = is_data_flag
                # just started receiving data
                bytes_seen = []
                recv_buffer = []
                print("started receiving data!")

            is_data_flag = bits[-1]
            if prev_is_data_flag == '0' and is_data_flag == '0':
                prev_is_data_flag = is_data_flag

                # just waiting for new data
                continue

            if prev_is_data_flag == '1' and is_data_flag == '0':
                prev_is_data_flag = is_data_flag

                # just finished the last byte of data, add it to buffer, then write buffer to terminal
                recv_buffer.append(self.safe_check_byte(bytes_seen))

                # FIXME: what to do with buffer?
                # for now print buffer as string
                buffer_as_string = ''.join([receive_string(byte) for byte in recv_buffer])
                print("data received: ", buffer_as_string)

                # clear data structure & buffer
                continue

            # at this point, we know we are receiving data
            if prev_is_new_byte_flag == is_new_byte_flag:
                prev_is_new_byte_flag = is_new_byte_flag

                # we are still receiving the same byte, store it in the data structure
                byte = bits[:-2]
                bytes_seen.append(byte)
                continue
            else:
                prev_is_new_byte_flag = is_new_byte_flag

                # we are receiving a new byte, so we need to write the old byte to the recv buffer
                recv_buffer.append(self.safe_check_byte(bytes_seen))
                # clear the data structure
                bytes_seen = []

                # append the new byte to the data structure
                byte = bits[:-2]
                bytes_seen.append(byte)
                continue


def main():
    recv = Recv()
    recv.listen()


if __name__ == "__main__":
    main()
