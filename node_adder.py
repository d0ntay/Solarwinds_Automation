from orionsdk import SwisClient
import json
import time
import getpass
import urllib3

# Disable SSL warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up SolarWinds connection
TARGET_SW_HOST = ""
USERNAME = ""  # Make sure to double backslash
PASSWORD = getpass.getpass("Enter your SolarWinds password: ")
JSON_FILE = "nodes_export_with_snmpv3.json"

swis = SwisClient(TARGET_SW_HOST, USERNAME, PASSWORD)


def add_node(node):
    try:
        print(f"Adding node: {node['DisplayName']} ({node['IPAddress']})")

        snmpv3 = node["SNMPv3"]

        node_props = {
            "IPAddress": node["IPAddress"],
            "EngineID": 1,
            "EntityType": "Orion.Nodes",
            "ObjectSubType": "SNMP",
            "SysName": node["DisplayName"],
            "Caption": node["DisplayName"],
            "SNMPVersion": 3,
            "SNMPV3Username": snmpv3["Username"],
            "SNMPV3AuthMethod": snmpv3["AuthMethod"],
            "SNMPV3AuthKey": snmpv3["AuthKey"],
            "SNMPV3PrivMethod": snmpv3["PrivMethod"],
            "SNMPV3PrivKey": snmpv3["PrivKey"],
            "SNMPV3Context": snmpv3.get("Context", ""),
        }

        node_uri = swis.create("Orion.Nodes", **node_props)
        print(f"Node created → {node_uri}")
        node_id = int(node_uri.split("=")[1]) 
        return node_id

    except Exception as e:
        print(f"Failed to add node {node['DisplayName']}: {e}")
        return None


def discover_and_add_interfaces(node_id):
    try:
        print(f"Discovering interfaces for NodeID {node_id}...")
        result = swis.invoke(
            "Orion.NPM.InterfacesDiscovery", "DiscoverInterfacesOnNode", node_id
        )
        interfaces = result["DiscoveredInterfaces"]
        print(f"→ Found {len(interfaces)} interfaces")

        if interfaces:
            iface_ids = [iface["InterfaceID"] for iface in interfaces]
            swis.invoke(
                "Orion.NPM.InterfacesDiscovery",
                "AddInterfacesOnNode",
                node_id,
                iface_ids,
            )
            print(f"Interfaces added to NodeID {node_id}")
        else:
            print("No interfaces discovered")

    except Exception as e:
        print(f"Interface discovery failed: {e}")


def import_nodes():
    try:
        with open(JSON_FILE, "r") as f:
            nodes = json.load(f)

        print(f"Importing {len(nodes)} nodes from JSON...")
        for node in nodes:
            node_id = add_node(node)
            if node_id:
                time.sleep(2) 
                discover_and_add_interfaces(node_id)

    except Exception as e:
        print(f"Failed to load JSON file: {e}")


if __name__ == "__main__":
    import_nodes()
