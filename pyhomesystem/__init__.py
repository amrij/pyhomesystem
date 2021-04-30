import sys

__version__ = "0.10"

__uri__ = 'https://github.com/amrij/pyhomesystem'
__title__ = "pyehomesystem"
__description__ = 'Interface Library for homesystem'
__doc__ = __description__ + " <" + __uri__ + ">"
__author__ = 'André Rijkeboer'
__email__ = 'root@am-rijkeboer.nl'
__license__ = "Apache 2.0"

__copyright__ = "Copyright (c) 2021 André Rijkeboer"

from .homesystem import (
    HSListener,
)

if __name__ == '__main__': print(__version__)
