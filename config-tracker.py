import concurrent
from datetime import datetime
from library.nxapi import nxapi_cli
from library.encrypt import decrypt_message
from library.gitlab_api import get_config, post_config, create_config
from library.extract import extract
from library.netbox_api import get_data
from library.napalm_ssh import napalm_ssh

def config_check(device_cfg,node):
    '''
    Function that performs config diff checking.
    - Updates the NetBox device status to offline if no config was pulled
    - Updates the NetBox device custom field data for 'Last Config Change' if diff is found
    - Commits the new configuration to gitlab if diff is found
    '''
    poll_timestamp=datetime.now().strftime("%Y-%h-%d %H%MH")
    if device_cfg:
        print(f'[INFO] {node.name} polling successfull on {poll_timestamp}.')
        gitlab_cfg = get_config(node.name)
        if gitlab_cfg:
            if gitlab_cfg != device_cfg:
                post_config(node.name,device_cfg)
                node.custom_fields['Last Config Change'] = timestamp
                node.save()
                print(f'[INFO] {node.name} netbox status updated.')
        else:
            create_config(node.name,device_cfg)
            node.custom_fields['Last Config Change'] = timestamp
            node.save()
    else:
        print(f'[WARNING] {node.name} polling failed on {poll_timestamp}.')
        if node.status == 'active':
            node.status = 'offline'
            node.save()

def config_pull_nxapi(node):
    '''
    Function that calls nxapi_cli function to fetch the latest configuration and passes this data to config_check function
    '''
    device_cfg = nxapi_cli(
        str(node.primary_ip4).split('/')[0],
        'show run | exc !Time',
        'cli_show_ascii',
        netdev_user,
        netdev_pass)
    config_check(device_cfg,node)

def config_pull_napalm(driver,command,node):
    '''
    Function that calls napalm_ssh function to fetch the latest configuration and passes this data to config_check function
    '''
    device_cfg = napalm_ssh(
        driver,
        str(node.primary_ip4).split('/')[0],
        [command],
        netdev_user,
        netdev_pass)
    config_check(device_cfg,node)

if __name__ == '__main__':
    timestamp = datetime.now().strftime("%Y-%m-%d")

    #Extract login credentials
    netdev_user = decrypt_message(extract('private/credentials.txt').split(',')[0].encode())
    netdev_pass = decrypt_message(extract('private/credentials.txt').split(',')[1].encode())

    #Fetch devices details from NetBox via API request
    devices = get_data()
    devices = [ i for i in devices if str(i.tags) == '[dev-simulation]' ]

    nxos_devices = []
    ios_devices = []
    iosxr_devices = []
    junos_devices = []

    #Iterates the list of devices and grouped based on platform
    for i in devices:
        if type(i.primary_ip) != type(None) and str(i.status) == 'Active':
            if str(i.platform) == 'Cisco NXOS':
                nxos_devices.append(i)
            elif str(i.platform) == 'Cisco IOS':
                ios_devices.append(i)
            elif str(i.platform) == 'Cisco IOS-XR':
                iosxr_devices.append(i)
            elif str(i.platform) == 'Juniper JunOS':
                junos_devices.append(i)
    
    #Performs multithreading operation to execute different functions and  platform groups at the same time
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    futures_nxos = [executor.submit(
        config_pull_nxapi,
        node) for node in nxos_devices]
    futures_ios = [executor.submit(
        config_pull_napalm,
        'ios',
        'show run  | exc clock-period',
        node) for node in ios_devices]
    futures_iosxr = [executor.submit(
        config_pull_napalm,
        'iosxr',
        'show run',
        node) for node in iosxr_devices]
    futures_junos = [executor.submit(
        config_pull_napalm,
        'junos',
        'show configuration | display set',
        node) for node in junos_devices]
    futures = futures_nxos + futures_ios + futures_iosxr + futures_junos
    concurrent.futures.wait(futures)
