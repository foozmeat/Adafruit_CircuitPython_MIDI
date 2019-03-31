# The MIT License (MIT)
#
# Copyright (c) 2019 Kevin J. Walters
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_midi`
================================================================================

A CircuitPython helper for encoding/decoding MIDI packets over a MIDI or UART connection.


* Author(s): Kevin J. Walters

Implementation Notes
--------------------

**Hardware:**



**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

from .midi_message import MIDIMessage

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MIDI.git"


class PitchBendChange(MIDIMessage):
    """Pitch Bend Change MIDI message.

    :param int pitch_bend: A 14bit unsigned int representing the degree of
        bend from 0 through 8192 (midpoint, no bend) to 16383.
    """

    _STATUS = 0xe0
    _STATUSMASK = 0xf0
    LENGTH = 3
    CHANNELMASK = 0x0f

    def __init__(self, pitch_bend):
        self.pitch_bend = pitch_bend
        if not 0 <= self.pitch_bend <= 16383:
            raise ValueError("Out of range")

    # channel value is mandatory
    def as_bytes(self, channel=None):
        return bytearray([self._STATUS | (channel & self.CHANNELMASK),
                          self.pitch_bend & 0x7f,
                          (self.pitch_bend >> 7) & 0x7f])

    @classmethod
    def from_bytes(cls, databytes):
        return cls(databytes[1] << 7 | databytes[0])

PitchBendChange.register_message_type()
