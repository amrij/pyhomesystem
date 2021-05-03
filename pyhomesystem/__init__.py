""" Nothing to see here """
import sys

__version__ = "0.10"

__uri__ = 'https://github.com/amrij/homesystem/'
__title__ = "pyhomesystem"
__description__ = 'Interface Library for homesyetem Protocol'
__doc__ = __description__ + " <" + __uri__ + ">"
__author__ = 'André Rijkeboer'
__email__ = 'a.m.rijkeboer@am-rijkeboer.nl'
__license__ = "Apache 2.0"

__copyright__ = "Copyright (c) 2021 André Rijkeboer"

from .homesystem import (
    HomesystemListener,
)

if __name__ == '__main__': print(__version__)
