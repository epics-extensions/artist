import epics

type_MTCAEVR300U="MTCA EVR 300U"

type_PCIEEVR300="PCIe EVR 300DC"

class EVR:
    """to represent an EVR in python object."""

    def __init__(
            self: "EVR",
            prefix:str,
            parent_id:int,
            port:int,
            desc: str,
            ) -> None:
        """Initialize EVR Class with the id and the type of the EVR."""
        self.parent_id = parent_id
        self.port = port
        self.desc = desc
        self.prefix = prefix
        self.type ="not defined"

    def def_frontpanel(self: "EVR")->None:
        msg = "Please Implement this method"
        self.listFP=[]
        # raise NotImplementedError(msg)
        # listFP=[]
        # self.listFP=listFP


class MTCAEVR300U(EVR):

  def __init__(
            self: "MTCAEVR300U",
            prefix:str,
            parent_id:int,
            port:int,
            desc: str,
            ) -> None:
      EVR.__init__(self,prefix,parent_id,port,desc)
      self.type=type_MTCAEVR300U


  def def_frontpanel(self: "EVR")->None:
        listFP=[]
        for i in range(4):
            #FP Output
            pv_name=self.prefix+f"OutFP{i}-Src-RB"
            source = epics.caget(pv_name, timeout=2)
            if (source.startswith("Pulser")):
                pv_name_label=self.prefix+f"OutFP{i}-Label-I"
                label = bytes(epics.caget(pv_name_label, timeout=2)).decode("utf-8").replace("\0","")
                fp=f"OUT{i}"
                if (label == ""):
                    label=fp
                listFP.append((label,fp))
        for i in range(2):
            #FP Input
            pv_name=self.prefix+f"In{i}-Code-Back-SP"
            pv_name_local=self.prefix+f"In{i}-Code-Ext-SP"
            event = epics.caget(pv_name, timeout=2)
            event_local = epics.caget(pv_name_local, timeout=2)

            if (event != 0 or event_local!=0):
                pv_name_label=self.prefix+f"In{i}-Label-I"
                label = bytes(epics.caget(pv_name_label, timeout=2)).decode("utf-8").replace("\0","")
                fp=f"IN{i}"
                if (label == ""):
                    label=fp
                listFP.append((label,fp))

        for i in range(4):
            #FP Univ
            pv_name=self.prefix+f"OutFPUV{i}-Src-RB"
            source = epics.caget(pv_name, timeout=2)
            if (source.startswith("Pulser")):
                pv_name_label=self.prefix+f"OutFPUV{i}-Label-I"
                label = bytes(epics.caget(pv_name_label, timeout=2)).decode("utf-8").replace("\0","")
                fp=f"UNIV{i}"
                if (label == ""):
                    label=fp
                listFP.append((label,fp))
        for i in range(4):
            #FP Input
            pv_name=self.prefix+f"UnivIn{i}-Code-Back-SP"
            pv_name_local=self.prefix+f"UnivIn{i}-Code-Ext-SP"
            event = epics.caget(pv_name, timeout=2)
            event_local = epics.caget(pv_name_local, timeout=2)

            if (event != 0 or event_local!=0):
                pv_name_label=self.prefix+f"UnivIn{i}-Label-I"
                label = bytes(epics.caget(pv_name_label, timeout=2)).decode("utf-8").replace("\0","")
                fp=f"UNIV{i}"
                if (label == ""):
                    label=fp
                listFP.append((label,fp))



        self.listFP=listFP


class PCIEVR300(EVR):
    def __init__(
            self: "PCIEVR300",
            prefix:str,
            parent_id:int,
            port:int,
            desc: str,
            ) -> None:
      EVR.__init__(self,prefix,parent_id,port,desc)
      self.type=type_PCIEEVR300

    def def_frontpanel(self: "EVR")->None:
        listFP=[]
        for i in range(16):
            pv_name=self.prefix+f"OutFPUV{i}-Src-RB"
            source = epics.caget(pv_name, timeout=2)
            if (source.startswith("Pulser")):
                pv_name_label=self.prefix+f"OutFPUV{i}-Label-I"
                label = bytes(epics.caget(pv_name_label, timeout=2)).decode("utf-8").replace("\0","")
                fp=f"UNIV{i}"
                if (label == ""):
                    label=fp
                listFP.append((label,fp))
        self.listFP=listFP
class EVM:
    """to represent an EVM in python object."""

    def __init__(
        self: "EVM",
        id: int,  # noqa: A002
        parent_id: int,
        port: int,
        name: str,
        master: bool,  # noqa: FBT001
    ) -> None:
        """Initialize EVR Class with the id and the type of the EVR."""
        self.id = id
        self.parent_id = parent_id
        self.port = port
        self.master = master
        self.name=name


def create_evr(pv_name: str) -> EVR:
    """Create an EVR object based on the provided process variable name.

    Args:
        pv_name (str): The name of the process variable.

    Returns:
        EVR: An EVR object if the PV value is successfully retrieved and processed.

    """
    pv_id = pv_name + "DC-ID-I"
    value = epics.caget(pv_id, timeout=2)
    evr= None
    if value is not None:
        #hardware Type
        pv_hw_type = pv_name + "HwType-I"
        hw_type = epics.caget(pv_hw_type, timeout=2)
        #Name if it has some
        pv_desc = pv_name + "Label-I"
        desc = epics.caget(pv_desc, timeout=2, as_string=True)
        if desc == "":
            pv_name2=pv_name
            for ch in ["-",":","!","$","'"]:
                pv_name2 = pv_name2.replace(ch, "_") if ch in pv_name2 else pv_name2
            desc = pv_name2

        value = int(hex(value).replace("0x", ""))
        parent_id, port = divmod(value, 10)

        if (hw_type== "mTCA-EVR-300"):
            evr = MTCAEVR300U(pv_name,parent_id,port, desc)
        elif (hw_type== "PCIe-EVR-300DC"):
             evr = PCIEVR300(pv_name,parent_id,port, desc)
        else:
            evr = EVR(pv_name,parent_id,port, desc)
        evr.def_frontpanel()


    return evr

def create_evm(pv_name:str)->EVM:
    """Create an EVM object based on the provided process variable name.

    Args:
        pv_name (str): The name of the process variable.

    Returns:
        EVM: An EVM object if the PV value is successfully retrieved and processed.

    """
    pv_id = pv_name + "FCT-ID-I"
    value = epics.caget(pv_id, timeout=2)
    evm=None
    if value is not None:
        value = int(hex(value).replace("0x", ""))
        parent_id, port = divmod(value, 10)
        master=False
        name="EVMFanout."
        if (value==0):
            master=True
            name="EVMMaster"
        evm = EVM(value,parent_id,port,name,master)
    return evm

