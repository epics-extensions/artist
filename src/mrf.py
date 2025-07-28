"""File to handle MRF timing system information."""
import data
type_MTCAEVR300U="MTCA EVR 300U"  # noqa: N816

type_PCIEEVR300="PCIe EVR 300DC"  # noqa: N816

class EVR:
    """to represent an EVR in python object."""

    def __init__(
            self: "EVR",
            data_retriever: data.AbstractDataRetriever,
            prefix:str,
            parent_id:int,
            port:int,
            desc: str,
            firmware: str,
            ) -> None:
        """Initialize EVR Class with the id and the type of the EVR."""
        self.parent_id = parent_id
        self.port = port
        self.desc = desc
        self.prefix = prefix
        self.type ="not defined"
        self.data_retriever=data_retriever
        self.firmware=firmware

    def def_frontpanel(self: "EVR")->None:
        """Build frontpanel connection of the EVR."""
        #"Please Implement this method"
        self.listFP=[]

    def def_front_univ_output(self, i)-> tuple:
        """Build frontpanel UnivOutput connection of the EVR."""
        pv_name=self.prefix+f"OutFPUV{i}-Src-RB"
        source = self.data_retriever.get(pv_name)
        if (source.startswith("Pulser")):
            pv_name_label=self.prefix+f"OutFPUV{i}-Label-I"
            label = bytes(self.data_retriever.get(pv_name_label))
            label = label.decode("utf-8").replace("\0", "")
            fp=f"UNIV{i}"
            if (label == ""):
                label=fp
            return (label,fp)
        return None

class MTCAEVR300U(EVR):
    """Class to represent MTCA EVR 300U."""

    def __init__(
            self: "MTCAEVR300U",
            data_retriever: data.AbstractDataRetriever,
            prefix:str,
            parent_id:int,
            port:int,
            desc: str,
            firmware: str,
            ) -> None:
        """Init Function of the object."""
        EVR.__init__(self,data_retriever,prefix,parent_id,port,desc,firmware)
        self.type=type_MTCAEVR300U


    def def_frontpanel(self: "EVR")->None:  # noqa: C901
        """Define front panel connection of the MTCA EVR 300U."""
        list_fp=[]
        for i in range(4):
            #FP Output
            pv_name=self.prefix+f"OutFP{i}-Src-RB"
            source = self.data_retriever.get(pv_name)
            if (source.startswith("Pulser")):
                pv_name_label=self.prefix+f"OutFP{i}-Label-I"
                label = bytes(self.data_retriever.get(pv_name_label))
                label = label.decode("utf-8").replace("\0", "")
                fp=f"OUT{i}"
                if (label == ""):
                    label=fp
                list_fp.append((label,fp))
        for i in range(2):
            #FP Input
            pv_name=self.prefix+f"In{i}-Code-Back-SP"
            pv_name_local=self.prefix+f"In{i}-Code-Ext-SP"
            event = self.data_retriever.get(pv_name)
            event_local = self.data_retriever.get(pv_name_local)

            if (event != 0 or event_local!=0):
                pv_name_label=self.prefix+f"In{i}-Label-I"
                label = bytes(self.data_retriever.get(pv_name_label))
                label = label.decode("utf-8").replace("\0", "")
                fp=f"IN{i}"
                if (label == ""):
                    label=fp
                list_fp.append((label,fp))

        for i in range(4):
            #FP Univ
            tup = self.def_front_univ_output(i)
            if (tup is not None):
                list_fp.append(tup)

        for i in range(4):
            #FP Input
            pv_name=self.prefix+f"UnivIn{i}-Code-Back-SP"
            pv_name_local=self.prefix+f"UnivIn{i}-Code-Ext-SP"
            event = self.data_retriever.get(pv_name)
            event_local = self.data_retriever.get(pv_name_local)

            if (event != 0 or event_local!=0):
                pv_name_label=self.prefix+f"UnivIn{i}-Label-I"
                label = bytes(self.data_retriever.get(pv_name_label))
                label = label.decode("utf-8").replace("\0", "")
                fp=f"UNIV{i}"
                if (label == ""):
                    label=fp
                list_fp.append((label,fp))



        self.listFP=list_fp

