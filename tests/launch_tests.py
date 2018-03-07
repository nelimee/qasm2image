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
