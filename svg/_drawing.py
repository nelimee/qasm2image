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

"""This module provide the core functions for drawing a circuit in SVG.

All the functions related to SVG drawing with svgwrite and needed by qasm2svg
are in this module. The main function is draw_json_circuit, which use all the
other functions to draw a quantum circuit in SVG.

The functions use a specific data structure for keeping track of the positions
where they can draw. The variable bit_gate_rank is this data structure and is
described below:

   Structure: {'qubits' : [ 3,    # last drawn gate on the first qubit
                                  # is in the third column.
                            2,
                            ...,
                            6,    # last drawn gate on the i-th qubit
                                  # is in the sixth column.
                            ...,
                            10 ], # last drawn gate on the last qubit
                                  # is in the tenth column.
               'clbits' : [ 1,    # last drawn gate on the first classical
                                  # bit is on the first column.
                            ...,
                            0 ]
              }

Requires:
    - svgwrite module
"""

from typing import Sequence, Dict
from svgwrite import Drawing
from . import _helpers
from . import _constants

BitRankType = Dict[str, Sequence[int]] #pylint: disable=invalid-name

def _draw_classical_double_line(drawing: Drawing,
                                x1, y1, x2, y2) -> None:
    """Draw a double line between (x1,y1) and (x2,y2).

    Assumes that x1==x2 or y1==y2.
    """
    x_increment, y_increment = 0, 0
    if x1 == x2:
        x_increment = _constants.DOUBLE_LINES_SEPARATION
    elif y1 == y2:
        y_increment = _constants.DOUBLE_LINES_SEPARATION

    drawing.add(drawing.line(start=(x1 - x_increment, y1 - y_increment),
                             end=(x2 - x_increment, y2 - y_increment),
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))
    drawing.add(drawing.line(start=(x1 + x_increment, y1 + y_increment),
                             end=(x2 + x_increment, y2 + y_increment),
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))


def _draw_line_between_qubits(drawing: Drawing,
                              bit_gate_rank: BitRankType,
                              control_qubit: int,
                              target_qubit: int,
                              index_to_draw: int = None) -> None:
    if index_to_draw is None:
        index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                                  qubits=[control_qubit, target_qubit])
    x_coord = _helpers.get_x_from_index(index_to_draw)
    y1_coord = _helpers.get_y_from_quantum_register(control_qubit)
    y2_coord = _helpers.get_y_from_quantum_register(target_qubit)
    drawing.add(drawing.line(start=(x_coord, y1_coord),
                             end=(x_coord, y2_coord),
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))

def _draw_qubit_clbit_line(drawing: Drawing,
                           bit_gate_rank: BitRankType,
                           qubit: int,
                           clbit: int,
                           index_to_draw: int = None) -> None:

    if index_to_draw is None:
        index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                                  qubits=[qubit],
                                                  clbits=[clbit])
    x_coord = _helpers.get_x_from_index(index_to_draw)
    y1_coord = _helpers.get_y_from_quantum_register(qubit)
    y2_coord = _helpers.get_y_from_classical_register(clbit, len(bit_gate_rank['qubits']))

    _draw_classical_double_line(drawing, x_coord, y1_coord, x_coord, y2_coord)

def _draw_cnot_cross(drawing: Drawing,
                     x_coord: float,
                     y_coord: float) -> None:
    # Draw the circle
    _draw_gate_circle(drawing, x_coord, y_coord)

    # Draw the cross
    drawing.add(drawing.line(start=(x_coord - _constants.GATE_SIZE/2, y_coord),
                             end=(x_coord + _constants.GATE_SIZE/2, y_coord),
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))

    drawing.add(drawing.line(start=(x_coord, y_coord - _constants.GATE_SIZE/2),
                             end=(x_coord, y_coord + _constants.GATE_SIZE/2),
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))


def _draw_control_circle(drawing: Drawing,
                         x_coord: float,
                         y_coord: float,
                         desired_value: bool) -> None:
    if desired_value:
        filling_color = _constants.CONTROL_TRUE_GATE_FILL_COLOR
    else:
        filling_color = _constants.CONTROL_FALSE_GATE_FILL_COLOR

    drawing.add(drawing.circle(center=(x_coord, y_coord),
                               r=_constants.CONTROL_GATE_SIZE/2,
                               fill=filling_color,
                               stroke=_constants.GATE_BORDER_COLOR,
                               stroke_width=_constants.STROKE_THICKNESS))