class PCIEVR300(EVR):
    """Class to represent MTCA EVR 300U."""

    def __init__(
            self: "PCIEVR300",
            data_retriever: data.AbstractDataRetriever,
            prefix:str,
            parent_id:int,
            port:int,
            desc: str,
            firmware: str
            ) -> None:
      """Init Function of the object."""
      EVR.__init__(self,data_retriever,prefix,parent_id,port,desc,firmware)
      self.type=type_PCIEEVR300

    def def_frontpanel(self: "EVR")->None:
        """Define front panel connection of the MTCA EVR 300U."""
        list_fp=[]
        for i in range(16):
            tup = self.def_front_univ_output(i)
            if (tup is not None):
                list_fp.append(tup)
        self.listFP=list_fp


class EVM:
    """to represent an EVM in python object."""

    def __init__(
        self: "EVM",
        data_retriever:data.AbstractDataRetriever,
        id: int,  # noqa: A002
        parent_id: int,
        port: int,
        name: str,
        firmware: str,
        master: bool,  # noqa: FBT001
    ) -> None:
        """Initialize EVR Class with the id and the type of the EVR."""
        self.data_retriever=data_retriever
        self.id = id
        self.parent_id = parent_id
        self.port = port
        self.master = master
        self.name=name
        self.firmware=firmware


def create_evr(pv_name: str,data_retriever: data.AbstractDataRetriever,) -> EVR:
    """Create an EVR object based on the provided process variable name.

    Args:
        pv_name (str): The name of the process variable.

    Returns:
        EVR: An EVR object if the PV value is successfully retrieved and processed.

    """
    pv_id = pv_name + "DC-ID-I"
    value = data_retriever.get(pv_id)
    pv_fw = pv_name + "FwVer-I"
    value_fw = data_retriever.get(pv_fw)
    evr= None
    if value is not None:
        #hardware Type
        pv_hw_type = pv_name + "HwType-I"
        hw_type = data_retriever.get(pv_hw_type)
        #Name if it has some
        pv_desc = pv_name + "Label-I"
        desc = data_retriever.get(pv_desc, as_string=True)
        if desc == "":
            pv_name2=pv_name
            for ch in ["-",":","!","$","'"]:
                pv_name2 = pv_name2.replace(ch, "_") if ch in pv_name2 else pv_name2
            desc = pv_name2

        value = int(hex(value).replace("0x", ""))
        parent_id, port = divmod(value, 10)

        if (hw_type== "mTCA-EVR-300"):
            evr = MTCAEVR300U(data_retriever,pv_name,parent_id,port, desc,value_fw)
        elif (hw_type== "PCIe-EVR-300DC"):
             evr = PCIEVR300(data_retriever,pv_name,parent_id,port, desc,value_fw)
        else:
            evr = EVR(pv_name,parent_id,port, desc)
        evr.def_frontpanel()

    return evr

def create_evm(pv_name:str, data_retriever: data.AbstractDataRetriever)->EVM:
    """Create an EVM object based on the provided process variable name.

    Args:
        pv_name (str): The name of the process variable.

    Returns:
        EVM: An EVM object if the PV value is successfully retrieved and processed.

    """
    pv_id = pv_name + "FCT-ID-I"
    value = data_retriever.get(pv_id)
    pv_fw = pv_name + "FwVer-I"
    value_fw = data_retriever.get(pv_fw)
    evm=None
    if value is not None:
        value = int(hex(value).replace("0x", ""))
        parent_id, port = divmod(value, 10)
        master=False
        name=f"EVMFanout{parent_id}{port}"
        if (value==0):
            master=True
            name="EVMMaster"
        evm = EVM(data_retriever,value,parent_id,port,name,value_fw,master)
    return evm

