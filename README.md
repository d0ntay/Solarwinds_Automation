# SolarWinds Orion Automation

Utilities for bulk device management in SolarWinds Network Performance Monitor (NPM) using the Orion REST API.

## What It Does

Automates device discovery, monitoring setup, and inventory management in SolarWinds Orion. Use cases include bulk node imports, interface discovery, and inventory export.

## Tools Included

### 1. **node_adder.py** — Bulk Node Import & Discovery
Reads device list from JSON and imports into Orion with SNMPv3 configuration.

**Features:**
- Bulk import of nodes from JSON export
- Automatic interface discovery
- SNMPv3 credential handling
- Error logging for failed imports

**Setup:**
1. Export device list as JSON (sample format required):
   ```json
   [
     {
       "DisplayName": "router1",
       "IPAddress": "192.168.1.1",
       "SNMPv3": {
         "Username": "snmp_user",
         "AuthMethod": "MD5",
         "AuthKey": "auth_key_here",
         "PrivMethod": "DES",
         "PrivKey": "priv_key_here"
       }
     }
   ]
   ```

2. Update credentials in script:
   ```python
   TARGET_SW_HOST = "orion.example.com"
   USERNAME = "orion_admin"
   JSON_FILE = "nodes_export_with_snmpv3.json"
   ```

3. Run:
   ```bash
   python node_adder.py
   ```

**What It Does:**
- Creates Orion nodes with SNMPv3 settings
- Discovers and adds interfaces for each node
- Logs progress and errors

### 2. **node_exporter.py** — Inventory Export
Exports current Orion node inventory to JSON for backup or migration.

### 3. **Node_getter_sw.py** — Node Lookup
Queries Orion API for device information.

## Requirements

```
orionsdk>=0.3.0
requests>=2.20.0
urllib3>=1.24.0
```

Install:
```bash
pip install orionsdk
```

## Configuration

Update connection details in each script:
```python
TARGET_SW_HOST = "orion.example.com"  # Orion server hostname/IP
USERNAME = "domain\\admin"              # Windows domain format for domain accounts
PASSWORD = getpass.getpass()            # Prompted at runtime
```

## Key Concepts

- **Orion.Nodes:** The entity type for monitoring devices in Orion
- **SNMPv3:** Authentication method used (v2c also supported with modifications)
- **Interface Discovery:** Automatically finds and monitors interfaces after node creation
- **Bulk Operations:** Useful for importing devices from other monitoring platforms

## Notes

- Requires network connectivity to SolarWinds Orion server
- Admin credentials needed for bulk operations
- SNMPv3 credentials must be preconfigured on managed devices
- Includes SSL warning suppression (self-signed certs)
- Modify scripts for SNMPv2c if SNMPv3 unavailable on your devices
