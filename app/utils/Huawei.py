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
        tn = telnetlib.Telnet(host, port,timeout=60)
        tn.read_until(b">>User name:", timeout=5).decode('ascii').strip()
        tn.write(username.encode('ascii') + b"\n")
        tn.read_until(b">>User password:", timeout=5)
        tn.write(password.encode('ascii') + b"\n")
        # time.sleep(1)
        output = tn.read_until(b">>", timeout=5).decode('ascii').strip()
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
                fsp_line = lines[1].strip()  # Get the line containing F/S/P information
                ont_sn_line = lines[2].strip()  # Get the line containing Ont SN information
                
                # Extract F/S/P value
                fsp = fsp_line.split(":")[1].strip()
                fs,p = fsp.rsplit("/",1)
                
                # Extract Ont SN value
                ont_sn = ont_sn_line.split(":")[1].strip().split()[0]  # Get the first part before the parenthesis
                
                # Append the extracted information as a dictionary to the ont_list
                ont_list.append({"SN": ont_sn, "FSP": fsp, "interface": fs, "port": p})
        
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


def SearchBySN(sn,tn):
    try:
        tn.write(b"display ont info by-sn "+sn.encode('ascii')+b"\n")
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
        if "Parameter error" in output:
            raise Exception("Invalid SN")

        if "The required ONT does not exist" in output:
            raise Exception("No OLT Found")
        # Regular expressions for the required fields
        # Regular expressions for extracting required fields
        # Regular expressions for extracting required fields
        patterns = {
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
            "FSP": extracted_data["F/S/P"].group(1) if extracted_data["F/S/P"] else "Not Found",
            "ONTID": extracted_data["ONT-ID"].group(1) if extracted_data["ONT-ID"] else "Not Found",
            "sn": extracted_data["SN"].group(1) if extracted_data["SN"] else "Not Found",
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
        tn.write(removeServiceProfileCMD.encode('ascii'))
        tn.write(b"y\n")
        interfaceCMD = "interface gpon " + inte + "\n"
        deleteCMD = "ont delete " + port + " " + data['ONTID'] + "\n"
        print(interfaceCMD)
        print(deleteCMD)
        time.sleep(1)
        tn.write(interfaceCMD.encode('ascii'))
        time.sleep(1)
        tn.write(deleteCMD.encode('ascii'))
        tn.write(b"quit\n")
        time.sleep(1)
        output = tn.read_until(b"config)#").decode()
        print(output)
        if "Failure: This configured object has some service virtual ports" in output:
           raise Exception("Virtual Port Not deleted")
        return {
           "status" : "success"
        }
   except Exception as e:
        print(f"Error while capturing ONT information: {str(e)}")
        return {
            "status": "failed",
            "error" : str(e)
        }