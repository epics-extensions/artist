"""CharTiming, script to build MRF topology to Mermaid format."""

import argparse
import logging
from pathlib import Path

import epics

epics.ca.HAS_NUMPY = False


class EVR:
    """to represent an EVR in python object."""

    def __init__(self: "EVR", id_evr: str, type_evr: str, desc: str) -> None:
        """Initialize EVR Class with the id and the type of the EVR."""
        self.id_evr = id_evr
        self.type_evr = type_evr
        self.desc = desc


class EVM:
    """to represent an EVM in python object."""

    def __init__(
        self: "EVR",
        id_evm: str,
    ) -> None:
        """Initialize EVR Class with the id and the type of the EVR."""
        self.id_evm = id_evm


def generate_mermaid_code(list_evrs: tuple, evm_ids: tuple) -> str:
    """Built Mermaid graph."""
    mermaid_code = "graph TD;\n"

    for evr in list_evrs:
        if evr.id_evr != 0:
            parent_id, port = divmod(evr.id_evr, 10)
            if parent_id == 0:
                mermaid_code += f"  {parent_id}[EVM Master] <-->|Port {port}| {evr.id_evr}[{evr.type_evr}\n{evr.desc}]\n"  # noqa: E501
            else:
                mermaid_code += (
                    f"  {parent_id} <-->|Port {port}| {evr.id_evr}[{evr.desc}]\n"
                )

    for evm in evm_ids:
        if evm.id_evm != 0:
            parent_id, port = divmod(evm.id_evm, 10)
            if parent_id == 0:
                mermaid_code += f"  {parent_id}[EVM Master] <-->|Port {port}| {evm.id_evm}[EVM Fanout]\n"  # noqa: E501
            else:
                mermaid_code += (
                    f"  {parent_id} <-->|Port {port}| {evm.id_evm}[EVM Fanout]\n"
                )

    return mermaid_code


def separate_pvs(list_pvs: list) -> tuple:
    """Dissociate evr from evm."""
    list_evr_pvs = []
    list_evm_pvs = []
    try:
        for pv_name in list_pvs:
            pv_id = pv_name + "DC-ID-I"
            value = epics.caget(pv_id, timeout=2)
            if value is not None:
                pv_hw_type = pv_name + "HwType-I"
                hw_type = epics.caget(pv_hw_type, timeout=2)
                pv_desc = pv_name + "Label-I"
                desc = epics.caget(pv_desc, timeout=2, as_string=True)
                if desc == "":
                    desc = pv_name

                value = int(hex(value).replace("0x", ""))
                evr = EVR(value, hw_type, desc)
                list_evr_pvs.append(evr)
            else:
                pv_id = pv_name + "FCT-ID-I"
                value = epics.caget(pv_id, timeout=2)
                if value is not None:
                    value = int(hex(value).replace("0x", ""))
                    evm = EVM(value)
                    list_evm_pvs.append(evm)
    except Exception:
        logging.exception("PV %s : No such PV!", pv_name)

    return list_evr_pvs, list_evm_pvs


def main() -> None:
    """Program's main entry point."""
    parser = argparse.ArgumentParser(
        prog="Depict",
        description="Document EPICs daTabase",
    )
    parser = argparse.ArgumentParser(
        description="Script to serialize EPICS records to csv file",
    )
    parser.add_argument("inputFile", help="File containing the PVList")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        choices=[0, 1, 2, 3, 4, 5],
        help="""
    decrease output verbosity. 5 (Critical), 4 (Error), 3 (Warning, default), 2 (Info), 1 (Debug)
    """,  # noqa: E501
    )
    args = parser.parse_args()
    arg_debug = logging.WARNING if args.verbosity is None else args.verbosity * 10

    logging.basicConfig(level=arg_debug)
    args = parser.parse_args()
    list_pvs = []
    with Path.open(args.inputFile) as file:
        for line in file:
            list_pvs.append(line.strip().replace(" ", ""))

    list_evr_pvs, list_evm_pvs = separate_pvs(list_pvs)

    mermaid_code = generate_mermaid_code(list_evr_pvs, list_evm_pvs)

    logging.info("Code Mermaid generated:")
    print(mermaid_code)


if __name__ == "__main__":
    main()