def _draw_gate_circle(drawing: Drawing,
                      x_coord: float,
                      y_coord: float) -> None:
    drawing.add(drawing.circle(center=(x_coord, y_coord),
                               r=_constants.GATE_SIZE/2,
                               fill=_constants.GATE_FILL_COLOR,
                               stroke=_constants.GATE_BORDER_COLOR,
                               stroke_width=_constants.STROKE_THICKNESS))


def _draw_gate_rect(drawing: Drawing,
                    x_coord: float,
                    y_coord: float) -> None:

    drawing.add(drawing.rect(insert=(x_coord - _constants.GATE_SIZE/2,
                                     y_coord - _constants.GATE_SIZE/2),
                             size=(_constants.GATE_SIZE,
                                   _constants.GATE_SIZE),
                             fill=_constants.GATE_FILL_COLOR,
                             stroke=_constants.GATE_BORDER_COLOR,
                             stroke_width=_constants.STROKE_THICKNESS))


def _draw_measure_gate(drawing: Drawing,
                       bit_gate_rank: BitRankType,
                       measured_qubit: int,
                       target_clbit: int,
                       show_clbits: bool) -> None:
    index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                              qubits=[measured_qubit],
                                              clbits=[target_clbit])

    x_coord = _helpers.get_x_from_index(index_to_draw)
    yq_coord = _helpers.get_y_from_quantum_register(measured_qubit)
    if show_clbits:
        yc_coord = _helpers.get_y_from_classical_register(target_clbit,
                                                          len(bit_gate_rank['qubits']))
        # Draw the line between the 2 bits
        _draw_classical_double_line(drawing, x_coord, yq_coord, x_coord, yc_coord)

        # Draw the little thing that tell where we put the measure.
        drawing.add(drawing.rect(insert=(x_coord - _constants.MEASURE_GATE_CLBIT_SIZE/2,
                                         yc_coord - _constants.MEASURE_GATE_CLBIT_SIZE/2),
                                 size=(_constants.MEASURE_GATE_CLBIT_SIZE,
                                       _constants.MEASURE_GATE_CLBIT_SIZE),
                                 fill=_constants.MEASURE_GATE_CLBIT_FILL_COLOR,
                                 stroke=_constants.GATE_BORDER_COLOR,
                                 stroke_width=_constants.STROKE_THICKNESS))
        # Draw the "measure" gate.
        _draw_unitary_gate(drawing, bit_gate_rank, measured_qubit, "M", index_to_draw=index_to_draw)

    else:
        # Draw the "measure" gate.
        _draw_unitary_gate(drawing, bit_gate_rank, measured_qubit, "M" + str(target_clbit),
                           index_to_draw=index_to_draw, font_size=_constants.GATE_FONT_SIZE/2)



def _draw_unitary_gate(drawing: Drawing,                          #pylint: disable=too-many-arguments
                       bit_gate_rank: BitRankType,
                       qubit: int,
                       gate_name: str,
                       font_size: int = _constants.GATE_FONT_SIZE,
                       index_to_draw: int = None,
                       is_controlled_gate: bool = False) -> None:
    if index_to_draw is None:
        index_to_draw = bit_gate_rank['qubits'][qubit]
    x_coord = _helpers.get_x_from_index(index_to_draw)
    y_coord = _helpers.get_y_from_quantum_register(qubit)

    # Draw the good gate shape
    if is_controlled_gate:
        _draw_gate_circle(drawing, x_coord, y_coord)
    else:
        _draw_gate_rect(drawing, x_coord, y_coord)

    # Adapt the font size to the thing we want to write before drawing
    # The power 0.8 is empirical. A power function was choosen because:
    # 1. The size for 1-letter names was good (i.e. a constant factor would have
    #    changed this size, which is not what we want).
    # 2. The size for more than 1 letter names was too small (i.e. we want to
    #    divide the size by something smaller than the number of characters).
    font_size //= len(gate_name)**0.8
    drawing.add(drawing.text(gate_name,
                             # font_size/3 is an experimental value that seems to work for
                             # centering vertically the text.
                             insert=(x_coord, y_coord + font_size/3),
                             text_anchor="middle",
                             font_size=font_size))

