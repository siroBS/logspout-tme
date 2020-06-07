
import asyncio
import aiohttp
import re
import traceback

from telethon import TelegramClient, events
from telethon.network.connection import ConnectionTcpMTProxyRandomizedIntermediate

# import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Listen logspout address
# LISTEN_ADDRESS = 'http://127.0.0.1:8000/logs'
LISTEN_ADDRESS = 'http://logspout:80/logs'

# Remember to use your own values from my.telegram.org!
# Telegram have "Application API" (i prefer mtproto way with 'dd...' key, such here) with two types connection: "as phone, password" && "as bot tocken way"; and "Bot API" (http way, not secure); both
API_ID = 0000000
API_HASH = 'a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0'

# @bot
BOT_TOKEN = '000000000:A0aA0aA0aA0aA0aA0aA0aA0aA0aA0aA0aA0'

# MTProto instance serve on
PROXY_IP = '0.0.0.0'
# PROXY_PORT = 443
PROXY_PORT = 0
PROXY_SECRET = 'dda0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0'

# Admin ID for sending logs
ADMIN_ID = 000000000

# COMPLETE_TRACEBACK = True
COMPLETE_TRACEBACK = False


try: from secret.secret import API_ID, API_HASH, BOT_TOKEN, PROXY_IP, PROXY_PORT, PROXY_SECRET, ADMIN_ID
except: pass

try: from my_secret import API_ID, API_HASH, BOT_TOKEN, PROXY_IP, PROXY_PORT, PROXY_SECRET, ADMIN_ID
except: pass 

    
proxy = (PROXY_IP, PROXY_PORT, PROXY_SECRET)

# If not None, create database file for save session
# client = TelegramClient('Logger', api_id, api_hash, 
client = TelegramClient(None, API_ID, API_HASH, 
                        proxy=proxy, 
                        connection=ConnectionTcpMTProxyRandomizedIntermediate)


async def message(text):
    print(text)
    await asyncio.sleep(0)
    try: await client.send_message(ADMIN_ID, text)
    except: pass


async def listen_logspout():
    
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout()) as session:
        
        async with session.put(LISTEN_ADDRESS) as resp:
            await message(CONNECT_OK_LOGSPOUT)
        
        async with session.get(LISTEN_ADDRESS) as resp:
            while True:
                bytes_chunk = (await resp.content.readchunk())[0]
                text = bytes_chunk.decode(encoding='utf-8')
                clear_text = ansi_escape.sub('', text)
                await client.send_message(ADMIN_ID, clear_text)


@client.on(events.NewMessage(pattern='/VERBOSE'))
async def verbose(event):
    global COMPLETE_TRACEBACK
    COMPLETE_TRACEBACK = not COMPLETE_TRACEBACK
    print(MESSAGE_VERBOSE)
    await event.reply(f'Been set: {COMPLETE_TRACEBACK}')


@client.on(events.NewMessage(pattern='/help'))
async def help(event):
    await event.reply('Version: 0.35')





async def main(loop):

    await message(MESSAGE_STARTING)

    while True:    
        
        try:
            await message('\n---')
            await client.start(bot_token=BOT_TOKEN)
            await message(CONNECT_OK_MTPROTO)
            while True:
                try:
                    await listen_logspout()
                except Exception as ex:
                    await message(f'\n{ex}\n')
                    if COMPLETE_TRACEBACK: await message(f'\n\n\n{traceback.format_exc()}\n\n')
                await asyncio.sleep(15) 
        except Exception as ex:
            await message(f'\n{ex}\n')
            if COMPLETE_TRACEBACK: await message(f'\n\n\n{traceback.format_exc()}\n\n')    
        finally:
            await client.disconnect()
        
        
        await asyncio.sleep(15)







# await asyncio.sleep(0)

ansi_escape = re.compile(r'''
                            \x1B  # ESC
                            (?:   # 7-bit C1 Fe (except CSI)
                                [@-Z\\-_]
                            |     # or [ for CSI, followed by a control sequence
                                \[
                                [0-?]*  # Parameter bytes
                                [ -/]*  # Intermediate bytes
                                [@-~]   # Final byte
                                [\n]*
                                [ ]*
                            )
                        ''', re.VERBOSE)

CONNECT_OK_MTPROTO = f'\n     ----->     Connected to MTPROTO.\n'
CONNECT_OK_LOGSPOUT = f'\n     ----->     Connected to "logspout".\n'
MESSAGE_VERBOSE = f'\n     ----->     VERBOSE: {COMPLETE_TRACEBACK}\n'
MESSAGE_STARTING = f'\n     ----->     Starting...\n'


if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
