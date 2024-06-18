import argparse
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hub.network_interface import NetworkInterface


def post_bot(opt) -> int:
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
            
        with open(opt.bconfig, 'r') as file:
            bot_config = json.load(file)
            botfile = bot_config['botfile']
            
        with open(botfile, 'r') as file:
            bot_source = file.read()
    except Exception as exc:
        print(f'Error loading configurations: {exc}')
        return 1
    
    handler = NetworkInterface(user_id, user_secret)
    try:
        result = handler.post_bot(bot_source=bot_source, host_id=host_id)
    except Exception as exc:
        print(f'Failed to post bot: {exc}')
        return 1

    result = result['answer']
    
    if 'error' in result:
        print('Post bot error:', result['error'])
        return 1
        
    print('The bot has been successefully posted.')
    print(result)
    
    return 0


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cconfig", type=str, default="client-config.json", help="path to client-config.json")
    parser.add_argument("--hconfig", type=str, default="host-config.json", help="path to host-config.json")
    parser.add_argument("--bconfig", type=str, default="bot-config.json", help="path to bot-config.json")

    return parser.parse_args()


if __name__ == "__main__":
    opt = parse_opt()
    exit(post_bot(opt))
