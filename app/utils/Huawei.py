import telnetlib
import time
import re
from .. import models,schemas
from sqlalchemy.orm import Session

# Start a new Telnet session
def TelnetSession(device):
    try:
        print(device.ip)
        host = device.ip
        username = device.username
        password = device.password
        port = 23
        print(username,password)
        tn = telnetlib.Telnet(host, port,timeout=60)
        tn.read_until(b">>User name:", timeout=5).decode('ascii').strip()
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b">>User password:", timeout=5)
        tn.write(password.encode('ascii') + b"\n")
        # time.sleep(1)
        output = tn.read_until(b">>", timeout=5).decode('ascii').strip()
        print(output)
        if "Username or password invalid." in output:
            raise ValueError("Invalid Username or password")
        
        pattern = r'\bReenter times have reached the upper limit\.'
        if re.search(pattern, output):
            raise Exception("User already logged in")
        else:
            tn.write(b"enable\n")
            tn.write(b"config\n")
            return tn
    except Exception as e:
        print(f"Failed to connect to {host}: {str(e)}")
        return None

# Run the command "display ont autofind all" , parse the output and return the devices
def autofind(tn):
    try:
        tn.write(b"display ont autofind all\n");
        output = ""
        while True:
          # Read the output from the command until the pagination prompt or timeout
            chunk = tn.read_until(b"---- More ( Press 'Q' to break ) ----", timeout=10).decode('ascii')
            output += chunk  # Append the chunk of output to the complete output
            if "---- More ( Press 'Q' to break ) ----" in chunk:
                # If the pagination prompt is found, send newlines to get more output
                tn.write(b"\n")
            else:
                # Break the loop if the pagination prompt
                break
        print(output)
        if "Failure: The automatically found ONTs do not exist" in output:
            raise Exception("Failure: The automatically found ONTs do not exist")
        # After capturing all outout, remove an trailing pagintaion prompt
        output = output.replace("---- More ( Press 'Q' to break ) ----", "")
        # Split the output into blocks based on the known separator
        blocks = output.split("----------------------------------------------------------------------------")
        # List to store dictionaries of Ont SN and F/S/P
        ont_list = []
        # Iterate over each block to extract F/S/P and Ont SN
        for block in blocks:
            if "Number" in block and "F/S/P" in block and "Ont SN" in block:
                lines = block.strip().split("\n")  # Split block into lines
                number = lines[0].split(":")[1].strip().split()[0]  # Get the line containing number information
                fsp_line = lines[1].strip()  # Get the line containing F/S/P information
                ont_sn_line = lines[2].strip()  # Get the line containing Ont SN information
                # Get the line containing Vendor ID information
                VendorID = lines[6].split(":")[1].strip().split()[0]  # Get the line containing Vendor ID information
                Model = lines[9].split(":")[1].strip().split()[0]  # Get the line containing Model information
                # Extract F/S/P value
                fsp = fsp_line.split(":")[1].strip()
                fs,p = fsp.rsplit("/",1)
                print(Model)
                # Extract Ont SN value
                ont_sn = ont_sn_line.split(":")[1].strip().split()[0]  # Get the first part before the parenthesis
                
                # Append the extracted information as a dictionary to the ont_list
                ont_list.append({"SN": ont_sn, "FSP": fsp, "interface": fs, "port": p, "VendorID": VendorID,"Number": number, "Model": Model})
        
        # Determine the status based on whether any ONTs were found
        status = "success" if ont_list else "failed"
        # Return the status and the list of ONTs found
        return {
            "status": status,
            "devices": ont_list
        }
    except Exception as e:
        print(f"Error while capturing ONT information: {str(e)}")
        print("Fucked")
        return {
            "status": "failed",
            "devices": []
        }

