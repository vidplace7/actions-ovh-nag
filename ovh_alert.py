#!/usr/bin/env python3

import requests
import os


ovh_baseurl = "https://us.ovhcloud.com/engine/api/v1/vps/order/rule/datacenter/?ovhSubsidiary=US&os="
discord_webhook = os.environ.get('DISCORD_WEBHOOK')

def get_stock(url, dc_code):
    print(f"DEBUG: {url}")
    r = requests.get(url)
    d = r.json()
    dcs = d['datacenters']
    for dc in dcs:
        if dc_code in dc['code']:
            print(dc)
            if dc['status'] == 'available':
                return True
            else:
                return False

def post_discord(hook_url, plan_code, dc_code):
    data = {
        "content": f"<@161932349959831552> OVH VPS **{plan_code}** is now in stock at **{dc_code}**!\nhttps://us.ovhcloud.com/vps/configurator/",
        "flags": 4
    }
    r = requests.post(hook_url, json=data)
    if r.status_code == 204:
        print("Discord notification sent successfully.")
    else:
        print(f"Failed to send Discord notification. Status code: {r.status_code}")

if __name__ == "__main__":
    in_stock = get_stock(f"{ovh_baseurl}&planCode=vps-2025-model1.LZ", "us-east-lz-atl")
    print(f"In stock: {in_stock}")
    if in_stock:
        post_discord(discord_webhook, "vps-2025-model1.LZ", "us-east-lz-atl")
