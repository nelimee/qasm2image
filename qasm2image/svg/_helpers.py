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

"""This module groups useful functions for qasm2svg.

The functions here are used in many places in the code of qasm2svg
and needed to be in a separate module.
"""
import os
from typing import Tuple, Sequence, Union
from . import _constants #pylint: disable=relative-beyond-top-level

def get_x_from_index(index: int) -> int:
    """Compute the x-coordinate with the provided x index.

    This method compute the x coordinate associated with the
    given x index. The returned value has the same dimension as
    the constants provided in _constants.py.

    Parameters:
        index (int): The circuit representation is divided in
                     columns. In each column fits a gate and some
                     additional space for gate separation. The
                     provided index represent the column in which
                     we want to plot.

    Returns:
      int: The *center* of the column that corresponds to the given
           index.
              ___________
             |           |
             |           |
             |           |
             |           |
              ‾‾‾‾‾‾‾‾‾‾‾
             ^     ^
             |     returned value
             not returned value

    """
    x_coord = _constants.REGISTER_NAME_WIDTH
    x_coord += _constants.GATE_LEFT_BORDER
    x_coord += index * (_constants.GATE_SIZE + _constants.GATE_HORIZONTAL_SPACING)
    x_coord += _constants.GATE_SIZE / 2
    return x_coord

def get_y_from_quantum_register(quantum_register_index_in_JSON: int,
                                bit_mapping: dict) -> int:
    """Compute the y-coordinate associated to the given quantum register.

    This method assumes that all the quantum registers are drawn *before* the
    classical ones.

    Parameter:
        quantum_register_index_in_JSON (int): identifier of the quantum
               register from the JSON circuit representation.
        bit_mapping (dict): the map that stores the correspondances between
               bits indices in the JSON circuit and the desired output
               indices.
               Structure:
                  {'qubits': {index_in_JSON : index_in_drawing},
                   'clbits': {index_in_JSON : index_in_drawing}}
    Returns:
      int: The y-coordinate of the line representing the quantum register
           number quantum_register_index.
    """
    y_coord = _constants.VERTICAL_BORDER
    index_to_draw = bit_mapping['qubits'][quantum_register_index_in_JSON]
    y_coord += index_to_draw * _constants.REGISTER_LINES_VERTICAL_SPACING
    return y_coord

def get_y_from_classical_register(classical_register_index_in_JSON: int,
                                  quantum_registers_number: int,
                                  bit_mapping: dict) -> int:
    """Compute the y-coordinate associated to the given classical register.

    This method assumes that all the quantum registers are drawn *before* the
    classical ones.

    Parameters:
        classical_register_index_in_JSON (int): identifier of the classical
                                from the JSON circuit representation.
        quantum_registers_number (int): Number of quantum registers in the
                                        circuit.
        bit_mapping (dict): the map that stores the correspondances between
               bits indices in the JSON circuit and the desired output
               indices.
               Structure:
                  {'qubits': {index_in_JSON : index_in_drawing},
                   'clbits': {index_in_JSON : index_in_drawing}}
    Returns:
      int: The y-coordinate of the line representing the classical register
           number classical_register_index.
    """
    y_coord = _constants.VERTICAL_BORDER
    cl_index_to_draw = bit_mapping['clbits'][classical_register_index_in_JSON]
    index_to_draw = quantum_registers_number + cl_index_to_draw
    y_coord += index_to_draw * _constants.REGISTER_LINES_VERTICAL_SPACING
    return y_coord

def get_dimensions(json_circuit, show_clbits: bool) -> Tuple[int, int]:
    """Compute the width and height of the given circuit.

    Parameter:
        json_circuit (dict): JSON representation of the circuit. Can be obtained
                             from the QASM representation by the following
                             lines of code:

          # qasm_str is the string containing the QASM code.
          ast = qiskit.qasm.Qasm(data = qasm_str).parse()
          u = qiskit.unroll.Unroller(ast, qiskit.unroll.JsonBackend(basis))
          u.execute()
          json_circuit = u.backend.circuit

        show_clbits   (bool): Flag set to True if the method should also draw
                              classical bits.
    Returns:
        tuple: The computed width and height of the given circuit.
    """

    circuit_gates_number = _get_circuit_width(json_circuit)
    register_number = json_circuit['header'].get('number_of_qubits', 0)
    if show_clbits:
        register_number += json_circuit['header'].get('number_of_clbits', 0)

    width = _constants.REGISTER_NAME_WIDTH
    width += _constants.GATE_LEFT_BORDER
    width += circuit_gates_number * (_constants.GATE_SIZE + _constants.GATE_HORIZONTAL_SPACING)
    width -= _constants.GATE_HORIZONTAL_SPACING
    width += _constants.GATE_RIGHT_BORDER

    height = _constants.VERTICAL_BORDER
    height += (register_number-1) * _constants.REGISTER_LINES_VERTICAL_SPACING
    height += _constants.VERTICAL_BORDER
    return (width, height)