def resetONU(tn,data):
    try:
        inte,port = data['FSP'].rsplit("/",1)
        tn.write(b"interface gpon " + inte.encode('ascii') + b"\n")
        tn.write(b"ont reset " + port.encode('ascii') + b" " + data['ONTID'].encode('ascii') + b"\n")
        tn.write(b"y\n")
        output = tn.read_until(b">>", timeout=5).decode('ascii').strip()
        print(output)
        if "Failure: The ONT is not online" in output:
            raise Exception("ONT is offline")
        return {
            'status' : "success",
            'message' : "ONT Reset Successfully"
        }
    except Exception as e:
        print(f"Error while capturing ONT information: {str(e)}")
        return {
            "status": "failed",
            "message" : str(e)
        }
def getOpticalInfo(tn,data):
    try:
        inte,port = data['FSP'].rsplit("/",1)
        tn.write(b"interface gpon " + inte.encode('ascii') + b"\n")
        tn.write(b"display ont optical-info " + port.encode('ascii') + b" " + data['ONTID'].encode('ascii') + b"\n")
        output = ""
        while True:
            # Read the output from the command
            chunk = tn.read_until(b"---- More ( Press 'Q' to break ) ----", timeout=10).decode('ascii')
            output += chunk
            if "---- More ( Press 'Q' to break ) ----" in chunk:
            # If the pagination prompt is found, send newlines to get more output
                tn.write(b"\n")
            else:
                    # Break the loop if no pagination prompt is found
                break
        print(output)
        if "Failure: The ONT is not online" in output:
            raise Exception("ONT is offline")
        ONU_RX = None
        OLT_RX = None
        rx_power_match = re.search(r"Rx optical power\(dBm\)\s+: (-?\d+\.\d+)", output)
        olt_rx_power_match = re.search(r"OLT Rx ONT optical power\(dBm\)\s+: (-?\d+\.\d+)", output)

        if rx_power_match:
            ONU_RX = float(rx_power_match.group(1))
        if olt_rx_power_match:
            OLT_RX = float(olt_rx_power_match.group(1))
           
        # Regular expressions for the required fields
        # Regular expressions for extracting required fields
        # Regular expressions for extracting required fields
       

        return {
            'status' : "success",
            'ONU_RX' : ONU_RX,
            'OLT_RX' : OLT_RX
        }
    except Exception as e:
        print(f"Error while capturing ONT information: {str(e)}")
        return {
            "status": "failed",
            "device": [],
            "message" : str(e)
        }

def SearchBySN(sn,tn):
    try:
        tn.write(b"display ont info by-sn "+sn.encode('ascii')+b"\n")
        output = ""
        while True:
            # Read the output from the command
            chunk = tn.read_until(b"---- More ( Press 'Q' to break ) ----", timeout=10).decode('ascii')
            output += chunk
            if "---- More ( Press 'Q' to break ) ----" in chunk and "FEC upstream switch" not in chunk:
            # If the pagination prompt is found, send newlines to get more output
                tn.write(b"\n")
            else:
                    # Break the loop if no pagination prompt is found
                
                break
        print(output)
        if "Parameter error" in output:
            raise Exception("Invalid SN")
        if "The required ONT does not exist" in output:
            raise Exception("No OLT Found")
        # Regular expressions for the required fields
        # Regular expressions for extracting required fields
        # Regular expressions for extracting required fields
        patterns = {
            "status": r"Run state\s+:\s+(\w+)",
            "F/S/P": r"F/S/P\s+:\s+(\d+/\d+/\d+)",
            "ONT-ID": r"ONT-ID\s+:\s+(\d+)",
            "SN": r"SN\s+:\s+([\w\d]+) \(([\w\d-]+)\)",
            "Description": r"Description\s+:\s+([^\r\n]+)",
            "Line Profile": r"Line profile name\s+:\s+([^\r\n]+)"
        }
        
        # Extract values using regex
        extracted_data = {key: re.search(pattern, output) for key, pattern in patterns.items()}
        
        # Clean up and format extracted data
        final_data = {
            "status": extracted_data["status"].group(1) if extracted_data["status"] else "Not Found",
            "FSP": extracted_data["F/S/P"].group(1) if extracted_data["F/S/P"] else "Not Found",
            "ONTID": extracted_data["ONT-ID"].group(1) if extracted_data["ONT-ID"] else "Not Found",
            "SN": extracted_data["SN"].group(1) if extracted_data["SN"] else "Not Found",
            "VendorSN": extracted_data["SN"].group(2) if extracted_data["SN"] else "Not Found",
            "Description": extracted_data["Description"].group(1).strip() if extracted_data["Description"] else "Not Found",
            "LineProfile": extracted_data["Line Profile"].group(1).strip() if extracted_data["Line Profile"] else "Not Found"
        }
        return {
            'status' : "success",
            'device' : final_data
        }
    except Exception as e:
        print(f"Error while capturing ONT information: {str(e)}")
        return {
            "status": "failed",
            "device": []
        }

