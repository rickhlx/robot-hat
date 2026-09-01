#!/usr/bin/env python3
"""
Platform compatibility layer.

robot-hat targets the Raspberry Pi, but it is convenient to be able to
import and exercise the library on other machines (e.g. macOS) for
development and testing. When Pi-only hardware or dependencies are
missing, mock implementations are used instead: hardware writes are
no-ops and hardware reads return zeros.

Set the environment variable ROBOT_HAT_MOCK=1 to force the mock layer
even on a Raspberry Pi.
"""
import os
import warnings


def is_raspberry_pi():
    """
    Check whether we are running on a Raspberry Pi.

    :return: True if running on a Raspberry Pi
    :rtype: bool
    """
    try:
        with open('/proc/device-tree/model') as f:
            return 'raspberry pi' in f.read().lower()
    except OSError:
        return False


ON_RASPBERRY_PI = is_raspberry_pi() and os.environ.get('ROBOT_HAT_MOCK') != '1'

_warned = False


def warn_mock_hardware():
    """Warn once that hardware access is mocked on this platform."""
    global _warned
    if not _warned:
        _warned = True
        warnings.warn(
            "robot_hat: not running on a Raspberry Pi, hardware access is "
            "mocked (GPIO/I2C/SPI/audio writes are no-ops, reads return 0)",
            RuntimeWarning,
            stacklevel=3)


class MockGPIO:
    """RPi.GPIO module stand-in: setup/output are no-ops, input returns 0."""
    # Constants mirror RPi.GPIO so values stored by callers stay meaningful.
    BOARD = 10
    BCM = 11
    OUT = 0
    IN = 1
    HIGH = 1
    LOW = 0
    PUD_OFF = 20
    PUD_DOWN = 21
    PUD_UP = 22
    RISING = 31
    FALLING = 32
    BOTH = 33

    def setmode(self, mode):
        warn_mock_hardware()

    def getmode(self):
        return self.BCM

    def setwarnings(self, flag):
        pass

    def setup(self, channel, direction, *args, **kwargs):
        pass

    def cleanup(self, channel=None):
        pass

    def input(self, channel):
        return 0

    def output(self, channel, value):
        pass

    def add_event_detect(self, channel, edge, callback=None, bouncetime=None):
        pass

    def remove_event_detect(self, channel):
        pass

    def event_detected(self, channel):
        return False

    def wait_for_edge(self, channel, edge, *args, **kwargs):
        return None


class MockSMBus:
    """smbus.SMBus stand-in: writes are no-ops, reads return zeros."""

    def __init__(self, bus=1, *args, **kwargs):
        warn_mock_hardware()
        self.bus = bus

    def write_byte(self, addr, data):
        return None

    def write_byte_data(self, addr, reg, data):
        return None

    def write_word_data(self, addr, reg, data):
        return None

    def write_i2c_block_data(self, addr, reg, data):
        return None

    def read_byte(self, addr):
        return 0

    def read_byte_data(self, addr, reg):
        return 0

    def read_word_data(self, addr, reg):
        return 0

    def read_i2c_block_data(self, addr, reg, num):
        return [0] * num

    def close(self):
        pass


class MockSpiDev:
    """spidev.SpiDev stand-in: transfers are no-ops, reads return zeros."""
    max_speed_hz = 0
    mode = 0
    bits_per_word = 8

    def open(self, bus, device):
        warn_mock_hardware()

    def close(self):
        pass

    def xfer(self, data, *args):
        return [0] * len(data)

    def xfer2(self, data, *args):
        return [0] * len(data)

    def writebytes(self, data):
        pass

    def readbytes(self, num):
        return [0] * num


class MockSpidevModule:
    """spidev module stand-in."""
    SpiDev = MockSpiDev


class _MockAudioStream:

    def write(self, frames, *args, **kwargs):
        pass

    def stop_stream(self):
        pass

    def close(self):
        pass


class _MockPyAudioInstance:

    def open(self, *args, **kwargs):
        return _MockAudioStream()

    def terminate(self):
        pass


class MockPyAudioModule:
    """pyaudio module stand-in: playing audio does nothing."""
    paFloat32 = 1
    paInt16 = 8

    def PyAudio(self):
        warn_mock_hardware()
        return _MockPyAudioInstance()


mock_gpio = MockGPIO()
mock_pyaudio = MockPyAudioModule()
mock_spidev = MockSpidevModule()
