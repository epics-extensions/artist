from graphviz import Digraph

def generate_graphviz_plot(
        list_evrs: list,
        list_evms: list,
        output: bool,
        output_path:str,
        ) -> str:

    # Créer un objet Digraph
    dot = Digraph(comment='EVM and EVR Graph')
    styles = {
        'EVM': {'shape': 'box', 'style': 'filled', 'color': 'violet'},
        'EVR': {'shape': 'box', 'style': 'filled', 'color': 'lightgreen'}
    }
    if (output):
        outputEVR= "<f0>OF| OUT0 |OUT1 |UNIV0|UNIV1|UNIV2|UNIV3|IN0|IN1"
    else:
        outputEVR= "<f0>OF"
    outputEVM= "<f1>OF1|<f2>OF2|<f3>OF3|<f4>OF4|<f5>OF5|<f6>OF6|<f7>OF7|<f8>OF8|RFIN|TTLIN"
    for evm in list_evms:
        dot.node(
                f"EVM{evm.id}",
                label=f"EVM{evm.id}|{outputEVM}",
                shape='record',
                style="filled",
                fillcolor="violet",
                )
        if evm.id!= 0:
            dot.edge(
                f"EVM{evm.id}:f8:s",
                f"EVM{evm.parent_id}:f{evm.port}",
                dir="both",
                color="orange",
                style="bold",
                )
    for evr in list_evrs:
        dot.node(
            f"{evr.desc}",
            label=f"{evr.desc}|{outputEVR}",
            shape="record",
            style="filled",
            fillcolor="lightgreen",
            )
        if evr.port!=0:
            dot.edge(
                f"{evr.desc}:f0:s",
                f"EVM{evr.parent_id}:f{evr.port}",
                dir="both",
                color="orange",
                style="bold")

    dot.graph_attr["splines"] = "false"
    dot.render('evm_evr_graph', format='png', view=True)