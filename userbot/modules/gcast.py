# Ultroid - UserBot
# Copyright (C) 2020 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by Koala @manusiarakitann
# Recode by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio
import os

import heroku3
from requests import get
from telethon.errors import FloodWaitError

from userbot import CMD_HELP, HEROKU_API_KEY, HEROKU_APP_NAME, BLACKLIST_GCAST
from userbot.events import register


while 0 < 6:
    _GCAST_BLACKLIST = get(
        "https://raw.githubusercontent.com/mrismanaziz/Reforestation/master/blacklistgcast.json"
    )
    if _GCAST_BLACKLIST.status_code != 200:
        if 0 != 5:
            continue
        GCAST_BLACKLIST = [-1001473548283, -1001390552926, -1001532001865]
        break
    GCAST_BLACKLIST = _GCAST_BLACKLIST.json()
    break

del _GCAST_BLACKLIST


Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
blchat = os.environ.get("BLACKLIST_GCAST") or ""


@register(pattern=r"^\.gcast(?: |$)(.*)", outgoing=True, disable_edited=True)
async def gcast(event):
    if xx := event.pattern_match.group(1):
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await event.edit("**Leave a message or reply**")
    kk = await event.edit("`Globally broadcasting message...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            if chat not in GCAST_BLACKLIST and chat not in BLACKLIST_GCAST:
                try:
                    await event.client.send_message(chat, msg)
                    await asyncio.sleep(0.1)
                    done += 1
                except FloodWaitError as anj:
                    await asyncio.sleep(int(anj.seconds))
                    await event.client.send_message(chat, msg)
                    done += 1
                except BaseException:
                    er += 1
    await kk.edit(
        f"**Successfully sent message to** `{done}` **group\nFailed to send message to** `{er}` **group**"
    )


@register(pattern=r"^\.blchats(?: |$)(.*)", outgoing=True)
async def sudo(event):
    blacklistgc = "True" if BLACKLIST_GCAST else "False"
    blc = blchat
    list = blc.replace(" ", "\n» ")
    if blacklistgc == "True":
        await event.edit(
            f"🔮 **Blacklist GCAST:** `Enabled`\n\n📚 **Blacklist Group:**\n» {list}\n\nType `.addblacklist` in the group you want to add to the gcast blacklist.",
        )
    else:
        await event.edit("🔮 **Blacklist GCAST:** `Disabled`")


@register(pattern=r"^\.addblacklist(?: |$)(.*)", outgoing=True)
async def add(event):
    xxnx = await event.edit("`Processing...`")
    var = "BLACKLIST_GCAST"
    gc = event.chat_id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await xxnx.edit(
            "**Please add var** `HEROKU_APP_NAME` **to add blacklist**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    blgc = f"{BLACKLIST_GCAST} {gc}"
    blacklistgrup = (
        blgc.replace("{", "")
        .replace("}", "")
        .replace(",", "")
        .replace("[", "")
        .replace("]", "")
        .replace("set() ", "")
    )
    await xxnx.edit(
        f"**Successfully added** `{gc}` **to gcast blacklist.**\n\nRestarting your bot to apply changes."
    )
    heroku_Config[var] = blacklistgrup


@register(pattern=r"^\.delblacklist(?: |$)(.*)", outgoing=True)
async def _(event):
    xxx = await event.edit("`Processing...`")
    gc = event.chat_id
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await xxx.edit(
            "**Please add var** `HEROKU_APP_NAME` **to add blacklist**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    gett = str(gc)
    if gett in blchat:
        blacklistgrup = blchat.replace(gett, "")
        await xxx.edit(
            f"**Successfully deleted** `{gc}` **to gcast blacklist.**\n\nRestarting your bot to apply changes."
        )
        var = "BLACKLIST_GCAST"
        heroku_Config[var] = blacklistgrup
    else:
        await xxx.edit(
            "**This group is not on the gcast blacklist.**", 45
        )


CMD_HELP.update(
    {
        "gcast": ">`.gcast` <reply to message>/<text>"
        "\nUsage: Sends a global broadcast message to all the groups you belong to."
        "\n\n>`.blchats`"
        "\nUsage: To check the gcast blacklist information."
        "\n\n>`.addblacklist`"
        "\nUsage: To add the group to the gcast blacklist."
        \"\n\n>`.delblacklist`"
        "\nUsage: To delete the group to the gcast blacklist."
    }
)
