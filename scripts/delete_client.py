import argparse
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hub.network_interface import NetworkInterface


def deauth(opt) -> int:
    print(f'Optional arguments: {opt}')

    try:
        with open(opt.config, 'r') as file:
            config = json.load(file)
            user_id = config['auth']['user_id']
            user_secret = config['auth']['user_secret']
            NetworkInterface.server_url = f"http://{config['host']}:{config['port']}"
    except Exception as exc:
        print(f'Error loading configuration: {exc}')
        return 1
    
    handler = NetworkInterface(user_id, user_secret)
    try:
        result = handler.delete_user()
    except Exception as exc:
        print(f'Failed to delete user: {exc}')
        return 1

    result = result['answer']
    
    if 'error' in result:
        print('Delete user error:', result['error'])
        return 1
        
    print(f'The user: \'{user_id}\' has been successfully deleted.')
    
    return 0


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="client-config.json", help="path to client-config.json")

    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    exit(deauth(opt))