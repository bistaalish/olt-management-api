import requests
import os
from dotenv import load_dotenv
load_dotenv()

APP_NAME = os.getenv("APP_NAME")
def sendMessage(webhook_url: str, data: dict) -> bool:
    """
    Sends a Discord embed message via webhook based on provided data.
    Color codes the embed depending on the 'Operation' type.

    Args:
        webhook_url (str): The Discord webhook URL.
        data (dict): Dictionary containing details like SN, Username, FSP, ONTID, Operation, etc.

    Returns:
        bool: True if message sent successfully, False otherwise.
    """

    # Determine color and emoji based on 'Operation'
    operation = data.get("Operation", "").strip().lower()
    if operation == "add":
        color = 0x2ecc71  # Green
        emoji = "🟢"
    elif operation == "delete":
        color = 0xe74c3c  # Red
        emoji = "🔴"
    else:
        color = 0x3498db  # Blue (Default)
        emoji = "🔵"

    # Build fields for embed
    fields = [
        {"name": key, "value": str(value), "inline": False}
        for key, value in data.items()
    ]

    embed = {
        "title": f"{emoji} {operation.capitalize()} Operation Notification",
        "color": color,
        "fields": fields,
        "footer": {
            "text": f"Powered by {APP_NAME}",
        }
    }

    payload = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code == 204:
            print("✅ Message sent successfully!")
            return True
        else:
            print(f"❌ Failed to send message. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ An error occurred: {e}")
        return False
