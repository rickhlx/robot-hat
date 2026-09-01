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
            "mocked (GPIO/I2C/audio writes are no-ops, reads return 0)",
            RuntimeWarning,
            stacklevel=3)


class MockSMBus:
    """smbus2.SMBus stand-in: writes are no-ops, reads return zeros."""

    def __init__(self, bus, *args, **kwargs):
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


class _MockLgpioCallback:

    def cancel(self):
        pass


class MockLgpio:
    """lgpio module stand-in: claims/writes are no-ops, reads return 0."""
    SET_PULL_NONE = 0x80
    SET_PULL_UP = 0x20
    SET_PULL_DOWN = 0x40
    RISING_EDGE = 1
    FALLING_EDGE = 2
    BOTH_EDGES = 3

    def gpiochip_open(self, gpiochip):
        warn_mock_hardware()
        return 0

    def gpiochip_close(self, handle):
        return 0

    def gpio_claim_output(self, handle, gpio, level=0, lFlags=0):
        return 0

    def gpio_claim_input(self, handle, gpio, lFlags=0):
        return 0

    def gpio_free(self, handle, gpio):
        return 0

    def gpio_read(self, handle, gpio):
        return 0

    def gpio_write(self, handle, gpio, level):
        return 0

    def callback(self, handle, gpio, edge, func):
        return _MockLgpioCallback()


class _MockAudioStream:

    def write(self, frames):
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
    paInt16 = 8

    def PyAudio(self):
        warn_mock_hardware()
        return _MockPyAudioInstance()


mock_lgpio = MockLgpio()
mock_pyaudio = MockPyAudioModule()
