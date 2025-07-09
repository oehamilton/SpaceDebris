import requests

url = "https://sms.api.sinch.com/xms/v1/d55362c23fe94a76a79a4409e249c85a/batches"
headers = {
    "Authorization": "Bearer 6081f3c378b745e69b507e4c1eabdc4d",
    "Content-Type": "application/json"
}
data = {
    "from": "12085797066",
    "to": ["19402063925"],
    "body": "Water Pump Failure - TCCD NE Campus"
}

response = requests.post(url, headers=headers, json=data)