import yaml

import artist.mrf


def generate_wireviz_code(list_evrs: tuple, list_evms: tuple, output:bool) -> str:  # noqa: FBT001
    """Generate a WireViz YAML schema based on the provided EVR and EVM lists.

    Args:
        list_evrs (tuple): A tuple of EVR objects, where each EVR object contains
                            attributes such as 'desc', 'parent_id', and 'port'.
        list_evms (tuple): A tuple of EVM objects, where each EVM object contains
                            attributes such as 'id', 'name', and 'master'.
        output (bool): A boolean flag indicating whether to include additional pin
                       labels in the EVR connectors.

    Returns:
        str: A YAML formatted string representing the cable schema, including connectors
                ,cables, and connections.

    """
    # cables dictionnaire
    of = {
        "type": "LC/LC",
        "colors": ["PK", "PK"],
    }
    ttl = {
        "type": "LEMO",
        "colors": ["BK"],
    }
    n_cables=0
    cables_dict={}
    cables_dict["TTL"]=ttl
    # Connectors dictionnaire
    if (output):
        evr_unknown = {
            "type": "OM4",
            "pinlabels": ["OF"],
        }
        evr_u = {
            "type": artist.mrf.type_MTCAEVR300U,
            "pinlabels": ["OF",
                          "OUT0",
                          "OUT1",
                          "OUT2",
                          "OUT3",
                          "IN0",
                          "IN1",
                          "UNIV0",
                          "UNIV1",
                          "UNIV2",
                          "UNIV3",
                          ],
        }
        pci = {
            "type": artist.mrf.type_PCIEEVR300,
            "pinlabels": ["OF",
                          "UNIV0",
                          "UNIV1",
                          "UNIV2",
                          "UNIV3",
                          "UNIV4",
                          "UNIV5",
                          "UNIV6",
                          "UNIV7",
                          "UNIV8",
                          "UNIV9",
                          "UNIV10",
                          "UNIV11",
                          "UNIV12",
                          "UNIV13",
                          "UNIV14",
                          "UNIV15",
                          ],
        }
    else:
        evr_unknown = {
            "type": "OM4",
            "pinlabels": ["OF"],
        }
        evr_u = {
            "type": artist.mrf.type_MTCAEVR300U,
            "pinlabels": ["OF"],
        }
        pci = {
            "type": artist.mrf.type_PCIEEVR300,
            "pinlabels": ["OF"],
        }
    evmmaster = {
        "type": "OM4",
        "pinlabels": ["RXTX1","RXTX2","RXTX3","RXTX4","RXTX5","RXTX6","RXTX7","RXTX8"],
    }
    connector_dict={}
    n=0
    connections=[]
    for evr in list_evrs:
        sublist_connect_rx=[]
        sublist_connect_tx=[]
        n_cables=n_cables+1
        if (evr.type== artist.mrf.type_MTCAEVR300U):
            connector_dict[evr.desc]= evr_u
        elif (evr.type== artist.mrf.type_PCIEEVR300):
            connector_dict[evr.desc]= pci
        else:
            connector_dict[evr.desc]=evr_unknown
        name=f"OF{n_cables}"
        cables_dict[name]= of
        sublist_connect_rx.append({evr.desc:1})
        sublist_connect_tx.append({evr.desc:1})
        sublist_connect_rx.append({name:1})
        sublist_connect_tx.append({name:2})
        evm_parent=next((evm for evm in list_evms if evm.id == evr.parent_id), None)
        sublist_connect_rx.append({evm_parent.name:evr.port})
        sublist_connect_tx.append({evm_parent.name:evr.port})
        connections.append(sublist_connect_rx)
        connections.append(sublist_connect_tx)
        if (output):
            for fp in evr.listFP:
                sublist_connect=[]
                connector = {
                "type": fp[0],
                "style": "simple",
                }
                connector_dict[fp[0]]=connector
                sublist_connect.append({f"{fp[0]}.":1})
                sublist_connect.append({"TTL.":1})
                sublist_connect.append({evr.desc:fp[1]})
                connections.append(sublist_connect)

    for evm in list_evms:
        if evm.master:
            connector_dict["EVMMaster"]= evmmaster
        else:
            n=n+1
            n_cables=n_cables+1
            connector_dict[("EVM",n)]= evmmaster
            cables_dict[("OF",n_cables)]= of

    #Connections



    cable_schema = {
        "connectors": connector_dict,
        "cables": cables_dict,
        "connections": connections,
    }

    return  yaml.dump(
        cable_schema,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        )
