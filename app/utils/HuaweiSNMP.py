from puresnmp import Client, V2C, PyWrapper
import asyncio


# # OID you want to GET or SET
# oid = "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4.4194312448.0"  # sysName
async def ExecuteSNMP(host,community,oid):
   client = PyWrapper(Client(host, V2C(community)))
   output = await client.get(oid)
   output = output / 100
   return output



def encode_fsp(frame: int, slot: int, port: int) -> int:
    """
    Encode Huawei OLT Frame/Slot/Port (F/S/P) to SNMP ifIndex.
    Frame is ignored in single-chassis OLTs.
    """
    inital_value = 4194312192
    encodedFSP = inital_value + ((slot-1) * 8192) + (port * 256)
    return encodedFSP

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
    return {
        "status" : "success",
        'ONU_RX' : str(OpticalPowerRx)
    }

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

