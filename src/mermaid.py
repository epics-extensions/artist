"""Class to generate markdown mermaid synoptic."""

def generate_mermaid_code(
        list_evrs: list,
        list_evms: list,
        output: bool,
        output_path:str,
        ) -> str:
    """Generate a markdown mermaid schema based on the provided EVR and EVM lists.

    Args:
        list_evrs (list): list of EVR object
        list_evms (list): list of EVM object
        output (bool): A boolean flag indicating whether to include additional pin 
                       labels in the EVR connectors.
        output_path (str): Directory where to write the result

    Returns:
        str: A YAML formatted string representing the cable schema, including connectors
                , cables, and connections.

    """
    mermaid_code = "graph TD;\n"
    if list_evms is not None and len(list_evms) > 0:
        evm_master = next((element for element in list_evms if element.id == 0), None)
    for evr in list_evrs:
        if evr.port == 0:
            mermaid_code += f"  {evr.parent_id}{evr.port}[{evr.type}\nv{evr.firmware}\n{evr.desc}]\n"
        elif evr.parent_id == 0:
            mermaid_code += f"  {evr.parent_id}[EVM Master\nv{evm_master.firmware}] <-->|Port {evr.port}| {evr.parent_id}{evr.port}[{evr.type}\nv{evr.firmware}\n{evr.desc}]\n"  # noqa: E501
        else:
            mermaid_code += (
                f"  {evr.parent_id} <-->|Port {evr.port}| {evr.parent_id}{evr.port}[{evr.type}\nv{evr.firmware}\n{evr.desc}]\n"
            )
        i=0
        if output:
            for fp in evr.listFP:
                i=i+1
                mermaid_code += (
                    f"  {evr.parent_id}{evr.port} <-->|{fp[1]}| "
                    f"{evr.parent_id}{evr.port}{i}[{fp[0]}]\n"
                )

    for evm in list_evms:
        if (not evm.master):
            if evm.parent_id == 0:
                mermaid_code += f"  {evm.parent_id}[EVM Master {evm.firmware}] <-->|Port {evm.port}| {evm.port}[EVM Fanout {evm.firmware}]\n"  # noqa: E501
            else:
                mermaid_code += (
                    f"  {evm.parent_id} <-->|Port {evm.port}| {evm.port}[EVM Fanout {evm.firmware}]\n"
                )
    from pathlib import Path
    Path(output_path).mkdir(parents=True, exist_ok=True)
    with Path(output_path).joinpath("output.md").open("w") as f:
        f.write(mermaid_code)

    return mermaid_code
