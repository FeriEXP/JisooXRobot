import requests
from JisooX.events import register


@register(pattern="^/truth ?(.*)")
async def _(td):
    try:
        kuntul = requests.get("https://tede-api.herokuapp.com/api/truth").json()
        results = f"**{kuntul['message']}**"
        return await td.reply(results)
    except Exception:
        await td.reply("`Something went wrong LOL...`")


@register(pattern="^/dare ?(.*)")
async def _(dr):
    try:
        kuntul = requests.get("https://tede-api.herokuapp.com/api/dare").json()
        results = f"**{kuntul['message']}**"
        return await dr.reply(results)
    except Exception:
        await dr.reply("`Something went wrong LOL...`")
