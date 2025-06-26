from orionsdk import SwisClient
import json
import getpass


class Interface:
    def __init__(self, name, alias, address):
        self.Name = name
        self.Alias = alias
        self.Address = address

    def to_dict(self):
        return {"Name": self.Name, "Alias": self.Alias, "Address": self.Address }


class Node:
    def __init__(self, display_name, ip_address):
        self.DisplayName = display_name
        self.IPAddress = ip_address
        self.Interfaces = []

    def add_interface(self, interface: Interface):
        self.Interfaces.append(interface)

    def to_dict(self):
        return {
            "DisplayName": self.DisplayName,
            "IPAddress": self.IPAddress,
            "Interfaces": [iface.to_dict() for iface in self.Interfaces],
        }


def export_nodes_from_instance(hostname, username, password, output_file):
    swis = SwisClient(hostname, username, password)

    query = """
    SELECT
        N.NodeID,
        N.Caption,
        N.IPAddress,
        I.InterfaceName,
        I.InterfaceAlias,
        I.PhysicalAddress
    FROM
        Orion.Nodes N
    JOIN
        Orion.NPM.Interfaces I ON N.NodeID = I.NodeID
    WHERE
        N.ObjectSubType = 'SNMP'
    """

    results = swis.query(query)["results"]
    print(f"Found {len(results)} interface records.")

    # Organize data into Node and Interface objects
    node_dict = {}

    for row in results:
        node_key = row["Caption"]
        if node_key not in node_dict:
            node_dict[node_key] = Node(row["Caption"], row["IPAddress"])

        interface = Interface(
            name=row["InterfaceName"],
            alias=row["InterfaceAlias"],
            address=row["PhysicalAddress"],
        )
        node_dict[node_key].add_interface(interface)

    # Convert all nodes to dict and save to JSON
    json_data = [node.to_dict() for node in node_dict.values()]

    with open(output_file, "w") as f:
        json.dump(json_data, f, indent=2)

    print(f"Exported {len(json_data)} nodes to {output_file}")


# Example usage:
if __name__ == "__main__":
    export_nodes_from_instance(
        hostname="",
        username="",
        password=getpass.getpass(),
        output_file="solarwinds_nodes_export.json",
    )
