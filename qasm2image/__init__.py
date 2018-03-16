
import sys

from . import qasm2svg
from . import qasm2png



setattr(sys.modules[__name__], "qasm2svg", qasm2svg.qasm2svg)
setattr(sys.modules[__name__], "qasm2png", qasm2png.qasm2png)
