#!/usr/bin/env python3
"""Play a sine signal."""
import argparse
import sys
import threading

import numpy as np
import sounddevice as sd

print(sd.query_devices())


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'frequency', nargs='?', metavar='FREQUENCY', type=float, default=500,
    help='frequency in Hz (default: %(default)s)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    '-a', '--amplitude', type=float, default=0.2,
    help='amplitude (default: %(default)s)')
args = parser.parse_args(remaining)

start_idx_1 = 0
start_idx_2 = 0

samplerate = sd.query_devices(args.device, 'output')['default_samplerate']

def myPlay1(fs,enable_left,enable_right):
    def callback1(outdata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        global start_idx_1
        t = (start_idx_1 + np.arange(frames)) / samplerate
        t = t.reshape(-1, 1)
        # outdata[:] = args.amplitude * np.sin(2 * np.pi * fs*1000 * t)
        data = args.amplitude * np.sin(2 * np.pi * fs*1000 * t)

        if enable_left:
            outdata[:, [0]] = data

        if enable_right:
            outdata[:, [1]] = data

        start_idx_1 += frames
    with sd.OutputStream(device=args.device, callback=callback1,
                samplerate=samplerate):
        print('haha')
        sd.sleep(5*1000)

def myPlay2(fs,enable_left,enable_right):
    def callback2(outdata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        global start_idx_2
        t = (start_idx_2 + np.arange(frames)) / samplerate
        t = t.reshape(-1, 1)
        # outdata[:] = args.amplitude * np.sin(2 * np.pi * fs*1000 * t)
        data = args.amplitude * np.sin(2 * np.pi * fs*1000 * t)

        if enable_left:
            outdata[:, [0]] = data

        if enable_right:
            outdata[:, [1]] = data

        start_idx_2 += frames
    with sd.OutputStream(device=args.device, callback=callback2,
                samplerate=samplerate):
        print('haha')
        sd.sleep(5*1000)

thread1 = threading.Thread(target=myPlay1, args=(1,True,False,))
thread1.start()

thread2 = threading.Thread(target=myPlay2, args=(3,False,True,))
thread2.start()


# def callback(outdata, frames, time, status):
#     if status:
#         print(status, file=sys.stderr)
#     global start_idx
#     t = (start_idx + np.arange(frames)) / samplerate
#     t = t.reshape(-1, 1)
#     outdata[:] = args.amplitude * np.sin(2 * np.pi * 10*1000 * t)
#     start_idx += frames


# with sd.OutputStream(device=args.device, channels=1, callback=callback,
#                 samplerate=samplerate):
#     print('haha')
#     sd.sleep(1*1000)

# def callback1(outdata, frames, time, status):
#     if status:
#         print(status, file=sys.stderr)
#     global start_idx
#     t = (start_idx + np.arange(frames)) / samplerate
#     t = t.reshape(-1, 1)
#     outdata[:] = args.amplitude * np.sin(2 * np.pi * 10*1000 * t)
#     start_idx += frames


# with sd.OutputStream(device=args.device, channels=1, callback=callback1,
#                 samplerate=samplerate):
#     print('haha')
#     sd.sleep(1*1000)

# def callback1(outdata, frames, time, status):
#     if status:
#         print(status, file=sys.stderr)
#     global start_idx
#     t = (start_idx + np.arange(frames)) / samplerate
#     t = t.reshape(-1, 1)
#     outdata[:] = args.amplitude * np.sin(2 * np.pi * 5*1000 * t)
#     start_idx += frames

# with sd.OutputStream(device=args.device, channels=1, callback=callback1,
#                         samplerate=samplerate):
#     print('#' * 80)
#     print('press Return to quit')
#     print('#' * 80)
#     input()
