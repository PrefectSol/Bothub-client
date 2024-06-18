import argparse
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hub.network_interface import NetworkInterface


def delete_host(opt) -> int:
    print(f'Optional arguments: {opt}')
    
    try:
        with open(opt.cconfig, 'r') as file:
            client_config = json.load(file)
            user_id = client_config['auth']['user_id']
            user_secret = client_config['auth']['user_secret']
            NetworkInterface.server_url = f"http://{client_config['host']}:{client_config['port']}"
            
        with open(opt.hconfig, 'r') as file:
            host_config = json.load(file)
            host_id = host_config['host_id']
    except Exception as exc:
        print(f'Error loading configurations: {exc}')
        return 1
    
    handler = NetworkInterface(user_id, user_secret)
    try:
        result = handler.delete_host(host_id)
    except Exception as exc:
        print(f'Failed to delete host: {exc}')
        return 1

    result = result['answer']
    
    if 'error' in result:
        print('Host delete error:', result['error'])
        return 1
        
    print('The host game has been successfully deleted.')
    print(result)
    
    return 0


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cconfig", type=str, default="client-config.json", help="path to client-config.json")
    parser.add_argument("--hconfig", type=str, default="host-config.json", help="path to host-config.json")

    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    exit(delete_host(opt))
