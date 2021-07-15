__help__ = """
Blacklists are used to stop certain triggers from being said in a group. Any time the trigger is mentioned, \
the message will immediately be deleted. A good combo is sometimes to pair this up with warn filters!
*NOTE:* blacklists do not affect group admins.
 - /blacklist: View the current blacklisted words.
*Admin only:*
 - /addblacklist <triggers>: Add a trigger to the blacklist. Each line is considered one trigger, so using different \
lines will allow you to add multiple triggers.
 - /unblacklist <triggers>: Remove triggers from the blacklist. Same newline logic applies here, so you can remove \
multiple triggers at once.
 - /rmblacklist <triggers>: Same as above.
*Blacklist Users :*
 - /ignore : blacklist users
 - /notice : 
 - /ignoredlist : List of blacklisted users 
*Blacklist Sticker :*
 - /blsticker: See current blacklisted sticker.
*Only admin:*
 - /addblsticker <sticker link>: Add the sticker trigger to the black list. Can be added via reply sticker.
 - /unblsticker <sticker link>: Remove triggers from blacklist. The same newline logic applies here, so you can delete multiple triggers at once.
 - /rmblsticker <sticker link>: Same as above.
 - /blstickermode ban/tban/mute/tmute .
Note:
 - `<sticker link>` can be `https://t.me/addstickers/<sticker>` or just `<sticker>` or reply to the sticker message.
"""

__mod_name__ = "BLACKLIST"