def _draw_classically_conditioned_part(drawing: Drawing,
                                       bit_gate_rank: BitRankType,
                                       operation):
    """Draw the line and the controls for classically controlled operations.

    Arguments:
        drawing (Drawing): an instance of svgwrite.Drawing, used to write the SVG.
        bit_gate_rank (dict): see module documentation for more information on this
                              data structure.
        operation (dict): A QISKit operation. The dict has a key 'conditional'
                          associated to an other Python dict with entries:
            'type': the type of the operation. For example 'equals'.
            'mask': the classical bits used (?)
            'val' : the value compared with 'type' comparator to the classical bit.

    Raises:
        NotImplementedError: if the given operation affects more than 1 qubit.

    """

    qubits = operation['qubits']
    if len(qubits) > 1:
        raise NotImplementedError("Classically controlled multi-qubit operations are not " +
                                  "implemented for the moment.")
    total_qubits_number = len(bit_gate_rank['qubits'])
    total_clbits_number = len(bit_gate_rank['clbits'])

    # We take the binary little-endian representation of the value that should be
    # compared with the value stored in classical registers.
    # int(x, 0) let the 'int' function choose automatically the good basis.
    value = int(operation['conditional']['val'], 0)
    mask = int(operation['conditional']['mask'], 0)
    # The [2:] is to remove the "Ob" part returned by the "bin" function.
    # The [::-1] is to reverse the list order, to have a little-endian representation.
    little_endian_bit_value = bin(value)[2:][::-1]
    number_of_clbits = len(bin(mask)[2:])

    assert number_of_clbits <= total_clbits_number

    # First compute the important coordinates.
    index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                              operation.get('qubits', None),
                                              operation.get('clbits', None))
    x_coord = _helpers.get_x_from_index(index_to_draw)
    yq_coord = _helpers.get_y_from_quantum_register(qubits[0])
    yc_coord = _helpers.get_y_from_classical_register(total_clbits_number-1, total_qubits_number)
    # Then draw the double line representing the classical control.
    _draw_classical_double_line(drawing, x_coord, yq_coord, x_coord, yc_coord)

    # Finally draw all the controlled circles
    for classical_register_index in range(number_of_clbits):
        y_coord = _helpers.get_y_from_classical_register(classical_register_index,
                                                         total_qubits_number)
        clbit_should_be_1 = (classical_register_index < len(little_endian_bit_value)
                             and little_endian_bit_value[classical_register_index] == '1')
        _draw_control_circle(drawing, x_coord, y_coord, clbit_should_be_1)

def _update_data_structure(bit_gate_rank: BitRankType,
                           operation) -> None:

    # By default we increment the current index by 1
    increment = 1
    # But not when the operation is a 'barrier' operation
    if operation['name'] == 'barrier':
        increment = 0

    # Update the structure
    index_to_update, (minq, maxq, minc, maxc) = _helpers.get_max_index(bit_gate_rank,
                                                                       operation.get('qubits',
                                                                                     None),
                                                                       operation.get('clbits',
                                                                                     None))
    for qubit in range(minq, maxq+1):
        bit_gate_rank['qubits'][qubit] = index_to_update + increment
    for clbit in range(minc, maxc+1):
        bit_gate_rank['clbits'][clbit] = index_to_update + increment

