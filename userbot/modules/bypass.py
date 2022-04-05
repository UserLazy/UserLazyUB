import requests
from bs4 import BeautifulSoup as bs
import re
from userbot.events import register


def get_html(url):
    tag_li = []
    req = requests.get(url)
    res = bs(req.text, "html.parser")
    box = res.find("div", class_="soraddlx soradlg").parent.find_all("li")
    if len(box) != 0:
        for clear in box:
            if clear.get_text() == "MKV":
                box.remove(clear)
            else:
                pass
    for box_ in box:
        tag_li.append(box_)
    return {"html": tag_li}


def link_download(query, url):
    tag_label = []
    tag_href = []
    r = get_html(url)["html"]
    for k, v in enumerate(r[query].find_all("a")):
        tag_href.append({"server": v.get_text(strip=True), "link": v["href"]})
    for p, o in enumerate(r[query].find_all("label")):
        tag_label.append(o.get_text())
    return {"label": tag_label, "url": tag_href}


@register(outgoing=True, pattern=r"^\.bypass ?(.*)")
async def _(event):
    url = event.pattern_match.group(1)
    if not url:
        await event.edit("Enter your url")
    elif "https://" not in url:
        await event.edit("Enter url")
        return
    else:
        await event.edit("`please wait..`")
        msg = "<b>➲ Link Download:</b>\n═════════════════\n"
        p = link_download(1, url)
        for label_name in p["label"]:
            msg += f"<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"

        p = link_download(2, url)
        for label_name in p["label"]:
            msg += f"\n<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"

        p = link_download(3, url)
        for label_name in p["label"]:
            msg += f"\n<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"

        p = link_download(4, url)
        for label_name in p["label"]:
            msg += f"\n<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"

        p = link_download(5, url)
        for label_name in p["label"]:
            msg += f"\n<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"

        p = link_download(6, url)
        for label_name in p["label"]:
            msg += f"\n<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"

        p = link_download(7, url)
        for label_name in p["label"]:
            msg += f"\n<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"

        p = link_download(8, url)
        for label_name in p["label"]:
            msg += f"\n<b>↛ {label_name} ↚</b>\n"
        for server_link in p["url"]:
            server_name = server_link["server"]
            server_url = server_link["link"]
            msg += f"➣ <a href='{server_url}'>{server_name}</a>\n"
        await event.edit(msg, parse_mode="html")
