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
## Execution
### Using Poetry
To run the script from anywhere in the directory execute 
``` bash
poetry shell
```
Then you can call the script from anywhere
``` bash
spicer --PVs="Labo*" --host=myElasticSearchHost
```
### Using Binary
If you have build the binardy you can 
``` bash
> cd dist
> artist -h
```

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

## Usage
 ```
 usage: artist [-h] [-v {0,1,2,3,4,5}] inputFile

positional arguments:
  inputFile             File containing the PVList

options:
  -h, --help            show this help message and exit
  -v {0,1,2,3,4,5}, --verbosity {0,1,2,3,4,5}
                        decrease output verbosity. 5 (Critical), 4 (Error), 3 (Warning, default), 2 (Info), 1 (Debug)
 ```
For the following list of Prefix in the file listPrefixDevices
```
SL-TMG-TIM:TIM-EVM-1:
SL-MPS-BDM:TIM-EVR-1:
SL-MPS-SBCT:TIM-EVR-1:
```
Execution of the script will give you that
```
> artist listPrefixDevices
graph TD;
  0[EVM Master] <-->|Port 2| 2[mTCA-EVR-300
EVR BDM]
  0[EVM Master] <-->|Port 5| 5[mTCA-EVR-300
EVR SBCT]
```

you can use https://mermaid.live to draw the mermaid result as a graph.