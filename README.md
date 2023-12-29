# basic-ultrasonic-linklayer
A project for cs1680 using sound waves to allow two nodes to share information wirelessly - without making any noise.

To run the sender, run the following command:
``` 
python3 Sender.py
```
This will prompt the user for a message to send, and then send it to the receiver.

To run the receiver, run the following command:
```
python3 Recv.py
```
The receiver will listen for a message from the sender, and then print it to the console.

To run the visualizer, run the following command:
```
python3 visualizer.py
```
The visualizer will display a graph of the frequencies heard by the microphone while the program is running.

## Project Design
In Python, we used three libraries within our implementation. PyAudio was used to create a channel that allows for the transmission and reading of audio data. SciPy and Numpy were used to create frequencies, handle numeric processing, and compute Fourier transforms for signal processing. Finally, we used MatplotLib to visualize the fourier transform of the sound wave frequencies.

Our utils.py file contains helper functions that assist in the encoding and decoding of data. This includes functions that map our bits to frequencies and functions that create and send the frequencies. In our visualize.py file is the code that creates a visualizer of the frequencies that our computer’s microphone picks up, which we used for presentation and debugging purposes.

To implement the link layer, we created two classes, a receiver and a sender. Similar to a radio, our receiver and sender classes must share the same initial frequency setting values such that they send and listen to the correct range of frequencies, sharing the same: starting_frequency, frequency_range, sampling_rate, bytes_per_transmit. These values must be shared in order for the receiver and sender to communicate properly. 
The sender class starts a thread that hangs on user input, the data we want to send. It then processes the inputted data, converting each data into its 8 bit representation. It then maps the bits to the frequencies that should be sent. Then, through its stream, it sends the data, or in our case plays the frequencies from our speakers.

Similarly, the receiver continuously listens for frequencies found within the agreed upon frequency range. When it hears data within that range, it proceeds to process it. Our receive process uses a protocol we decided to use in order to receive data more accurately. Our protocol to send waves consists of mapping a bit sequence to fundamental frequencies then summing those fundamental frequencies to build a wave. 
To map a chunk of data sequence, we take the frequency range and split it into:  8 * # of data bytes per transmission + 2 flag bits sections. The frequencies mapped to the positions that hold “1”s in the bit sequence are given a max amplitude, and the frequencies mapped to the positions of “0”s are given an amplitude of 0. This is how we encode one or more bytes as multiple fundamental frequencies inside of a soundwave.

The first flag assists with an issue that comes with transmitting the same byte back to back, for example “hello”. When transmitting the two “l”s, the bit sequence for that data is the same, so we needed a way to tell the receiver that this same bit sequence actually is a new byte that should be read into the buffer. Therefore, whenever the time to broadcast a new signal occurs, this bit is always flipped.

The second flag assists with an issue of knowing if the sender is sending data. Helping to establish whether a bit sequence of all zeros should be written into the buffer, or if any random ultrasonic wave is actually real data.

The receiver reads the broadcasted soundwave, applies the fourier transform on it, and then determines the 8 max fundamental frequencies (with amplitude greater than .125) within the frequency range of transmission. These 8 max values are decoded by directly mapping them to their representative bit sequence, and the data is written inside the buffer, if the flags are correct.
