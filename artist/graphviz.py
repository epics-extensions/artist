"""Generate graphviz plot."""
from graphviz import Digraph


def rank_edge(
        dot : Digraph,
        list_evms: list,
        list_evrs: list,
        output: bool,
        )-> None:
    """Rank edge to display them correctly."""
    empty=1
    rank_n=1
    with dot.subgraph() as evm_master_rank:
        evm_master_rank.attr(rank="same")
        for evm in list_evms:
            if evm.id==0:
                evm_master_rank.node(f"EVM{evm.id}")
    while empty==1:
        empty=0
        with dot.subgraph() as rank:
            rank.attr(rank="same")
            for evr in list_evrs:
                if rank_n==1:
                    if evr.parent_id==0:
                        rank.node(f"{evr.desc}")
                        empty=1
                elif evr.parent_id!=0 and len(str(evr.parent_id))==rank_n-1:
                    rank.node(f"{evr.desc}")
                    empty=1
            for evm in list_evms:
                if evm.id!=0 and rank_n==1:
                    if evm.parent_id==0:
                            rank.node(f"EVM{evm.id}")
                            empty=1
                elif evm.id!=0 and evm.parent_id!=0 and len(str(evm.id))==rank_n:
                        rank.node(f"EVM{evm.id}")
                        empty=1

        rank_n=rank_n+1
    if (output):
        with dot.subgraph() as fp_rank:
            fp_rank.attr(rank="same")
            for evr in list_evrs:
                for fp in evr.listFP:
                    fp_rank.node(f"{fp[0]}")

def generate_graphviz_plot(  # noqa: C901
        list_evrs: list,
        list_evms: list,
        output: bool,
        ) -> str:
    """Generate a graphviz plot for MRF topology.

    If output is true, it add Input/output for each front panel input/outputs.
    """
    dot = Digraph(comment="EVM and EVR Graph")

    if (output):
        output_evr= "<f0>OF| <OUT0>OUT0 |<OUT1>OUT1 |<UNIV0>UNIV0|<UNIV1>UNIV1|<UNIV2>UNIV2|<UNIV3>UNIV3|<IN0>IN0|<IN1>IN1"  # noqa: E501
    else:
        output_evr= "<f0>OF"
    output_evm= "<f1>OF1|<f2>OF2|<f3>OF3|<f4>OF4|<f5>OF5|<f6>OF6|<f7>OF7|<f8>OF8|RFIN|TTLIN"  # noqa: E501
    with dot.subgraph(name="EVMs") as c:
        c.attr(label="EVMs")
        for evm in list_evms:
            dot.node(
                    f"EVM{evm.id}",
                    label=f"EVM{evm.id}|{output_evm}",
                    shape="record",
                    style="filled",
                    fillcolor="violet",
                    )

        for evm in list_evms:
            if evm.id!= 0:
                dot.edge(
                    f"EVM{evm.id}:f8:n",
                    f"EVM{evm.parent_id}:f{evm.port}:s",
                    dir="both",
                    color="orange",
                    style="bold",
                    )
                dot.edge(f"EVM{evm.parent_id}", f"EVM{evm.id}",style="invis")

    with dot.subgraph(name="EVRs") as c:
        c.attr(label="EVRs")
        for evr in list_evrs:
            dot.node(
                f"{evr.desc}",
                label=f"{evr.desc}|{output_evr}",
                shape="record",
                style="filled",
                fillcolor="lightgreen",
                )
            if evr.port!=0:
                dot.edge(
                    f"{evr.desc}:f0:n",
                    f"EVM{evr.parent_id}:f{evr.port}:s",
                    dir="both",
                    color="orange",
                    style="bold")
            # Invisible edge to force verticality
            dot.edge(f"EVM{evr.parent_id}", f"{evr.desc}",style="invis")

    if (output):
        with dot.subgraph(name="FPs") as c:
            c.attr(label="FPs")
            for evr in list_evrs:
                i=0
                for fp in evr.listFP:
                    i=i+1
                    dot.node(
                        f"{fp[0]}",
                        label=f"{fp[0]}",
                        shape="record",
                        style="filled",
                        fillcolor="lightblue",
                    )
                    stdir = "back" if fp[1].startswith("IN") else "forward"
                    dot.edge(
                        f"{evr.desc}:{fp[1]}:s",
                        f"{fp[0]}:n",
                        color="black",
                        style="bold",
                        dir=f"{stdir}")

    rank_edge(dot,list_evms,list_evrs,output)

    dot.attr(rankdir="TB")
    dot.graph_attr["splines"] = "false"
    dot.graph_attr["ranksep"] = "1.0"
    dot.graph_attr["pack"] = "true"
    dot.graph_attr["packmode"] = "clust"
    dot.render("evm_evr_graph", format="png", view=True)
