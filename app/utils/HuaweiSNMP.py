import subprocess

def snmp_get(oid, ip, community):
    try:
        # Construct the snmpget command
        command = ['snmpwalk', '-v2c', '-c', community, ip, oid]

        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(command)
        # Print the output
        print(result.stdout.strip())

    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.strip()}")

if __name__ == "__main__":
    # Define the OID, IP address of the device, and SNMP community string
    oid = '.1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3'  # Example OID for sysDescr
    ip = '100.126.255.16'          # Replace with the target device's IP address
    community = 'l0nvh%MaMYXq'        # Replace with the appropriate community string

    # Call the SNMP GET function
    snmp_get(oid, ip, community)