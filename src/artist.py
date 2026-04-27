"""CharTiming, script to build MRF topology to visual format."""

import argparse
import logging
from pathlib import Path

import epics
import yaml
from src import data, graphvizData, mermaid, mrf, wirevizData

epics.ca.HAS_NUMPY = False

def separate_pvs(list_pvs: list,data_retriever:data.AbstractDataRetriever) -> tuple:
    """Dissociate evr from evm."""
    list_evr_pvs = []
    list_evm_pvs = []
    try:
        for pv_name in list_pvs:
            evr=mrf.create_evr(pv_name,data_retriever)
            if (evr is not None):
                list_evr_pvs.append(evr)
            else:
                evm=mrf.create_evm(pv_name,data_retriever)
                if (evm is not None):
                    list_evm_pvs.append(evm)
    except Exception:
        logging.exception("PV %s : No such PV!", pv_name)

    return list_evr_pvs, list_evm_pvs

def main() -> None:
    """Program's main entry point."""
    parser = argparse.ArgumentParser(
        prog="Artist",
        description="Document EPICs daTabase",
    )
    parser = argparse.ArgumentParser(
        description="Script to draw timing topology to defined format",
    )
    parser.add_argument("inputFile", help="File containing the PVList")
    parser.add_argument("outputPath", help="Result directory")
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        choices=[0, 1, 2, 3, 4, 5],
        help="""
    decrease output verbosity. 5 (Critical), 4 (Error), 3 (Warning, default), 2 (Info), 1 (Debug)
    """,  # noqa: E501
    )
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["md","wireviz","graphviz"],
        default="md",
        help="Define which format for the output.",
    )
    parser.add_argument(
        "--add-io",
        action="store_true",
        help="Add input/output of the EVR on the synoptics",
    )

    args = parser.parse_args()
    arg_debug = logging.INFO if args.verbosity is None else args.verbosity * 10

    logging.basicConfig(level=arg_debug)
    args = parser.parse_args()
    list_pvs = []
    with open(args.inputFile, 'r') as file:
        for line in file:
            list_pvs.extend([line.strip().replace(" ", "")])
    with open(args.inputFile, "r", encoding="utf-8") as f:
        conf = yaml.safe_load(f)

    channel_data_retriever= data.ChannelAccessRetriever()
    list_evr_pvs=[]
    list_evm_pvs=[]
    sorted_evrs=[]



    for bloc in conf:
        if "evms" in bloc:
            for evm in bloc["evms"]:
                for name, infos in evm.items():
                    titre = next((x["titre"] for x in infos if "titre" in x), None)
                    description = next((x["description"] for x in infos if "description" in x), None)

                    print("name:", name)
                    print("titre:", titre)
                    print("description:", description)
                    print()
                    evm=mrf.create_evm(name,channel_data_retriever)
                    if evm is not None:
                        list_evm_pvs.append(evm) 

        if "evrs" in bloc:
            for evr in bloc["evrs"]:
                for name, infos in evr.items():
                    titre = next((x["titre"] for x in infos if "titre" in x), None)
                    description = next((x["description"] for x in infos if "description" in x), None)

                    print("name:", name.rstrip(":"))
                    print("titre:", titre)
                    print("description:", description)
                    print()
                    evr=mrf.create_evr(name,channel_data_retriever)
                    if evr is not None:
                        list_evr_pvs.append(evr)
    
            # list_evr_pvs, list_evm_pvs = separate_pvs(list_pvs,channel_data_retriever)
            if evr is not None:
                sorted_evrs = sorted(list_evr_pvs, key=lambda evr: (evr.parent_id, evr.port))

    if (args.format=="md"):
        print("md format generation")
        code = mermaid.generate_mermaid_code(
            sorted_evrs,
            list_evm_pvs,
            args.add_io,
            args.outputPath,
            )
        logging.info("Code Mermaid generated:")
    elif (args.format=="graphviz"):
        print("md format generation")
        code = graphvizData.generate_graphviz_plot(
            sorted_evrs,
            list_evm_pvs,
            args.add_io,
            )
        logging.info("networkx generated:")
    else:
        print("wireviz format generation")
        code = wirevizData.generate_wireviz_code(
            sorted_evrs,
            list_evm_pvs,
            args.add_io,
            args.outputPath,
            )
        logging.info("Code Mermaid generated:")
    print(code)

if __name__ == "__main__":
    main()
