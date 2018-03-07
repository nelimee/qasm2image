Note: The code is currently being reviewed by people to ensure that I can publish it. It will be available soon, probably before 9th of March, 2018. The following README is an overview of what is done and currently works in local, but may be subject to minor or major changes before release.

# qasm2image

The qasm2image repository provides functions to represent quantum circuits written following the [OpenQASM](https://github.com/QISKit/qiskit-openqasm) specification.

## Not supported operations (TODO)

### Classically controlled operations

#### Description

The operations controlled by classical bits are not correctly drawn.

#### Example

See test-case [`inverseqft1.qasm`](tests/qasm/inverseqft1.qasm)

## Installation

### Dependencies

All the dependencies are available via the PIP tool. See the installation instructions below.

### Installation procedure

```shell
# Cloning the git repository
git clone https://github.com/nelimeee/qasm2image.git
# Installing the dependencies locally
pip3 install --user -r qasm2image/dependencies.txt
```

You may also need to edit your Python path in order to be able to import the qasm2image module.

## Usage

### In a Python environnement

```python
# Import the functions
from qasm2svg import qasm2svg
from qasm2png import qasm2png
# Generate your QASM string (either read from a file or generate a circuit and ask for its QASM).
qasm_str = "..."
# Define the basis used to represent the circuit
basis = 'u1,u2,u3,U,cx'
# Compute the SVG representation
svg_str = qasm2svg(qasm_str, basis=basis, show_clbits=True)
# Compute the PNG representation
png_bytes = qasm2png(qasm_str, basis=basis, show_clbits=True)
# Types of the outputs
assert type(svg_str) is str
assert type(png_bytes) is bytes
# Write the result into files
with open('circuit.svg', 'w') as svg_file:
    svg_file.write(svg_str)
# Don't forget to write in *binary* mode for PNG
with open('circuit.png', 'wb') as png_file:
    png_file.write(png_bytes)
```

### In a shell environnement

A wrapper can be found in the `tools/` directory. This wrapper can be used as follow:

```shell
$ ./qasm2image.py -h
usage: qasm2image.py [-h] [-b BASIS] [--hide-clbits] [-s SCALE]
                     input_file output_file

Transform a quantum circuit in QASM format to an image format.

positional arguments:
  input_file            the QASM file implementing the circuit to transform
  output_file           the image file that will be generated by the tool

optional arguments:
  -h, --help            show this help message and exit
  -b BASIS, --basis BASIS
                        a comma-separated list of gate names which represent
                        the gate basis in which the circuit will be decomposed
  --hide-clbits         if present, classical bits will not be represented
  -s SCALE, --scale SCALE
                        scale of the PNG image. SVG output is not affected by
                        this parameter
```

## License

This project is distributed under the [CeCILL-B](http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html) license. A copy of the whole license is included
in the repository.

In order to use the work in this repository you have a strong obligation to cite (as stated in the license):

 1. The author of the work (see on my GitHub page or [mail me](mailto:adrien.suau@grenoble-inp.org) if any doubt).

 2. The CERFACS (Centre Européen de Recherche et de Formation Avancée en Calcul Scientifique).
