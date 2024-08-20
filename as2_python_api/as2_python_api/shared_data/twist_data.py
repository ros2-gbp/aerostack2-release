"""Twist data wrapper."""

from __future__ import annotations

# Copyright 2022 Universidad Politécnica de Madrid
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


__authors__ = 'Miguel Fernández Cortizas, Pedro Arias Pérez, David Pérez Saura, Rafael Pérez Seguí'
__copyright__ = 'Copyright (c) 2022 Universidad Politécnica de Madrid'
__license__ = 'BSD-3-Clause'

from dataclasses import dataclass, field
import threading
from typing import Callable

lock = threading.Lock()


def lock_decor(func: Callable) -> Callable:
    """Locker."""

    def wrapper(self, *args, **kwargs) -> Callable:
        with lock:
            return func(self, *args, **kwargs)
    return wrapper


@dataclass
class TwistData:
    """Twist data [vx, vy, vz]."""

    __vx: float = field(default_factory=lambda: float('nan'))
    __vy: float = field(default_factory=lambda: float('nan'))
    __vz: float = field(default_factory=lambda: float('nan'))

    def __repr__(self) -> str:
        twist = self.twist
        return f'[{twist[0]}, {twist[1]}, {twist[2]}]'

    @property
    @lock_decor
    def twist(self) -> list[float]:
        """Locked getter."""
        return [self.__vx, self.__vy, self.__vz]

    @twist.setter
    @lock_decor
    def twist(self, twist_: list[float]) -> None:
        """Locked setter."""
        self.__vx = twist_[0]
        self.__vy = twist_[1]
        self.__vz = twist_[2]
