# logspout-tme

logspout-tme is a snippet for building couple containers to translate the logs from docker.sock from host to Telegram via Telegram MTProto protocol

### Installation

1. Get from GitHub

```sh
$ git clone https://github.com/siroBS/logspout-tme.git
```
2. Set secret information; you need:
    
    _Telegram "Application API" id and hash_ 
    ```python
    API_ID
    API_HASH
    ```
    _Token for your bot (@BotFather)_
    ```python
    BOT_TOKEN
    ```
    _Server with Telegram MTProto instance_
    ```python
    PROXY_IP
    PROXY_PORT
    PROXY_SECRET
    ```
    _Receiver Telegram id_
    ```python
    ADMIN_ID
    ```

3. Start up your logger

    _cd logspout-tme/_
```sh
$ docker-compose up -d
```

### Dependencies
[![GitHub](https://img.shields.io/github/license/LonamiWebs/Telethon?label=Telethon%20%3E%3D%201.13.0)](https://github.com/LonamiWebs/Telethon.git)
[![Docker pulls](https://img.shields.io/docker/pulls/gliderlabs/logspout.svg?label=logspout%20%3E%3D%203.2.11)](https://hub.docker.com/r/gliderlabs/logspout/)
[![GitHub](https://img.shields.io/github/license/aio-libs/aiohttp?label=aiohttp%20%3E%3D%203.6.2)](https://github.com/aio-libs/aiohttp)