def _get_circuit_width(json_circuit) -> int:
    """Compute the width of the given circuit.

    The returned width is not:
        1) A number of pixel (or cm, mm, ...)
        2) The *minimum* number of time steps needed to complete the
           circuit.

    Here the "width" is the number of columns needed to *represent clearly*
    the circuit.
    One situation where the returned integer does not correspond to the
    definition given in 2) above could be

        cx q[0], q[5];
        cx q[1], q[6];

    The 2 operations above are completely independent and could be performed
    in parallel (in one time step). But the graphic representations of these 2
    operations overlap: the CNOT lines will overlap between the qubits 1 and 5.
    This situation will then output a "width" of 2, even if the width of the
    circuit in the sense of quantum computing is 1.

    Parameters:
        json_circuit (dict): JSON representation of the circuit. Can be obtained
                             from the QASM representation by the following
                             lines of code:

          # qasm_str is the string containing the QASM code.
          ast = qiskit.qasm.Qasm(data = qasm_str).parse()
          u = qiskit.unroll.Unroller(ast, qiskit.unroll.JsonBackend(basis))
          u.execute()
          json_circuit = u.backend.circuit

    Returns:
        int: The computed width of the given circuit.
    """

    clbits_number = json_circuit['header'].get('number_of_clbits', 0)
    qubits_number = json_circuit['header'].get('number_of_qubits', 0)
    index_last_gate_on_reg = {'clbits' : [0] * max(clbits_number, 1),
                              'qubits' : [0] * max(qubits_number, 1)}
    # For each operation
    for operation in json_circuit['operations']:
        # First we compute the x-index
        current_index, (minq, maxq, minc, maxc) = get_max_index(index_last_gate_on_reg,
                                                                qubits=operation.get('qubits',
                                                                                     None),
                                                                clbits=operation.get('clbits',
                                                                                     None))
        # Update the x-index for the bits used by the current operation
        for qubit in range(minq, maxq+1):
            index_last_gate_on_reg['qubits'][qubit] = current_index+1
        for clbit in range(minc, maxc+1):
            index_last_gate_on_reg['clbits'][clbit] = current_index+1

    return max(max(index_last_gate_on_reg['clbits']),
               max(index_last_gate_on_reg['qubits']))

def get_max_index(bit_gate_rank,
                  qubits: Sequence[int] = None,
                  clbits: Sequence[int] = None) -> Tuple[int, Tuple[int, int, int, int]]:
    """Compute the maximum x index with an overlap.

    The maximum x index with an overlap is the maximum column index
    where the representation of the operation on the given bits would
    overlap with an already drawn gate representation.

    Parameters:
        bit_gate_rank (dict): Dictionnary representing the column index
                              of the last drawn gate for each bit.
           Structure: {'qubits' : [ 3,    # last drawn gate on the first qubit
                                          # is in the third column.
                                    2,
                                    ...,
                                    10 ], # last drawn gate on the last qubit
                                          # is in the tenth column.
                       'clbits' : [ 1,    # last drawn gate on the first classical
                                          # bit is on the first column.
                                    ...,
                                    0 ]
                      }
        qubits (list): Indexes of the qubits concerned by the operation.
        clbits (list): Indexes of the classical bits concerned by the operation.

    Returns:
        tuple: (max_index, (minq, maxq, minc, maxc)):
                 - max_index (int): the maximum x index with an overlap.
                 - minq      (int): smallest qubit index used.
                 - maxq      (int): greatest qubit index used.
                 - minc      (int): smallest classical bit index used.
                 - maxc      (int): greatest classical bit index used.
               You can iterate on all the register indexes where something will
               be drawn with
                 for qreg_index in range(minq, maxq+1):
                     # code
                 for creg_index in range(minq, maxq+1):
                     # code
               The ranges can be empty, i.e. it is possible that minq = 0 and
               maxq = -1 or minc = 0 and maxc = -1.
    Raises:
        RuntimeError: when no qubits and no clbits are given to the function.
    """

    if qubits is None and clbits is None:
        raise RuntimeError("get_max_index cannot be called without any register.")
    # By default, [minq,maxq] and [minc,maxc] are set to None.
    # Same for the index we are searching.
    minq, maxq, minc, maxc = None, None, None, None
    max_index_q, max_index_c = -1, -1
    # We update with the given sequences of qubits and clbits.
    if qubits is not None:
        minq = min(qubits)
        maxq = max(qubits) if clbits is None else len(bit_gate_rank['qubits'])-1
        max_index_q = max([bit_gate_rank['qubits'][qubit] for qubit in range(minq, maxq+1)])
    if clbits is not None:
        minc = min(clbits) if qubits is None else 0
        maxc = max(clbits)
        max_index_c = max([bit_gate_rank['clbits'][clbit] for clbit in range(minc, maxc+1)])

    if minq is None:
        minq, maxq = 0, -1
    if minc is None:
        minc, maxc = 0, -1

    return tuple((max(max_index_c, max_index_q),
                  tuple((minq, maxq, minc, maxc))))

def _get_text_dimensions(text:str, fontsize:int):
    try:
        import cairocffi as cairo
    except ImportError:
        return len(text) * fontsize, fontsize
    surface = cairo.SVGSurface('undefined65761354373731713.svg', 1280, 200)
    cairo_context = cairo.Context(surface)
    cairo_context.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cairo_context.set_font_size(fontsize)
    xbearing, ybearing, width, height, xadvance, yadvance = cairo_context.text_extents(text)

    # Don't forget to remove the undefined65761354373731713.svg file
    os.remove("undefined65761354373731713.svg")

    return width, height


def adapt_text_font_size(text:str,
                         desired_width:Union[int,float],
                         desired_height:Union[int,float]) -> int:
    # Take an arbitrary initial font size, big enought to lower the errors of the
    # computations below
    initial_font_size = 100
    # Draw the text. To draw the text with the best font size (not too small nor too big)
    # we compute its width with a known font size and adapt the real font size.
    text_width, text_height = _get_text_dimensions(text, initial_font_size)
    # We want to fit the full gate name to the gate box, so we compute the scaling factor
    # needed to fit the gate name.
    font_scale = max(text_width/desired_width, text_height/desired_height)
    # Finally we do the assumption that applying a scaling factor to the font size is the
    # same as applying this scaling factor to the rendered text.
    return int(initial_font_size / font_scale)
