
def generate_mermaid_code(list_evrs: list, list_evms: list) -> str:
    """Generate a markdown mermaid schema based on the provided EVR and EVM lists.

    Args:
        list_evrs (list): list of EVR object
        list_evms (list): list of EVM object
        output (bool): A boolean flag indicating whether to include additional pin 
                       labels in the EVR connectors.

    Returns:
        str: A YAML formatted string representing the cable schema, including connectors
                , cables, and connections.

    """
    mermaid_code = "graph TD;\n"

    for evr in list_evrs:
        if evr.parent_id == 0:
            mermaid_code += f"  {evr.parent_id}[EVM Master] <-->|Port {evr.port}| {evr.port}[{evr.type_evr}\n{evr.desc}]\n"  # noqa: E501
        else:
            mermaid_code += (
                f"  {evr.parent_id} <-->|Port {evr.port}| {evr.port}[{evr.desc}]\n"
            )

    for evm in list_evms:
        if (not evm.master):
            if evm.parent_id == 0:
                mermaid_code += f"  {evm.parent_id}[EVM Master] <-->|Port {evm.port}| {evm.port}[EVM Fanout]\n"  # noqa: E501
            else:
                mermaid_code += (
                    f"  {evm.parent_id} <-->|Port {evm.port}| {evm.port}[EVM Fanout]\n"
                )

    return mermaid_code
