from graphviz import Digraph

def generate_graphviz_plot(
        list_evrs: list,
        list_evms: list,
        output: bool,
        output_path:str,
        ) -> str:

    # Créer un graphe orienté
    dot = Digraph()

    # Styles pour les nœuds
    styles = {
        'EVM': {'shape': 'box', 'style': 'filled', 'color': 'violet'},
        'EVR': {'shape': 'box', 'style': 'filled', 'color': 'lightgreen'}
    }

    for evm in list_evms:
        dot.node(str(evm.id), label=evm.name, **styles["EVM"])
        if evm.id!= 0:
            dot.edge(
                str(evm.parent_id),
                str(evm.id),
                label=" "+str(evm.port),
                dir="both",
                color="orange",
                style="bold"
                )

    for evr in list_evrs:
        dot.node(str(evr.desc), label=evr.desc, **styles["EVR"])
        dot.edge(
            str(evr.parent_id),
            str(evr.desc),
            label=" "+str(evr.port),
            dir="both",
            color="orange",
            style="bold")
    dot.graph_attr["splines"] = "true"
    dot.render("tree_graph", format="png", view=True)