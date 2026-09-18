# Robot Hat

Robot Hat Python library for Raspberry Pi.

Quick Links:

- [Robot Hat](#robot-hat)
  - [About Robot Hat](#about-robot-hat)
  - [Update](#update)
  - [Installation](#installation)
    - [macOS / non-Raspberry Pi development](#macos--non-raspberry-pi-development)
  - [Debug commands](#debug-commands)
  - [Trouble Shooting](#trouble-shooting)
  - [About SunFounder](#about-sunfounder)
  - [License](#license)
  - [Contact us](#contact-us)

## About Robot Hat

TODO

## Update

2026-09-01:

- Run on macOS / non-Raspberry Pi machines with mocked hardware
  (`robot_hat/_compat.py`): `RPi.GPIO`, `smbus`, `spidev` and `pyaudio` are
  replaced by mocks off-Pi, and `ROBOT_HAT_MOCK=1` forces the mock layer.
  See [macOS / non-Raspberry Pi development](#macos--non-raspberry-pi-development).
- `setup.py install` skips the apt/pip/raspi-config bootstrap when not on a Pi.
- `I2C.scan()` returns `[]` off-Pi instead of shelling out to `i2cdetect`.
- `pygame` and `numpy` are now optional for `Music`; a clear `ImportError` is
  raised only by the methods that need them.
- Fixes: `spi.py` `SPiDev` -> `SpiDev` typo; `tts.py` uses `shutil.which`
  instead of `distutils` (removed in Python 3.12); `music.py` no longer leaks
  a global "ignore" warnings filter.
- Added `tests/test_mock_platform.py` smoke test.

2021-07-05:

- New Release

## Installation

```bash
git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat
sudo python3 setup.py install

# i2c

# Install espeak

sudo apt install espeak
```

### macOS / non-Raspberry Pi development

The library targets the Raspberry Pi, but it can be installed, imported and
exercised on other machines (e.g. macOS) for development and testing. When it
detects it is not running on a Raspberry Pi, the Pi-only packages
(`RPi.GPIO`, `smbus`, `spidev`, `pyaudio`) are replaced by mocks: GPIO/I2C/SPI/
audio writes are no-ops and reads return 0. A `RuntimeWarning` is emitted once
when the mock layer is first touched.

```bash
git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat
pip3 install .
python3 -c "import robot_hat; print(robot_hat.__version__)"

# run the mock-platform smoke test
python3 -m unittest tests/test_mock_platform.py
```

Notes:

- `python3 setup.py install` skips the `apt`/`pip`/`raspi-config` bootstrap
  when not on a Raspberry Pi, so it never prompts for `sudo`.
- Config files that the Pi keeps under `/home/<user>` are stored under
  `~/.config/robot-hat/` (and `~/Music`, `~/Sound`) instead.
- The `Music` class needs pygame at runtime: `pip3 install pygame`;
  `Music.play_tone_for()` additionally needs numpy. Installing `pyaudio` is
  optional; without it, tone playback is mocked.
- `TTS` constructs fine but the actual engines (`pico2wave`, `espeak`,
  `aplay`) are Linux tools.
- Set `ROBOT_HAT_MOCK=1` to force the mock layer even on a Raspberry Pi.

## Debug commands

All command records for debug

```bash
# reinstall on the Pi after pulling changes
cd ~/robot-hat && git pull && sudo pip3 install . --break --no-deps --no-build-isolation
sudo pip3 uninstall -y robot_hat --break && sudo pip3 install ~/robot-hat --break --no-deps --no-build-isolation

# exercise the library with mocked hardware (any machine, or a Pi)
ROBOT_HAT_MOCK=1 python3 -m unittest tests/test_mock_platform.py
```


## Trouble Shooting

----------------------------------------------

## About SunFounder

SunFounder is a technology company focused on Raspberry Pi and Arduino open source community development. Committed to the promotion of open source culture, we strives to bring the fun of electronics making to people all around the world and enable everyone to be a maker. Our products include learning kits, development boards, robots, sensor modules and development tools. In addition to high quality products, SunFounder also offers video tutorials to help you make your own project. If you have interest in open source or making something cool, welcome to join us!

----------------------------------------------

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied wa rranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

{Repository Name} comes with ABSOLUTELY NO WARRANTY; for details run ./show w. This is free software, and you are welcome to redistribute it under certain conditions; run ./show c for details.

SunFounder, Inc., hereby disclaims all copyright interest in the program '{Repository Name}' (which makes passes at compilers).

Mike Huang, 21 August 2015

Mike Huang, Chief Executive Officer

Email: service@sunfounder.com, support@sunfounder.com

----------------------------------------------

## Contact us

website:
    www.sunfounder.com

E-mail:
    service@sunfounder.com, support@sunfounder.com
