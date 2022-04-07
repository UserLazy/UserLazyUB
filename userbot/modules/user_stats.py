import time

from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.functions.contacts import GetBlockedRequest
from telethon.tl.functions.messages import GetAllStickersRequest
from telethon.tl.types import Channel, Chat, User

from userbot import CMD_HELP
from userbot.events import register


def user_full_name(user):
    nick = [user.first_name, user.last_name]
    nick = [i for i in list(nick) if i]
    return " ".join(nick)


def user_tag(user):
    mentions = user_full_name(user) or "No Name"
    return f"[{mentions}](tg://user?id={user.id})"


@register(outgoing=True, pattern=r"^\.stats ?(.*)")
async def stats(
    event: NewMessage.Event,
) -> None:
    stat = await event.edit("`Collecting stats...`")
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    try:
        ct = (await event.client(GetBlockedRequest(1, 0))).count
    except AttributeError:
        ct = 0
    try:
        sp = await event.client(GetAllStickersRequest(0))
        sp_count = len(sp.sets)
    except BaseException:
        sp_count = 0
    full_name = user_tag(await event.client.get_me())
    response = f"📊 **Stats for {full_name}** \n\n"
    response += f"**Private Chats:** {private_chats} \n"
    response += f"**  •• **`Users: {private_chats - bots}` \n"
    response += f"**  •• **`Bots: {bots}` \n"
    response += f"**Groups:** {groups} \n"
    response += f"**Channels:** {broadcast_channels} \n"
    response += f"**Admin in Groups:** {admin_in_groups} \n"
    response += f"**  •• **`Creator: {creator_in_groups}` \n"
    response += f"**  •• **`Admin Rights: {admin_in_groups - creator_in_groups}` \n"
    response += f"**Admin in Channels:** {admin_in_broadcast_channels} \n"
    response += f"**  •• **`Creator: {creator_in_channels}` \n"
    response += f"**  •• **`Admin Rights: {admin_in_broadcast_channels - creator_in_channels}` \n"
    response += f"**Unread:** {unread} \n"
    response += f"**Unread Mentions:** {unread_mentions} \n"
    response += f"**Blocked Users:** {ct}\n"
    response += f"**Total Stickers Pack Installed :** `{sp_count}`\n\n"
    response += f"⏱ **__It Took:__** {stop_time:.02f}s \n"
    await stat.edit(response)


@register(outgoing=True, pattern=r"^\.ustats ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = "".join(event.text.split(maxsplit=1)[1:])
    reply_message = await event.get_reply_message()
    if not input_str and not reply_message:
        await event.edit(
            "`Reply to user messages or provide userid/username`",
        )
    if input_str:
        try:
            uid = int(input_str)
        except ValueError:
            try:
                u = await event.client.get_entity(input_str)
            except ValueError:
                await event.edit("`Provide userid or username to view group history`")
            uid = u.id
    else:
        uid = reply_message.sender_id
    chat = "@tgscanrobot"
    sevent = await event.edit("`Processing...`")
    async with event.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(f"{uid}")
        except Exception:
            await sevent.edit("**Unblock @tgscanrobot and try again**")
        response = await conv.get_response()
        await event.client.send_read_acknowledge(conv.chat_id)
        await sevent.edit(response.text)
        """Cleanup after completed"""
        await event.client.delete_messages(conv.chat_id, [msg.id, response.id])


CMD_HELP.update(
    {
        "user_stats": ">`.stats`"
        "\nUsage: To check user statistics"
        "\n\n>`.ustats`"
        "\nUsage: To check which group the person has joined"
    }
)
