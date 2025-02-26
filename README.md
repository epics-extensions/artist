# ARTIST
#### Advanced Representation of MRF TIming System Topology

This script takes a file in input with the EPICS Prefix used to control every EVMs and EVRs of your system. It results a mermaid graph representing your timing topology and to which port each EVRs is connected to EVMs.


``` mermaid
flowchart
  2 <-->|Port 1| 21[mTCA-EVR-300\nEVR2]
  2 <-->|Port 2| 22[mTCA-EVR-300\nEVR4]
  0[EVM Master] <-->|Port 1| 1[mTCA-EVR-300\n EVR1]
  0[EVM Master] <-->|Port 3| 3[PCIe-EVR-300DC\n EVR3 PCI] 
  0[EVM Master] <-->|Port 2| 2[EVM Fanout]
```

## Installation
### using Poetry

First, install Poetry.
Refer to the [Poetry](https://duckduckgo.com) for instructions.

To build the project,
you can run:

``` bash
poetry install
poetry run build
```
It is using PyInstaller to create a binary in **dist**

## Execution
### Using Poetry
To run the script from anywhere in the directory execute 
``` bash
poetry shell
```
Then you can call the script from anywhere
``` bash
artist fileListingPrefixes /tmp/outputPath -f wireviz --add-io
```
### Using Binary
If you have build the binary you can 
``` bash
> cd dist
> artist -h
```

## Usage
 ```
usage: artist [-h] [-v {0,1,2,3,4,5}] [-f {md,wireviz}] [--add-io] inputFile outputPath

Script to serialize EPICS records to csv file

positional arguments:
  inputFile             File containing the PVList
  outputPath            Result directory

options:
  -h, --help            show this help message and exit
  -v {0,1,2,3,4,5}, --verbosity {0,1,2,3,4,5}
                        decrease output verbosity. 5 (Critical), 4 (Error), 3 (Warning, default), 2 (Info), 1 (Debug)
  -f {md,wireviz}, --format {md,wireviz}
                        Define which format for the output.
  --add-io              Add input/output of the EVR on the synoptics
 ```

### Format 
For the following list of Prefix in the file listPrefixDevices
```
SL-TMG-TIM:TIM-EVM-1:
SL-MPS-BDM:TIM-EVR-1:
SL-MPS-SBCT:TIM-EVR-1:
```

#### Mermaid 
Execution of the script with the format mermaid will give you that
```
> artist listPrefixDevices
graph TD;
  0[EVM Master] <-->|Port 2| 2[mTCA-EVR-300
EVR BDM]
  0[EVM Master] <-->|Port 5| 5[mTCA-EVR-300
EVR SBCT]
```

you can use https://mermaid.live to draw the mermaid result as a graph.

#### Wireviz 

Now you can also generate wireviz format synoptic https://github.com/wireviz/WireViz

⚠️ : Graphviz need to be installed in your computer, if you use the binary. No problem with poetry.
