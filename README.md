# ARTIST
Advanced Representation of MRF TIming System Topology
``` mermaid
flowchart
  2 <-->|Port 1| 21[mTCA-EVR-300]
  2 <-->|Port 2| 22[mTCA-EVR-300]
  0[EVM Master] <-->|Port 1| 1[mTCA-EVR-300]
  0[EVM Master] <-->|Port 3| 3[PCIe-EVR-300DC]
  0[EVM Master] <-->|Port 2| 2[EVM Fanout]
```
