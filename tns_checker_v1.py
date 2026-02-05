import time
import os
import random
import requests
import json
import datetime
print('Terra Network Sync Checker v1.0')
print('Created By: Anthony R Shively, Ohio USA')
print('')
def loads(file_name, i=None):
    io = {}
    if i != None:
        if os.path.exists(file_name) == False:
            dumps(file_name, io)
    try:
        if os.path.exists(file_name) == True:
            while True:
                try:
                    with open(file_name, "r") as file:
                        io = json.load(file)
                        break
                except IOError:
                    print("File Waiting:", file_name)
                    time.sleep(1)
    except Exception as e:
        print("Issues with:", file_name, e)
    return (io)
def dumps(file_name, data, i=None):
    if i != None:
        if i == 'Clean':
            if os.path.exists(file_name) == True:
                os.remove(file_name)
        else:
            file_name = os.path.join(i, file_name)
    try:
        if len(data) == 0:
            print('File is empty!:', file_name)
    except:
        pass
    with open(file_name, "w") as config:
        json.dump(data, config, indent=4)
def curl_to_python(url, headers=None, data=None):
    if headers == None:
        headers = {"Content-Type": "application/json"}
    time.sleep(.25)
    # Get and Post are Different Here!!
    if data == None:
        time.sleep(.25)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print('Bad Url:',  url)
        return (response.json())
    else:
        time.sleep(.25)
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            print('Bad Url:',  url)
        return(response.json())
def terra_rpc_publicnode():
    try:
        io = loads('snapshot_hash.json')
        url_list = ['https://terra-rpc.publicnode.com/status', 'https://terra-classic-rpc.publicnode.com/status']
        for line in url_list:
            try:
                ion = {}
                dns_name = (((line).replace('https://', '')).replace('/status', ''))
                data = curl_to_python(line)
                data = data.get('result')
                network = data.get('node_info').get('network')
                sync_info = data.get('sync_info')
                ion['name'] = (line)
                ion['network'] = (network)
                ion['version'] = (data.get('node_info').get('version'))
                ion['latest_block_hash'] = (sync_info.get('latest_block_hash'))
                ion['latest_block_height'] = (sync_info.get('latest_block_height'))
                ion['latest_block_time'] = (sync_info.get('latest_block_time'))
                ion['earliest_block_hash'] = (sync_info.get('earliest_block_hash'))
                ion['earliest_block_height'] = (sync_info.get('earliest_block_height'))
                ion['earliest_block_time'] = (sync_info.get('earliest_block_time'))
                io[str(time.time())] = (ion)
                time.sleep(1)
            except Exception as e:
                print('Issues with:', line)
                print('Connection Issues:', e)
        iot = list(io.keys())
        iot.sort(reverse=True)
        iou = {}
        for line in iot:
            iou[line] = (io.get(line))
        dumps('snapshot_hash.json', iou)
    except Exception as e:
        print('Terra RPC Public Node Issues:', e)
def main():
    terra_rpc_publicnode()
    done = ['Finished', 'Completed', 'Done', 'Successful']
    print(random.choice(done))
    time.sleep(240)
while True:
    main()