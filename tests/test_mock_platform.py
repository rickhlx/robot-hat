#!/usr/bin/env python3
"""
Smoke test for the mocked hardware layer (macOS / non-Raspberry Pi).

Run with:  ROBOT_HAT_MOCK=1 python3 -m unittest tests/test_mock_platform.py
The environment variable is set below as well so the test is hermetic even
on a Raspberry Pi.
"""
import os
import tempfile
import unittest
import warnings

os.environ['ROBOT_HAT_MOCK'] = '1'

import robot_hat  # noqa: E402
from robot_hat import (ADC, I2C, PWM, SPI, TTS, Motor, Music, Pin, Robot,  # noqa: E402
                       Servo, fileDB)
from robot_hat._compat import ON_RASPBERRY_PI  # noqa: E402
from robot_hat.utils import reset_mcu, set_volume  # noqa: E402


class MockPlatformTest(unittest.TestCase):

    def test_mock_layer_is_active(self):
        self.assertFalse(ON_RASPBERRY_PI)

    def test_pin(self):
        pin = Pin('D0', Pin.OUT)
        self.assertEqual(pin.high(), 1)
        self.assertEqual(pin.low(), 0)
        self.assertEqual(pin.value(), 0)
        button = Pin('D1', Pin.IN, Pin.PULL_UP)
        button.irq(handler=lambda ch: None, trigger=Pin.IRQ_FALLING)
        self.assertEqual(button.name(), 'GPIO18')  # board type reads 0 -> _dict_1

    def test_pwm_servo(self):
        pwm = PWM('P0')
        pwm.freq(50)
        self.assertEqual(pwm.freq(), 50)
        pwm.pulse_width_percent(50)
        servo = Servo(PWM('P1'))
        servo.angle(30)

    def test_adc_i2c_spi(self):
        self.assertEqual(ADC('A0').read(), 0)
        i2c = I2C()
        self.assertEqual(i2c.scan(), [])
        self.assertFalse(i2c.is_ready(0x14))
        SPI(0, 0)

    def test_motor(self):
        motor = Motor()
        motor.wheel(50)
        motor.wheel(-30, 0)
        motor.wheel(0, 1)

    def test_utils(self):
        reset_mcu()
        set_volume(50)  # must not shell out to sudo amixer off-Pi

    def test_tts_constructs(self):
        self.assertEqual(TTS().engine, 'pico2wave')

    def test_music_requires_pygame(self):
        try:
            import pygame  # noqa: F401
        except ImportError:
            with self.assertRaises(ImportError):
                Music()
        else:
            Music()

    def test_robot_and_filedb(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = os.path.join(tmp, 'robot-hat', 'robot-hat.conf')
            robot = Robot([10, 11, 12], 3, db=db, init_angles=[10, 45, -45])
            self.assertTrue(os.path.isfile(db))
            robot.set_offset([1, 2, 3])
            self.assertEqual(fileDB(db).get('piarm_servo_offset_list'),
                             '[1,2,3]')

    def test_mock_warning_emitted_once(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            import robot_hat._compat as compat
            compat._warned = False
            Pin('D2', Pin.OUT)
            Pin('D3', Pin.OUT)
        runtime = [w for w in caught if issubclass(w.category, RuntimeWarning)]
        self.assertEqual(len(runtime), 1)
        self.assertIn('mocked', str(runtime[0].message))

    def test_no_global_warning_filter_leak(self):
        # music.py used to alias warnings.filters and leave a global "ignore"
        self.assertFalse(any(f[0] == 'ignore' and f[2] is Warning
                             for f in warnings.filters))


if __name__ == '__main__':
    unittest.main()
