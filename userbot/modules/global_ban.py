from asyncio import sleep
from os import remove

from telethon.events import ChatAction
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from userbot import BOTLOG_CHATID, CMD_HELP, bot
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


@bot.on(ChatAction)
async def handler(new):
    if not new.user_joined and not new.user_added:
        return
    try:
        from userbot.modules.sql_helper.gban_sql import is_gban

        guser = await new.get_user()
        gban = is_gban(guser.id)
    except BaseException:
        return
    if gban:
        for i in gban:
            if i.sender == str(guser.id):
                chat = await new.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if admin or creator:
                    try:
                        await client.edit_permissions(
                            new.chat_id, guser.id, BANNED_RIGHTS,
                        )
                        await new.reply(
                            f"**First Name :** [{guser.id}](tg://user?id={guser.id}) was **Banned**\n"
                            f"**Reason :** `Gbanned`"
                        )
                    except BaseException:
                        return


@register(outgoing=True, disable_errors=True, pattern=r"^\.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """For .gban command, globally gbans the replied/tagged person"""
    # Admin or creator check
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except AttributeError:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if not user:
        return

    # If pass, inform and start gbanning
    userban = [
            d.entity.id
            for d in await un_gban.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for idiot in userban:
            try:
                await gspdr.client(EditBannedRequest(idiot, user, BANNED_RIGHTS))
                await gspdr.edit("`Grabs a huge, gbanned succses!`")
            except BaseException:
                pass

    if gban(user.id) is False:
        await gspdr.edit("`Error! User probably already gbanned.\nRe-rolls the ban.`")
    else:
        if reason:
            await gspdr.edit(f"`Globally banned!`\nReason: {reason}")
        else:
            await gspdr.edit("`Globally banned!`")

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID,
                "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)",
            )

            
@register(outgoing=True, disable_errors=True, pattern=r"^\.ungban(?: |$)(.*)")
async def ungbans(un_gban):
    """For .ungban command, ungbans the target in the userbot"""
    # Admin or creator check
    chat = await un_gban.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # If not admin and not creator, return
    if not admin and not creator:
        await un_gban.edit(NO_ADMIN)
        return

    # Check if the function running under SQL mode
    try:
        from userbot.modules.sql_helper.gban_sql import ungban
    except AttributeError:
        await un_gban.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gban)
    user = user[0]
    if not user:
        return

    # If pass, inform and start ungbanning
    userunban = [
            d.entity.id
            for d in await un_gban.client.get_dialogs()
            if (d.is_group or d.is_channel)
        ]
        for idiot in userunban:
            try:
                await un_gban.client(EditBannedRequest(idiot, user, UNBAN_RIGHTS))
                await un_gban.edit("```Ungbanning...```")
            except BaseException:
                pass

    if ungban(user.id) is False:
        await un_gban.edit("`Error! User probably not gban.`")
    else:
        # Inform about success
        await un_gban.edit("```Ungbanned Successfully```")
        await sleep(3)
        await un_gban.delete()

        if BOTLOG:
            await un_gban.client.send_message(
                BOTLOG_CHATID,
                "#UNGBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {un_gban.chat.title}(`{un_gban.chat_id}`)",
            )
