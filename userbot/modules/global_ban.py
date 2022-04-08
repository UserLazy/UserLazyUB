from asyncio import sleep
from os import remove

from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import MessageEntityMentionName
from telethon.tl.types import ChatBannedRights

from userbot import CMD_HELP
from userbot.events import register


NO_ADMIN = "`I am not an admin!`"
NO_SQL = "`Running on Non-SQL mode!`"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)


async def get_full_user(event):
    args = event.pattern_match.group(1).split(":", 1)
    extra = None
    if event.reply_to_msg_id and len(args) != 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif len(args[0]) > 0:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`UserID is required")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            return await event.edit("Something went wrong", str(err))
    return user_obj, extra


async def get_user_sender_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj


@register(outgoing=True, pattern=r"^\.gban(?: |$)(.*)")
async def gspider(userbot):
    lol = userbot
    sender = await lol.get_sender()
    me = await lol.client.get_me()
    if sender.id != me.id:
        userlazy = await lol.reply("`Gbanning...`")
    else:
        userlazy = await lol.edit("`Gbanning......`")
    me = await userbot.client.get_me()
    await userlazy.edit("`Global Banned user...`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        pass
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await userlazy.edit(f"**Something went wrong!!**")
    if user:
        if user.id == 870471128:
            return await userlazy.edit(
                f"**Didn't , Your father teach you ? That you can't gban your creator🖕**"
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import gmute
        except BaseException:
            pass
        try:
            await userbot.client(BlockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, BANNED_RIGHTS)
                a += 1
                await userlazy.edit(f"`Gbanned Total Affected Chats : {a}`")
            except BaseException:
                b += 1
    else:
        await userlazy.edit(f"`Reply to a user !!`")
    try:
        if gmute(user.id) is False:
            return await userlazy.edit(f"`Error! User already gbanned.`")
    except BaseException:
        pass
    return await userlazy.edit(
        f"`Gbanned` [{user.first_name}](tg://user?id={user.id}) `in {a} chats.\nAdded to gbanwatch.`"
    )


@register(outgoing=True, pattern=r"^\.ungban(?: |$)(.*)")
async def gspider(userbot):
    lol = userbot
    sender = await lol.get_sender()
    me = await lol.client.get_me()
    if sender.id != me.id:
        userlazy = await lol.reply("`UnGbanning...`")
    else:
        userlazy = await lol.edit("`UnGbanning....`")
    me = await userbot.client.get_me()
    await userlazy.edit(f"`Trying to ungban user !`")
    my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
    await userbot.get_chat()
    a = b = 0
    if userbot.is_private:
        user = userbot.chat
        reason = userbot.pattern_match.group(1)
    else:
        pass
    try:
        user, reason = await get_full_user(userbot)
    except BaseException:
        pass
    try:
        if not reason:
            reason = "Private"
    except BaseException:
        return await userlazy.edit("`Terjadi Kesalahan!!`")
    if user:
        if user.id == 870471128:
            return await userlazy.edit(
                "`You can't gban him... as a result you can not ungban him... he is my creator!`"
            )
        try:
            from userbot.modules.sql_helper.gmute_sql import ungmute
        except BaseException:
            pass
        try:
            await userbot.client(UnblockRequest(user))
        except BaseException:
            pass
        testuserbot = [
            d.entity.id
            for d in await userbot.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for i in testuserbot:
            try:
                await userbot.client.edit_permissions(i, user, UNBAN_RIGHTS)
                a += 1
                await userlazy.edit(f"`Ungbanning... AFFECTED CHATS - {a} `")
            except BaseException:
                b += 1
    else:
        await userlazy.edit("`Reply to a user !!`")
    try:
        if ungmute(user.id) is False:
            return await userlazy.edit("`Error! User probably already ungbanned.`")
    except BaseException:
        pass
    return await userlazy.edit(
        f"`Ungbanned` [{user.first_name}](tg://user?id={user.id}) `in {a} chats.\nRemoved from gbanwatch.`"
    )


CMD_HELP.update(
    {
        "gban": ">`.gban <userid/reply>`"
        "\nUsage: For globally banned chat "
    }
)