def deleteONU(tn,data):
   try:
        inte,port = data['FSP'].rsplit("/",1)
        removeServiceProfileCMD = 'undo service-port port ' + data['FSP'] +" ont " + data['ONTID'] + " \n\n"
        tn.write(b"\n\n")
        tn.write(removeServiceProfileCMD.encode('ascii'))
        tn.write(b"y\n")
        interfaceCMD = "interface gpon " + inte + "\n"
        deleteCMD = "ont delete " + port + " " + data['ONTID'] + "\n"
        print(interfaceCMD)
        print(deleteCMD)
        # time.sleep(1)
        tn.write(interfaceCMD.encode('ascii'))
        # time.sleep(1)
        tn.write(deleteCMD.encode('ascii'))
        tn.write(b"quit\n\n")
        output = tn.read_until(b">>", timeout=5).decode('ascii').strip()
        print(output)
        if "Failure: The ONT does not exist" in output:
            raise Exception("ONU Doesnot Exists")
        if "Failure: This configured object has some service virtual ports" in output:
           raise Exception("Virtual Port Not deleted")
        if " Number of ONTs that can be deleted: 1, success: 1" in output:
            return {
            "status" : "success"
            }
   except Exception as e:
        print(f"Error while capturing ONT information: {str(e)}")
        return {
            "status": "failed",
            "error" : str(e)
        }
   
def AddONU(tn,data):
    try:
        interfaceCMD = "interface gpon " + data['interface'] + "\n"
        AddCMD = "ont add " + data['port'] +  " sn-auth " + data ['sn'] + " omci ont-lineprofile-id " + data['lineProfileId'] +" ont-srvprofile-id "+ data['serviceProfileId'] + " desc " + data['description'] +"\n\n\n"
        
        tn.write(interfaceCMD.encode('ascii'))
        tn.write(AddCMD.encode('ascii'))
        tn.write(b"/n")
        time.sleep(1)
        tn.write(b"/n/n")
        output = tn.read_until(b">>", timeout=5).decode('ascii').strip()
        print(output)
        if "Failure: SN already exists" in output:
            raise Exception("SN not added, SN already Exists")
        if "Failure: System is busy, please retry after a while" in output:
            time.sleep(10)
            tn.write(b"\n")
            tn.write(AddCMD.encode('ascii'))
            tn.write(b"/n")
        match = re.search(r"ONTID\s*:(\d+)", output)
        match1 = re.search(r"ONTID\s*:\s*(\d+)", output)
        if match:
            ontid = match.group(1)
        if match1:
            ontid = match1.group(1)
        print("ontid: ", ontid)
        if data['nativevlan'] == True:
            # Add native VLAN
            NativeVLANCommand = "ont port native-vlan " + data['port'] + " " + ontid + " " + " eth 1 vlan " + data['vlan'] + " priority 0\n\n"
            tn.write(b"\n")
            tn.write(NativeVLANCommand.encode('ascii'))
            tn.write(b'\n')
        AddServicePortCMD = "service-port vlan " + data['vlan'] + " gpon " + data['FSP'] + " ont " + ontid + " gemport " + data['gemport'] + " multi-service user-vlan " + data['vlan'] + " tag-transform translate\n\n\n"
        quitCMD = "quit \n"
        tn.write(b"\n")
        tn.write(quitCMD.encode('ascii'))
        tn.write(AddServicePortCMD.encode('ascii'))
        tn.write(b'\n')
        if data['acs'] == True:
            ACSCommand = "service-port vlan " + data['acs_vlan'] + " gpon " + data['FSP'] + " ont " + ontid + " gemport " + data['acs_gemport'] + " multi-service user-vlan " + data['acs_vlan'] + " tag-transform translate\n\n\n"
            quitCMD = "quit \n"
            tn.write(b"\n")
            tn.write(ACSCommand.encode('ascii'))
            tn.write(b'\n')
        output = tn.read_until(b">>", timeout=5).decode('ascii').strip()
        print(output)
        data = {
            "SN" : data['sn'],
            "Description" : data['description'],
            "FSP" : data['FSP'],
            "ONTID" : ontid,
            "vlan" : data['vlan']
        }
        return {
            "status" : "success",
            "data" : data
        }
    except Exception as e:
        return {
            "status": "failed",
            "error" : str(e)
        }
    
