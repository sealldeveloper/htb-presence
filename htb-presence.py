#!/usr/bin/env python3

## htb-presence.py - RichPresence for HackTheBox on Discord
## Author: @Pirrandi (https://github.com/Pirrandi)
## Translator: @wh0crypt (https://github.com/wh0crypt)
## Additional Contributions: @sealldev (https://github.com/sealldeveloper)

from pypresence import Presence
import psutil
import requests
import time
import os
import sys
import atexit
import traceback
from dotenv import load_dotenv
from tempfile import gettempdir
from pathlib import Path
from platform import system

from utils.functions import *

# Load environment variables
load_dotenv()

# Load appropriate language
lang = os.getenv('LANGUAGE') if os.getenv('LANGUAGE') else 'EN' # default is english
if lang == 'EN':
    from translations.en import *
elif lang == 'ES':
    from translations.es import *


lock_file = os.path.join(Path("/tmp" if system() == "Darwin" else gettempdir()),'test.py.lock')

if __name__ == "__main__":
    atexit.register(release_lock,lock_file)
    acquire_lock(lock_file)

# HackTheBox and Discord APIs configuration
client_id = os.getenv('CLIENT_ID') if os.getenv('CLIENT_ID') else '1125543074861432864' # default is '1125543074861432864' 
htb_api_token = os.getenv('HTB_API_TOKEN') if os.getenv('HTB_API_TOKEN') else None

# RPC Customisation
rpc_large_text = os.getenv('RPC_LARGE_TEXT') if os.getenv('RPC_LARGE_TEXT') else "Hack The Box"
rpc_large_img = os.getenv('RPC_LARGE_IMG') if os.getenv('RPC_LARGE_IMG') else None
rpc_small_text = os.getenv('RPC_SMALL_TEXT') if os.getenv('RPC_SMALL_TEXT') else None
rpc_small_img = os.getenv('RPC_SMALL_IMG') if os.getenv('RPC_SMALL_IMG') else None
rpc_state = os.getenv('RPC_STATE') if os.getenv('RPC_STATE') else "User: <USER> | Root: <ROOT>"

if not htb_api_token or htb_api_token == 'HTB_TOKEN_HERE':
    print(htb_api_token_not_set)
    sys.exit()

RPC_status=0
RPC = Presence(str(client_id))
connection=0

