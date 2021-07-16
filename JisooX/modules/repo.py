import github
from pyrogram import filters
from JisooX import pbot as app


@app.on_message(filters.command("repos") & ~filters.edited)
async def give_repo(c, m):
    g = github.Github()
    list_of_users = ""
    count = 0
    repo = g.get_repo("ferikunn/JisooXRobot")
    for i in repo.get_contributors():
        count += 1
        list_of_users += f"*{count}.* [{i.login}](https://github.com/{i.login})\n"
    text = f"""[Github](https://github.com/ferikunn/JisooXRobot) | [Group](https://t.me/JisooSupport)
```----------------
| Contributors |
----------------```
{list_of_users}"""
    await m.reply(text, disable_web_page_preview=False)


__help__ = """
 ❍ /repos*:* To Get My Github Repository Link And Support Group Link
"""

__mod_name__ = "REPO"
