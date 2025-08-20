from puresnmp import Client, V2C, PyWrapper
import asyncio


# # OID you want to GET or SET
# oid = "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4.4194312448.0"  # sysName
#async def ExecuteSNMP(host,community,oid):
#   client = PyWrapper.walk(Client(host, V2C(community)))
#   output = await client(oid)
#   return output

async def ExecuteSNMP(host,community,oid):
   client = PyWrapper(Client(host, V2C(community)))
   output = await client.get(oid)
   return output


async def Walk(host, community, oid):
    client = PyWrapper(Client(host, V2C(community)))
    AutofindData = []
    async for oid_str, value in client.walk(oid):
        # print(f"[{oid_str}:{value.hex().upper()}]")
        SN = value.hex().upper()
        oid_str = oid_str.split(".")
        FSP = decode_fsp(int(oid_str[-2]))
        vendorID = bytes.fromhex(SN[:8])
        vendorSN = f"{vendorID.decode()}-{SN[8:]}"
        AutofindData.append({
            "FSP": FSP,
            "SN": SN,
            "vendorsn": vendorSN,
            "vendorid": vendorID,
        
        })
        print(AutofindData)
    return AutofindData

def encode_fsp(frame: int, slot: int, port: int) -> int:
    """
    Encode Huawei OLT Frame/Slot/Port (F/S/P) to SNMP ifIndex.
    Frame is ignored in single-chassis OLTs.
    """
    inital_value = 4194312192
    encodedFSP = inital_value + ((slot-1) * 8192) + (port * 256)
    return encodedFSP

def decode_fsp(encodedFSP: int) -> tuple:
    """
    Decode SNMP ifIndex back to Huawei OLT Frame/Slot/Port (F/S/P).
    """
    inital_value = 4194312192
    offset = encodedFSP - inital_value
    slot = (offset // 8192) + 1
    port = (offset % 8192) // 256
    FSP = f"0/{slot}/{port}"
    return (FSP)  # Frame is ignored in single-chassis OLTs

def splitFSP(FSP):
    return FSP.split('/')


# oid = "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4." + str(encodedFSP) + "."+str(ont_id)



# print(asyncio.run(ExecuteSNMP(host,community,oid)))

# frame, slot, port = splitFSP("0/1/1")
# print(f"Frame: {frame}, Slot: {slot}, Port: {port}")
def checkOpticalPowerRx(device,FSP,ontid):
    host = device.ip
    community = device.SNMP_RO
    frame, slot, port = splitFSP(FSP)
    generatedFSPCode = encode_fsp(int(frame),int(slot),int(port))
    generatedOID = "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4." + str(generatedFSPCode) + "."+str(ontid)
    print(generatedOID)
    OpticalPowerRx = asyncio.run(ExecuteSNMP(host,community,generatedOID))
    print(OpticalPowerRx)
    output = OpticalPowerRx / 100
    return {
        "status" : "success",
        'ONU_RX' : str(output)
    }

#def checkDeviceStatus(device):
#    host = device.ip
#    community = device.SNMP_RO
#    OID = "1.3.6.1.2.1.1.3.0"
#    try:
#        DeviceStatus = asyncio.run(asyncio.wait_for(ExecuteSNMP(host, community, OID), timeout=2))
#        print(DeviceStatus)
#        if DeviceStatus:
#            return {
#                 "status" : "online"
#            }
#    except asyncio.TimeoutError:
#        print("SNMP request timed out.")
#        return {
#            "status" : "offline"
#        }

def checkDeviceStatus(device):
    host = device.ip
    community = device.SNMP_RO
    OID = "1.3.6.1.2.1.1.3.0"
    try:
        DeviceStatus = asyncio.run(asyncio.wait_for(ExecuteSNMP(host, community, OID), timeout=2))
        if DeviceStatus:
            return {
                 "status" : "online"
            }
    except asyncio.TimeoutError:
        print("SNMP request timed out.")
        return {
            "status" : "offline"
        }





def RunAutofind(device):
    print(device)
    host = device.ip
    community = device.SNMP_RO
    # OID = "1.3.6.1.2.1.1.3.0"
    OID = ".1.3.6.1.4.1.2011.6.128.1.1.2.52.1.2"
    try:
        AutofindData = asyncio.run(asyncio.wait_for(Walk(host, community, OID), timeout=10))
        status = "success" if AutofindData else "failed"
        message = "No data found" if status == "failed" else "Data found"
        print(AutofindData)
        return {
            "status" : status,
            "message" : message,
            "data" : AutofindData
        }
    except asyncio.TimeoutError:
        print("SNMP request timed out.")
        return {
            "status" : "failed",
            "message" : "SNMP request timed out.",
            "data" : []
        }

