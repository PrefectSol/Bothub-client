import argparse
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hub.network_interface import NetworkInterface


def create_host(opt) -> int:
    print(f'Optional arguments: {opt}')
    
    try:
        with open(opt.cconfig, 'r') as file:
            client_config = json.load(file)
            user_id = client_config['auth']['user_id']
            user_secret = client_config['auth']['user_secret']
            NetworkInterface.server_url = f"http://{client_config['host']}:{client_config['port']}"
            
        with open(opt.hconfig, 'r') as file:
            host_config = json.load(file)
    except Exception as exc:
        print(f'Error loading configurations: {exc}')
        return 1
    
    if not os.path.isfile(host_config['hostfile']):
        print('The source code of the host game could not be found.')
        return 1
    
    with open(host_config['hostfile'], 'r') as file:
        source = file.read()

    host = {
        'source': source,
        'game': host_config['game'],
        'settings': host_config['settings'],
        'requirements': host_config['requirements']
    }
    
    handler = NetworkInterface(user_id, user_secret)
    try:
        result = handler.create_host(host=host)
    except Exception as exc:
        print(f'Failed to create host game: {exc}')
        return 1

    result = result['answer']
    
    if 'error' in result:
        print('Host creation error:', result['error'])
        return 1
        
    print('The new users game enviroment has been successfully hosted.')
    
    host_config['host_id'] = result['host_id']
    with open(opt.hconfig, 'w') as file:
        file.write(json.dumps(host_config, indent=4))
    
    return 0


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cconfig", type=str, default="client-config.json", help="path to client-config.json")
    parser.add_argument("--hconfig", type=str, default="host-config.json", help="path to host-config.json")

    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    exit(create_host(opt))