def searchByDesc(desc,tn):
    try:
        command = "display ont info by-desc " + desc
        tn.write(command.encode('ascii') + b'\n')
        output = tn.read_until(b">>", timeout=5).decode('ascii').strip()
        # print(output)
        while True:
            # Read the output from the command
            chunk = tn.read_until(b"---- More ( Press 'Q' to break ) ----", timeout=30).decode('ascii')
            output += chunk
            if "---- More ( Press 'Q' to break ) ----" in chunk:
                # If the pagination prompt is found, send newlines to get more output
                tn.write(b"\n")
            else:
                # Break the loop if no pagination prompt is found
                break
        print(output)
        pattern = r'\b\d+/\s*\d+/\d+\s+\d+\s+\w+\s+\w+\s+\w+\s+\w+\s+\w+\b'
        pattern1 = r'\b\d+/\s*\d+/\s*\d+\b\s+\d+\s+(\b\w+\b)'
        fsps_set = re.findall(pattern, output)
        uset_set_unfiltered = re.findall(pattern1, output)
        fsps_set = re.findall(pattern, output)
        users = []
        uset_set_unfiltered = re.findall(pattern1, output)
        for user_filter in uset_set_unfiltered:
            if "_" in user_filter:
                users.append(user_filter)
        count = 0
        infos = []
        for fsp_details in fsps_set:
            fsp_details_list = fsp_details.split("  ")
            fsp = fsp_details_list[0].replace(" ","")
            ont = fsp_details_list[1]
            sn = fsp_details_list[2]
            status = fsp_details_list[6]
            if ont == "":
                ont = fsp_details_list[2]
                sn = fsp_details_list[3]
                status = fsp_details_list[7]
            desc_output = users[count]
            fsp_split = fsp.split("/")
            fs = fsp_split[0] +"/"+fsp_split[1]
            p = fsp_split[2]
            fsp_sep = fsp_split[0] +" "+fsp_split[1] +" "+fsp_split[2]
            customerInfo = {
                "FSP": fsp,
                "Description": desc_output,
                "ONTID": ont,
                "SN": sn,
                'P': p,
                "Interface" : fs,
                'state' : status
                }
            infos.append(customerInfo)
            print(customerInfo)
            count = count + 1
        # print(infos)
        # print("-"*50)
        return {
            "status" : "success",
            "device" : infos
        }
    except Exception as e:
        print(e)
        # writeLog("Error:\n")
        # writeLog(output)
        return {
            "status" : "failed"
        }
