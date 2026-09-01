#!/usr/bin/env python3
from ._compat import ON_RASPBERRY_PI
if ON_RASPBERRY_PI:
    import spidev
else:
    from ._compat import mock_spidev as spidev


class SPI(object):
    def __init__(self, bus, device):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
