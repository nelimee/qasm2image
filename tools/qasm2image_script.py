#!/usr/bin/env python3

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

"""Command line interface to the qasm2* functions.

Type './qasm2image.py -h' for more informations.
"""


def main():
    """Main function executed if this file is directly launched with Python."""
    # 1. Argument parsing.
    import argparse
    argument_parser = argparse.ArgumentParser(
        description='Transform a quantum circuit in QASM format to an '
                    'image format.')

    argument_parser.add_argument('input_file',
                                 help='the QASM file implementing the circuit '
                                      'to transform')
    argument_parser.add_argument('output_file',
                                 help='the image file that will be generated '
                                      'by the tool')
    argument_parser.add_argument('-b', '--basis', default=(
        'id,u0,u1,u2,u3,x,y,z,h,s,sdg,t,tdg,rx,ry,rz,'
        'cx,cy,cz,ch,crz,cu1,cu3,swap,ccx'),
                                 help='a comma-separated list of gate names '
                                      'which represent the gate basis in '
                                      'which the circuit will be decomposed')
    argument_parser.add_argument('--hide-clbits', action='store_true',
                                 help='if present, classical bits will not be '
                                      'represented')
    argument_parser.add_argument('-s', '--scale', default=1, type=float,
                                 help='scale of the image. SVG output is not '
                                      'affected by this parameter')
    arguments = argument_parser.parse_args()

    # 2. Drawing.
    from qasm2image.qasm2svg import qasm2svg
    from qasm2image.qasm2png import qasm2png
    from qasm2image.qasm2ps import qasm2ps
    from qasm2image.qasm2pdf import qasm2pdf

    # Read the QASM code.
    with open(arguments.input_file, 'r') as qasm_file:
        qasm_str = qasm_file.read()

    if arguments.output_file.endswith('.svg'):
        with open(arguments.output_file, 'w') as svg_file:
            svg_file.write(
                qasm2svg(qasm_str, arguments.basis, not arguments.hide_clbits))
    elif arguments.output_file.endswith('.png'):
        with open(arguments.output_file, 'wb') as png_file:
            png_file.write(
                qasm2png(qasm_str, arguments.basis, not arguments.hide_clbits,
                         arguments.scale))
    elif arguments.output_file.endswith('.ps'):
        with open(arguments.output_file, 'wb') as ps_file:
            ps_file.write(
                qasm2ps(qasm_str, arguments.basis, not arguments.hide_clbits,
                        arguments.scale))
    elif arguments.output_file.endswith('.pdf'):
        with open(arguments.output_file, 'wb') as pdf_file:
            pdf_file.write(
                qasm2pdf(qasm_str, arguments.basis, not arguments.hide_clbits,
                         arguments.scale))
    else:
        raise NotImplementedError(
            "The output type you wanted is not implemented! Time has "
            "come to implement it by your own.")


if __name__ == '__main__':
    main()
