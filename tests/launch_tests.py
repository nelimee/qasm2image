#!/usr/bin/env python3

"""Transform all the QASM files in the qasm subfolder to PNG."""

import os

from qasm2png import qasm2png

this_directory = os.path.dirname(os.path.realpath(__file__)) #pylint: disable=invalid-name
test_files_directory = os.path.join(this_directory, "qasm") #pylint: disable=invalid-name

for root, dirs, files in os.walk(test_files_directory):
    for test_file in files:
        if test_file.endswith(".qasm"):

            try:
                qasm_file_path = os.path.join(root, test_file)
                print("Testing with '{}'...".format(qasm_file_path), end='', flush=True)

                with open(qasm_file_path, 'r') as qasm_file:
                    qasm_str = qasm_file.read()
                qasms = {'simple': qasm2png(qasm_str),
                         'no_clbits': qasm2png(qasm_str, show_clbits=False),
                         'other_basis': qasm2png(qasm_str, basis='x,y,z,h,cx')}
                for suffix in qasms:
                    png_file_path = os.path.join(root,
                                                 test_file.replace('.qasm',
                                                                   "_{}.png".format(suffix)))
                    with open(png_file_path, 'wb') as png_file:
                        png_file.write(qasms[suffix])
            except Exception as exception: #pylint: disable=broad-except
                print("\nException occured on file '{}' (see below for details).".format(test_file))
                print(exception)
            else:
                print(" OK")
