# credits @RoseLoverX
from JisooX import telethn as tbot
from JisooX.events import register
import os
import asyncio
import os
import time
from datetime import datetime
from JisooX import OWNER_ID
from JisooX import TEMP_DOWNLOAD_DIRECTORY as path
from JisooX import TEMP_DOWNLOAD_DIRECTORY
from datetime import datetime
water = './JisooX/resources/Twitter.jpeg'
client = tbot

@register(pattern=r"^/send ?(.*)")
async def Prof(event):
    if event.sender_id == OWNER_ID:
        pass
    else:
        return
    thumb = water
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    the_plugin_file = "./JisooX/modules/{}.py".format(input_str)
    if os.path.exists(the_plugin_file):
     message_id = event.message.id
     await event.client.send_file(
             event.chat_id,
             the_plugin_file,
             force_document=True,
             allow_cache=False,
             thumb=thumb,
             reply_to=message_id,
         )
    else:
        await event.reply("No File Found!")


from JisooX import telethn as tbot, OWNER_ID, DEV_USERS
from JisooX.events import register
import os
import asyncio
import os
import time
from datetime import datetime
from JisooX import TEMP_DOWNLOAD_DIRECTORY as path
from JisooX import TEMP_DOWNLOAD_DIRECTORY
from datetime import datetime
import asyncio
import os
import time
from datetime import datetime as dt
opn = []

@register(pattern="/open")
async def _(event):
    xx = await event.reply("Processing...")
    if event.reply_to_msg_id:
        a = await event.get_reply_message()
        if a.media:
            b = await a.download_media()
            c = open(b, "r")
            d = c.read()
            c.close()
            n = 4096
            for bkl in range(0, len(d), n):
                opn.append(d[bkl : bkl + n])
            for bc in opn:
                await event.client.send_message(
                    event.chat_id,
                    f"{bc}",
                    reply_to=event.reply_to_msg_id,
                )
            await event.delete()
            opn.clear()
            os.remove(b)
            await xx.delete()
        else:
            return await event.reply("Reply to a readable file")
    else:
        return await event.reply("Reply to a readable file")

client = tbot
import time
from io import BytesIO
from pathlib import Path
from JisooX import telethn as borg
from telethon import functions, types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import SendMediaRequest


@register(pattern="^/make ?(.*)")
async def get(event):
    name = event.text[5:]
    if name is None:
        await event.reply("reply to text message as `.ttf <file name>`")
        return
    m = await event.get_reply_message()
    if m.text:
        with open(name, "w") as f:
            f.write(m.message)
        await event.delete()
        await event.client.send_file(event.chat_id, name, force_document=True)
        os.remove(name)
    else:
        await event.reply("reply to text message as `.ttf <file name>`")
