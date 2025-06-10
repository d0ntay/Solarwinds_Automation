import orionsdk
import json
import getpass

class Node:
    def __init__(self, node_id, display_name, ip_address, vendor, model):
        self.NodeID = node_id
        self.DisplayName = display_name
        self.IPAddress = ip_address
        self.Vendor = vendor
        self.Model = model

    def to_dict(self):
        return {
            "NodeID" : self.NodeID,
            "DisplayName" : self.DisplayName,
            "IPAddress" : self.IPAddress,
            "Vendor" : self.Vendor,
            "Model" : self.Model
        }

def get_info(server, username, password, output_file):
    swis = orionsdk.SwisClient(server, username, password)

    query = """
    
    SELECT

    N.NodeID,
    N.Caption,
    N.IPAddress,
    N.Vendor,
    H.Model

    FROM

        Orion.Nodes AS N

    LEFT JOIN

        Orion.HardwareHealth.HardwareInfo AS H ON N.NodeID = H.NodeID

    """

    results = swis.query(query)['results']
    print(f"Found {len(results)} nodes.")

    nodes = []
    for result in results:
        node_id = result.get('NodeID', 'Unknown')
        display_name = result.get('Caption', 'Unknown')
        ip_address = result.get('IPAddress', 'Unknown')
        vendor = result.get('Vendor', 'Unknown')
        model = result.get('Model', 'Unknown')
        node_obj = Node(node_id, display_name, ip_address, vendor, model)
        nodes.append(node_obj.to_dict())

    with open(output_file, "w") as f:
        json.dump(nodes, f, indent=4)

    print(f"info added to {output_file}")

if __name__ == "__main__":
    get_info(
        server = "",
        username = "",
        password = getpass.getpass(),
        output_file = "test_output.json",
    )
