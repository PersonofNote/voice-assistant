import sys
from dotenv import load_dotenv, set_key
import os
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

def wyze_client(env_path = '.env'):
    print("Initializing client")
    try: 
        response = Client().login(
        email=os.getenv('WYZE_EMAIL'),
        password=os.getenv('WYZE_PASSWORD'),
        key_id=os.getenv('WYZE_API_KEY_ID'),
        api_key=os.getenv('WYZE_API_KEY')
        )
        set_key(env_path, 'WYZE_API_TOKEN', response['access_token'])
        return Client(response['access_token'])
            
    except:
        # if no token exists, create and save the new token
        print('Creating new token')
        response = Client().login(
            email=os.getenv('WYZE_EMAIL'),
            password=os.getenv('WYZE_PASSWORD'),
            key_id=os.getenv('WYZE_API_KEY_ID'),
            api_key=os.getenv('WYZE_API_KEY')
        )
        set_key(env_path, 'WYZE_API_TOKEN', response['access_token'])
        return Client(response['access_token'])

def wyze_execute_command(device, command, client):
    # TODO: expand this to offer more commands
    # For each of these commands, will need to adjust by the 'type' property to access the corresponding method for bulbs, plugs, etc
    # If each type has the same methods, this will be as easy as using bracket notation and passing the type property
    
    #bulb = client.bulbs.info(device_mac=device.mac) Redundant for now but maybe useful later and easy to forget the exact syntax

    match command:
        case "on": client.bulbs.turn_on(device_mac=device.mac, device_model=device.product.model)
        case "off": client.bulbs.turn_off(device_mac=device.mac, device_model=device.product.model)
            
            

def wyze_list_devices(client, filter = ''):
    # TODO: allow filtering by type if wanted
    device_list = []
    print(client.devices_list())
    for device in client.devices_list():
        print(f"mac: {device.mac}")
        print(f"nickname: {device.nickname}")
        print(f"is_online: {device.is_online}")
        print(f"product model: {device.product.model}")
        device_list.append(device.nickname)
    return device_list

def wyze_get_mac_from_nickname(nickname, client):
    for device in client.devices_list():
        if device.nickname.lower().strip() == nickname.lower().strip():
            return device
    return None

