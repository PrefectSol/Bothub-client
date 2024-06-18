# BotHub-client

## Server Architecture
![](https://sun9-63.userapi.com/impg/ADTAsBJuR0-TvXZj3PXDWLIZpMLs6GFiY8AqjQ/Z1nGVUCr_aE.jpg?size=868x586&quality=96&sign=cb61f0186f24d422221ce4f18c87a847&type=album)
- (Web impl. is not available)


A simple client for send local self-written games and bots in the form of modules with Docker on server.

Also check [Bothub-client](https://github.com/PrefectSol/BotHub-server.git) for using client on server

 - Before sending requests to the server, make sure that the network module is enabled, otherwise the requests will be ignored
 - `hub/network_interface.py` implements the api for working with the server

- The bot is implemented based on an abstract class `hub/abc_bot.py`
- The game is implemented based on an abstract class `hub/game.py`

## Authentication
Creates a user to work with the server

The permissions are set via the `client-config.json` file
```bash
make auth
```

## Deauthentication
Deletes the user and all his linked hosts via the `client-config.json` file
```bash
make deauth
```

## Host Create
Creates a new host on the server with the submitted game. It is configured via the `host-config.json` file
```bash
make hcreate
```

## Host Delete
Deletes the user's host
```bash
make hdelete
```

## Sending the bot to the host
Sends the bot to the specified host. It is configured via the `bot-config.json` file
```bash
make post
```

## View database
Gets the url for viewing logs
```bash
make view
```

## Clear solution
```bash
make clear
```