def _draw_gate(drawing: Drawing,
               bit_gate_rank: BitRankType,
               operation,
               show_clbits: bool) -> None:

    unitary_gate_names = 'xyzh'
    supported_base_gates = set(unitary_gate_names)
    supported_u_gates = {"u{}".format(i) for i in [1, 2, 3]} | set(['u'])
    supported_unitary_gates = supported_base_gates | supported_u_gates
    supported_controled_gates = {"c{}".format(name) for name in supported_unitary_gates}
    supported_special_gates = set(['measure', 'barrier', 'reset'])
    supported_gates = supported_unitary_gates | supported_controled_gates | supported_special_gates

    name = operation['name']
    qubits = operation['qubits']

    if 'conditional' in operation:
        _draw_classically_conditioned_part(drawing, bit_gate_rank, operation)

    # Tags needed later
    drawing_controlled_gate = False
    index_to_draw = None

    # If it is a measure gate then call the specialized function to draw it.
    if name == 'measure':
        _draw_measure_gate(drawing, bit_gate_rank, qubits[0], operation['clbits'][0], show_clbits)

    # If it is a barrier gate then we do not draw anything
    if name == 'barrier':
        pass

    # If it is a reset gate, then draw a unitary gate with 'reset' name.
    if name == 'reset':
        _draw_unitary_gate(drawing, bit_gate_rank, qubits[0], name)

    # If the gate is a controlled one then draw the controlled part and let the
    # code just after draw the main gate.
    if name.lower().startswith('c'):
        control_qubit = qubits[0]
        target_qubit = qubits[1]
        index_to_draw, _ = _helpers.get_max_index(bit_gate_rank,
                                                  qubits=[control_qubit, target_qubit])

        # Draw the line, then the little control circle
        _draw_line_between_qubits(drawing,
                                  bit_gate_rank['qubits'],
                                  control_qubit,
                                  target_qubit,
                                  index_to_draw)
        _draw_control_circle(drawing,
                             _helpers.get_x_from_index(index_to_draw),
                             _helpers.get_y_from_quantum_register(control_qubit),
                             True)
        # Then if it's a CX gate, draw the nice CX gate.
        if name.lower() == "cx":
            _draw_cnot_cross(drawing,
                             _helpers.get_x_from_index(index_to_draw),
                             _helpers.get_y_from_quantum_register(target_qubit))
        # Else keep the information that we should draw a controlled gate.
        else:
            drawing_controlled_gate = True
            name = name[1:]
            qubits = qubits[1:]


    # Draw the main gate.
    ## 1. Special case for gates with parameters
    if operation.get('params', None):
        def _round_numeric_param(numeric_param: float) -> str:
            if abs(numeric_param) < 1e-10:
                # Avoid the "0.0"
                return "0"
            return str(round(numeric_param, _constants.PARAMETERS_ROUND_DECIMAL))

        _draw_unitary_gate(drawing,
                           bit_gate_rank,
                           qubits[0],
                           name+"({})".format(",".join(map(_round_numeric_param,
                                                           operation['params']))),
                           is_controlled_gate=drawing_controlled_gate,
                           index_to_draw=index_to_draw)

    ## 2. For all the gates without parameters, simply draw them
    elif name.lower() in supported_base_gates:
        _draw_unitary_gate(drawing,
                           bit_gate_rank,
                           qubits[0],
                           name.upper(),
                           is_controlled_gate=drawing_controlled_gate,
                           index_to_draw=index_to_draw)

    # Warn the user we encountered a non-implemented gate.
    if name.lower() not in supported_gates:
        print("WARNING: Gate '{}' is not implemented".format(name))


    # And finally take care of our data structure that keeps track of the position
    # where we want to draw.
    _update_data_structure(bit_gate_rank, operation)


def _draw_registers_lines(drawing: Drawing,
                          circuit_width: int,
                          json_circuit: str,
                          show_clbits: bool) -> None:
    # Initialise the y coordinate of the first register line
    y_coord = _constants.VERTICAL_BORDER

    # Start with quantum registers
    quantum_register_number = json_circuit['header'].get('number_of_qubits', 0)
    for _ in range(quantum_register_number):
        drawing.add(drawing.line(start=(0, y_coord),
                                 end=(circuit_width, y_coord),
                                 stroke=_constants.GATE_BORDER_COLOR,
                                 stroke_width=_constants.STROKE_THICKNESS))
        y_coord += _constants.REGISTER_LINES_VERTICAL_SPACING

    # And see if we want to plot classical registers.
    if show_clbits:
        classical_register_number = json_circuit['header'].get('number_of_clbits', 0)
        for _ in range(classical_register_number):
            _draw_classical_double_line(drawing, 0, y_coord, circuit_width, y_coord)
            y_coord += _constants.REGISTER_LINES_VERTICAL_SPACING


def _draw_json_circuit(json_circuit,
                       unit: str = 'px',
                       round_index: int = 0,
                       show_clbits: bool = True) -> str:
    """Draw a circuit represented as a JSON string.

    Args:
        json_circuit (dict): A quantum circuit in JSON format. This can be obtained with
                             the QISKit object qiskit.unroll.JsonBackend.
        unit         (str) : Unit used to draw the circuit. This parameter is not really
                             tested at the moment and values different from "px" could
                             cause the function to fail.
        round_index  (int) : Number of digits after the decimal point to keep in the SVG.
                             A value different from "0" could cause the function to fail,
                             this parameter need to be tested.
        show_clbits  (bool): True if the function should draw the classical bits, False
                             otherwise.
    Returns:
        str: SVG string representing the given circuit.
    """
    # Compute the width and height
    width, height = _helpers.get_dimensions(json_circuit, show_clbits)
    width, height = round(width, round_index), round(height, round_index)
    width_str, height_str = str(width)+unit, str(height)+unit
    # Create the drawing
    drawing = Drawing(size=(width_str, height_str))
    # Create the internal structure used by the drawing functions
    index_last_gate_on_reg = {'clbits': [0] * json_circuit['header'].get('number_of_clbits', 0),
                              'qubits': [0] * json_circuit['header'].get('number_of_qubits', 0)}

    # And draw!
    # First the registers lines
    _draw_registers_lines(drawing, width, json_circuit, show_clbits)
    # And then each gate
    for operation in json_circuit['operations']:
        _draw_gate(drawing, index_last_gate_on_reg, operation, show_clbits)
    return drawing.tostring()
