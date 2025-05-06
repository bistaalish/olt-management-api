import requests

def sendMessage(webhook_url, data_dict):
    """
    Send a nicely boxed and formatted message to a Discord channel using a webhook URL.
    """
    headers = {
        "Content-Type": "application/json"
    }

    # Format the message inside a code block with separators
    separator = "━━━━━━━━━━━━━━━━━━━━━━"
    message_lines = [f"{key}: {value}" for key, value in data_dict.items()]
    boxed_message = f"```ini\n{separator}\n" + "\n".join(message_lines) + f"\n{separator}\n```"

    payload = {
        "content": boxed_message
    }

    response = requests.post(webhook_url, headers=headers, json=payload)
    if response.status_code == 204:
        print("✅ Message sent successfully!")
        return True
    else:
        print(f"❌ Failed to send message. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return False

# Example data
# data = {
#     "SN": "xxxxxxxxxxxxxxxx",
#     "Username": "xxx_xxxxx_xxxx",
#     "FSP": "x/x/x",
#     "ONTID": 13
# }

# discordWebhook = "https://discord.com/api/webhooks/1369183539513524354/XUh5XPWgeVyr1WYTH47OQ4YA73kaCbrsp9iuziZSl4c4XZYMyo4aFX4-5fOOpWjmmtBP"
# sendMessage(discordWebhook, data)
