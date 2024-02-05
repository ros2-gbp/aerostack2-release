"""Different utility methods"""

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


__authors__ = "Miguel Fernández Cortizas, Pedro Arias Pérez, David Pérez Saura, Rafael Pérez Seguí"
__copyright__ = "Copyright (c) 2022 Universidad Politécnica de Madrid"
__license__ = "BSD-3-Clause"
__version__ = "0.1.0"


from math import atan2, asin
from typing import Tuple, List, TYPE_CHECKING
import importlib
from importlib.machinery import ModuleSpec
import inspect
import sys
import os

from nav_msgs.msg import Path

if TYPE_CHECKING:
    from as2_python_api.modules.module_base import ModuleBase


def euler_from_quaternion(_x: float, _y: float, _z: float, _w: float) -> Tuple[float, float, float]:
    """
    Convert a quaternion into euler angles (roll, pitch, yaw)
    roll is rotation around _x in radians (counterclockwise)
    pitch is rotation around _y in radians (counterclockwise)
    yaw is rotation around _z in radians (counterclockwise)
    """
    t_0 = +2.0 * (_w * _x + _y * _z)
    t_1 = +1.0 - 2.0 * (_x * _x + _y * _y)
    roll_x = atan2(t_0, t_1)

    t_2 = +2.0 * (_w * _y - _z * _x)
    t_2 = +1.0 if t_2 > +1.0 else t_2
    t_2 = -1.0 if t_2 < -1.0 else t_2
    pitch_y = asin(t_2)

    t_3 = +2.0 * (_w * _z + _x * _y)
    t_4 = +1.0 - 2.0 * (_y * _y + _z * _z)
    yaw_z = atan2(t_3, t_4)

    return roll_x, pitch_y, yaw_z  # in radians


def path_to_list(path: Path) -> List[List[float]]:
    """Converts path into list"""
    return list(map(lambda p: [p.pose.position.x, p.pose.position.y, p.pose.position.z],
                    path.poses))


def get_class_from_module(module_name: str) -> 'ModuleBase':
    """Get class from module name
    source: https://docs.python.org/3.10/library/importlib.html#importing-programmatically
    """
    # check if absolute name
    if 'module' not in module_name:
        module_name = f'{module_name}_module'
    spec = find_module_in_envvar(module_name)
    print(f"spec: {spec}")
    module = importlib.util.module_from_spec(spec)  # get module from spec
    sys.modules[f"{module_name}"] = module  # adding manually to loaded modules
    
    spec.loader.exec_module(module)  # load module

    # get class from module
    target = [t for t in dir(module) if "Module" in t and t != 'ModuleBase']
    return getattr(module, *target)


def find_module_in_envvar(module_name: str) -> 'ModuleSpec':
    """Search for ModuleSpec in aerostack2 modules path environment variable
    """
    as2_modules_path_list = os.getenv('AS2_MODULES_PATH').split(':')
    for module_path in as2_modules_path_list:
        spec = importlib.util.spec_from_file_location(
            module_name, module_path + f'/{module_name}.py')
        if not os.path.exists(spec.origin):
            continue
        return spec
    return None


def get_module_call_signature(module_name: str) -> inspect.Signature:
    """get call method signature from given module name

    :rtype: inspect.Signature
    """
    class_ = get_class_from_module(module_name)

    signature = inspect.signature(class_.__call__)
    return signature
