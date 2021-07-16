from pyrogram import filters
from JisooX import pbot as app
from JisooX.utils.http import get


@app.on_message(filters.command("repos") & ~filters.edited)
async def repo(_, message):
    users = await get(
        "https://api.github.com/repos/ferikunn/JisooXRobot/contributors"
    )
    list_of_users = ""
    count = 1
    for user in users:
        list_of_users += (
            f"**{count}.** [{user['login']}]({user['html_url']})\n"
        )
        count += 1

    text = f"""[Github](https://github.com/ferikunn/JisooXRobot) | [Group](https://t.me/JisooSupport)
```----------------
| Contributors |
----------------```
{list_of_users}"""
    await app.send_message(
        message.chat.id, text=text, disable_web_page_preview=True
    )


__help__ = """
 ❍ /repos*:* To Get My Github Repository Link And Support Group Link
"""

__mod_name__ = "Repo"
