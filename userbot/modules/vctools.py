# Copyright (C) 2021 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de
#
# Kalo mau ngecopas, jangan hapus credit ya goblok

from telethon.tl.functions.channels import GetFullChannelRequest as getchat
from telethon.tl.functions.phone import CreateGroupCallRequest as startvc
from telethon.tl.functions.phone import DiscardGroupCallRequest as stopvc
from telethon.tl.functions.phone import EditGroupCallTitleRequest as settitle
from telethon.tl.functions.phone import GetGroupCallRequest as getvc
from telethon.tl.functions.phone import InviteToGroupCallRequest as invitetovc

from userbot import ALIVE_NAME
from userbot import CMD_HELP, bot
from userbot.events import register


async def get_call(event):
    mm = await event.client(getchat(event.chat_id))
    xx = await event.client(getvc(mm.full_chat.call))
    return xx.call


def user_list(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


@register(outgoing=True, disable_errors=True, pattern=r"^\.startvc$")
async def start_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await c.edit(f"**Sorry {ALIVE_NAME} not admin 👮**")
        return
    try:
        await c.client(startvc(c.chat_id))
        await c.edit("`Voice Chat Started...`")
    except Exception as ex:
        await c.edit(f"**ERROR:** `{ex}`")


@register(outgoing=True, disable_errors=True, pattern=r"^\.stopvc$")
async def stop_voice(c):
    chat = await c.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await c.edit(f"**Soryy {ALIVE_NAME} not admin 👮**")
        return
    try:
        await c.client(stopvc(await get_call(c)))
        await c.edit("`Voice Chat Stopped...`")
    except Exception as ex:
        await c.edit(f"**ERROR:** `{ex}`")


@register(outgoing=True, disable_errors=True, pattern=r"^\.vcinvite$")
async def _(c):
    await c.edit("`Inviting members to voice chat...`")
    users = []
    z = 0
    async for x in c.client.iter_participants(c.chat_id):
        if not x.bot:
            users.append(x.id)
    botman = list(user_list(users, 6))
    for p in botman:
        try:
            await c.client(invitetovc(call=await get_call(c), users=p))
            z += 6
        except BaseException:
            pass
    await c.edit(f"`{z}` **Users invited to voice call group**")


@register(outgoing=True, disable_errors=True, pattern=r"^\.vctitle$")
async def change_title(e):
    title = e.pattern_match.group(1).lower()
    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not title:
        return await e.edit("**Enter the voice call group title**")

    if not admin and not creator:
        await e.edit(f"**Sorry {ALIVE_NAME} not admin 👮**")
        return
    try:
        await e.client(settitle(call=await get_call(e), title=title.strip()))
        await e.edit(f"**Change title succsesed** `{title}`")
    except Exception as ex:
        await e.edit(f"**ERROR:** `{ex}`")


CMD_HELP.update(
    {
        "vctools": ">.`startvc`"
        "\nUsage: Start voice call group"
        "\n\n>`.stopvc`"
        "\nUsage: Stop voice call group"
        "\n\n>`.vcinvite`"
        "\nUsage: Invite members to voice call group"
        "\n\n>`.vctitle <new title>`"
        "\nUsage: Change voice call group title"
    }
)
