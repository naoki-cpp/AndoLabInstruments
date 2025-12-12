#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2023 PyMeasure Developers
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
#

import logging
from ctypes import *

from pymeasure.instruments import Instrument
from pymeasure.instruments.validators import (
    truncated_range, truncated_discrete_set,
    strict_discrete_set
)


lvdll = WinDLL("C:\\TOEI\\LabVIEW_Toei.dll")
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class toei_magnet(Instrument):
    """ Represents the toei magnet controller and provides a high-level
    interface for interacting with the instrument.

    .. code-block:: python


    """
    def __init__(self, adapter=0, **kwargs):
        super().__init__(
            adapter, "toei magnet controller", **kwargs
        )
    lvdll = WinDLL("C:\\TOEI\\LabVIEW_Toei.dll") 
    def Bx_Bz_set(self,Bx,Bz):
        magout = self.lvdll._sub_MagOut_BxBz
        magout .argtypes = [c_double, c_double]
        magout .restype = c_int
        print("magoutBxBz:",magout(float(Bx),float(Bz)))


    def origin_angle(self):
        org = self.lvdll._sub_Motor_Origin_Stop
        org.restype = c_int
        print("org:",org())

    def rotation_in_plane(self,angle,speed=0):
        if angle > 360:
            raise ValueError("Angle is too large. Angle must be set less than 360 deg.")
        move = self.lvdll._sub_Motor_Move_Stop
        move .argtypes = [c_double, c_int]
        move.restype = c_int
        print("move:",move(float(angle),int(speed)))

if __name__ == "__main__":
    mag=toei_magnet()
    mag.rotation_in_plane(0)
