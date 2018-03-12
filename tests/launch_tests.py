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

"""Transform all the QASM files in the qasm subfolder to PNG."""

import os

use_colors = True
try:
    from colorama import Fore, Style
except ImportError:
    use_colors = False
    print("colorama was not found on your Python installation. Colored output will not " +
          "work. You can install colorama with pip: 'pip install colorama'.")

import sys
import os
# Add '..' in the Python path and import qasm2png
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qasm2png import qasm2png


def recursive_check_all_qasm_files(directory, exception_expected = False):
    error_coloring_format = Fore.RED + '{}' + Style.RESET_ALL
    ok_coloring_format = Fore.GREEN + '{}' + Style.RESET_ALL
    def color_text(text, coloring_format):
        if use_colors:
            return coloring_format.format(text)
        else:
            return text

    ok_text = color_text(" OK ", ok_coloring_format)
    fail_text = color_text("FAIL", error_coloring_format)

    on_exception_str = ok_text   if exception_expected else fail_text
    no_exception_str = fail_text if exception_expected else ok_text

    for root, dirs, files in os.walk(directory):
        for test_file in files:
            if test_file.endswith(".qasm"):
                qasm_file_path = os.path.join(root, test_file)
                printed_text = "[....] Testing with '{}'".format(qasm_file_path)
                try:
                    print(printed_text, end='\r', flush=True)

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
                    print(printed_text.replace("....", on_exception_str))
                    print(exception)
                else:
                    print(printed_text.replace("....", no_exception_str))

if __name__ == '__main__':
    this_directory = os.path.dirname(os.path.realpath(__file__)) #pylint: disable=invalid-name
    test_files_directory = os.path.join(this_directory, "examples") #pylint: disable=invalid-name

    for directory in os.listdir(test_files_directory):
        current_directory = os.path.join(test_files_directory, directory)
        recursive_check_all_qasm_files(current_directory, exception_expected=(directory=="invalid"))