test=1
while test==1:
    def is_discord_open():
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if 'discord' in process.info['name'].lower():
                return 1
        return 0
    discord_status= is_discord_open()
    print(discord_status)
    if is_discord_open():
        print(discord_running_str)
    else:
        print(discord_not_running_str)

    while is_discord_open():
        # HackTheBox API configuration
        htb_machine_api = 'https://www.hackthebox.com/api/v4/machine/active'
        htb_user_api = 'https://www.hackthebox.com/api/v4/user/info'
        htb_connection_api = 'https://www.hackthebox.com/api/v4/user/connection/status'

        headers = {
            'User-Agent': 'HTB Discord Rich Presence',
            'Authorization': f'Bearer {htb_api_token}'
        }

        # Media
        htb_logo = 'https://yt3.googleusercontent.com/ytc/AOPolaR5R7bueWAUHc7ctRNCy5r63xddkeL17RDHOwxAlw=s900-c-k-c0x00ffffff-no-rj'
        buttons = [
            {
                'label': label1_str,
                'url': url1_str
            },
            {
                'label': label2_str,
                'url': url2_str
            }
        ]
        def closeDiscord_clearRPC_status():
            global RPC_status
            if discord_status==0:
                RPC_status=0
                
        # Variable that stores the Active Machine's name
        active_machine_name = None
        # Loop for continuous state update and verification
        start_time=1
        while is_discord_open:
            # try:
            is_discord_open()
            
            time.sleep(1)
            closeDiscord_clearRPC_status()
            # Retrieve the Active Machine's information from HackTheBox
            response_machine = requests.get(htb_machine_api, headers=headers)
            response_user = requests.get(htb_user_api, headers=headers)
            response_connection = requests.get(htb_connection_api, headers=headers)
            if RPC_status == 0:
                print(connecting_rpc_str)

                RPC.connect()
                RPC_status=1
                print(connected_rpc_str)
            
            if response_machine.status_code == 200:
                data_machine = response_machine.json()
                data_user = response_user.json()
                data_connection = response_connection.json()
                
                connection = data_connection['status']
                # print(data_machine,data_user,data_connection)
                if data_machine:
                    user = data_user['info']
                    user_nickname = user['name']
                    user_avatar = user['avatar']
                    user_avatar = f"https://www.hackthebox.com{user['avatar']}"
                    print(user_info_retrieved_str)
                    # print(discord_status)
                    # print(RPC_status)
                    small_text = rpc_small_text if rpc_small_text else user_nickname
                    small_image = rpc_small_img if rpc_small_img else user_avatar
                    if discord_status==1 and connection == True and RPC_status == 1 and active_machine_name == None:
                        large_image = rpc_large_img if rpc_large_img else htb_logo
                        print(updating_rp_str)
                        RPC.update(
                                details=connected_htb_str,
                                state=waiting_state_str,
                                large_image=large_image,
                                large_text=rpc_large_text,
                                small_image=small_image,
                                small_text=small_text,
                                buttons=buttons
                            )                        
                    
                    machine = data_machine['info']
                    machine_name = machine['name']
                    machine_avatar = machine['avatar']
                    machine_avatar = f"https://www.hackthebox.com{machine['avatar']}"
                    large_image = rpc_large_img if rpc_large_img else machine_avatar
                    print(large_image,rpc_large_img,machine_avatar)
                    print(machine_info_retrieved_str)
                    
                    ###
                    htb_get_api = f"https://www.hackthebox.com/api/v4/user/profile/activity/{user['id']}"
                    response_activity = requests.get(htb_get_api, headers=headers)
                    data_activity = response_activity.json()
                    print(apis_connected_str)

                    root_flag = "🔴"
                    user_flag = "🔴"

                    for record in data_activity["profile"]["activity"]:
                        if record["name"] == machine_name:
                            if record["type"] == "root":
                                if record['first_blood'] == True:
                                    root_flag = "🩸"
                                else:
                                    root_flag = "🟢"
                            elif record["type"] == "user":
                                if record['first_blood'] == True:
                                    user_flag = "🩸"
                                else:
                                    user_flag = "🟢"
                    
                    playing_machine = [
                        {
                            'label': play_str,
                            'url': f'https://app.hackthebox.com/machines/{machine_name}'
                        }
                    ]
                    print(machine_found_str)
                    
                    # Check if the machine has changed
                    if machine_name != active_machine_name:
                        active_machine_name = machine_name

                        start_time = int(time.time())
                        
                    # Update RichPresence's state
                    rpc_state = rpc_state.replace('<USER>',user_flag).replace('<ROOT>',root_flag)
                    RPC.update(
                        details=machine_str+machine_name,
                        large_image=large_image, 
                        large_text=rpc_large_text,
                        small_image=small_image,
                        small_text=small_text,
                        state=rpc_state,
                        buttons = playing_machine
                    )
                else:
                    active_machine_name = None
                    print(cleaning_rpc_str)
                    RPC.clear()
            else:
                print(request_error_str+response.status_code)
                
            # except Exception as e:
            #     print(active_machine_warning_str)
            #     active_machine_name = None
            #     def is_discord_open():
            #         for process in psutil.process_iter(attrs=['pid', 'name']):
            #             if 'discord' in process.info['name'].lower():
            #                 return 1
            #         return 0
            #     discord_status= is_discord_open()   
                
            #     if discord_status==1 and connection==False:
            #         print(cleaning_rpc_str)              
            #         RPC.clear()
            #         continue
            #     if discord_status==0:
            #         print(discord_not_running_str)
            #         continue               
release_lock(lock_file)           
