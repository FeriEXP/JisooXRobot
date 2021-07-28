import requests
from JisooX.events import register


@register(pattern="^/hilih ?(.*)")
async def _(hilih):
    kuntul = hilih.pattern_match.group(1)
    if not kuntul:
        await hilih.reply("Usage: /hilih <text>")
        return
    try:
        resp = requests.get(f"https://tede-api.herokuapp.com/api/hilih?kata={kuntul}").json()
        hilihnya = f"{resp['result']}"
        return await hilih.reply(hilihnya)
    except Exception:
        await hilih.reply("Something went wrong LOL...")
