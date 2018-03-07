# ======================================================================
# Copyright CERFACS (February 2018)
# Contributor: Adrien Suau (suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

"""Definition of constants proper to the qasm2svg generator."""

GATE_SIZE = 100
GATE_HORIZONTAL_SPACING = 100
CONTROL_GATE_SIZE = 20
GATE_LEFT_BORDER = 100
GATE_RIGHT_BORDER = 100
MEASURE_GATE_CLBIT_SIZE = 20
GATE_FILL_COLOR = 'white'
GATE_BORDER_COLOR = 'black'
REGISTER_LINES_COLOR = 'black'
CONTROL_GATE_FILL_COLOR = 'black'
MEASURE_GATE_CLBIT_FILL_COLOR = 'black'
VERTICAL_BORDER = 100
REGISTER_LINES_VERTICAL_SPACING = 150
STROKE_THICKNESS = 3

GATE_FONT_SIZE = 90
PARAMETERS_ROUND_DECIMAL = 2


assert REGISTER_LINES_VERTICAL_SPACING > GATE_SIZE, ("Gates may vertically overlap with the " +
                                                     "given constants.")
assert VERTICAL_BORDER > GATE_SIZE/2, ("Gates may be drawn outside the image with the given " +
                                       "constants.")
