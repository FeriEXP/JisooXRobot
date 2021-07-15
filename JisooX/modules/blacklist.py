import html
import re

from typing import List

from telegram import Bot, Update, ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, MessageHandler, Filters, run_async

import JisooX.modules.sql.blacklist_sql as sql

from JisooX import dispatcher, LOGGER
from JisooX.modules.disable import DisableAbleCommandHandler
from JisooX.modules.helper_funcs.chat_status import user_admin, user_not_admin, connection_status
from JisooX.modules.helper_funcs.extraction import extract_text
from JisooX.modules.helper_funcs.misc import split_message

BLACKLIST_GROUP = 11


@run_async
@connection_status
def blacklist(bot: Bot, update: Update, args: List[str]):

    msg = update.effective_message
    chat = update.effective_chat

    update_chat_title = chat.title
    message_chat_title = update.effective_message.chat.title

    if update_chat_title == message_chat_title:
        BASE_BLACKLIST_STRING = "Current <b>blacklisted</b> words:\n"
    else:
        BASE_BLACKLIST_STRING = f"Current <b>blacklisted</b> words in <b>{update_chat_title}</b>:\n"

    all_blacklisted = sql.get_chat_blacklist(chat.id)

    filter_list = BASE_BLACKLIST_STRING

    if len(args) > 0 and args[0].lower() == 'copy':
        for trigger in all_blacklisted:
            filter_list += "<code>{}</code>\n".format(html.escape(trigger))
    else:
        for trigger in all_blacklisted:
            filter_list += " - <code>{}</code>\n".format(html.escape(trigger))

    split_text = split_message(filter_list)
    for text in split_text:
        if text == BASE_BLACKLIST_STRING:
            if update_chat_title == message_chat_title:
                msg.reply_text("There are no blacklisted messages here!")
            else:
                msg.reply_text(f"There are no blacklisted messages in <b>{update_chat_title}</b>!", parse_mode=ParseMode.HTML)
            return
        msg.reply_text(text, parse_mode=ParseMode.HTML)


@run_async
@connection_status
@user_admin
def add_blacklist(bot: Bot, update: Update):

    msg = update.effective_message
    chat = update.effective_chat
    words = msg.text.split(None, 1)

    if len(words) > 1:
        text = words[1]
        to_blacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
        
        for trigger in to_blacklist:
            sql.add_to_blacklist(chat.id, trigger.lower())

        if len(to_blacklist) == 1:
            msg.reply_text("Added <code>{}</code> to the blacklist!".format(html.escape(to_blacklist[0])),
                           parse_mode=ParseMode.HTML)

        else:
            msg.reply_text(
                "Added <code>{}</code> triggers to the blacklist.".format(len(to_blacklist)), parse_mode=ParseMode.HTML)

    else:
        msg.reply_text("Tell me which words you would like to remove from the blacklist.")


@run_async
@connection_status
@user_admin
def unblacklist(bot: Bot, update: Update):

    msg = update.effective_message
    chat = update.effective_chat
    words = msg.text.split(None, 1)

    if len(words) > 1:
        text = words[1]
        to_unblacklist = list(set(trigger.strip() for trigger in text.split("\n") if trigger.strip()))
        successful = 0

        for trigger in to_unblacklist:
            success = sql.rm_from_blacklist(chat.id, trigger.lower())
            if success:
                successful += 1

        if len(to_unblacklist) == 1:
            if successful:
                msg.reply_text("Removed <code>{}</code> from the blacklist!".format(html.escape(to_unblacklist[0])),
                               parse_mode=ParseMode.HTML)
            else:
                msg.reply_text("This isn't a blacklisted trigger...!")

        elif successful == len(to_unblacklist):
            msg.reply_text(
                "Removed <code>{}</code> triggers from the blacklist.".format(
                    successful), parse_mode=ParseMode.HTML)

        elif not successful:
            msg.reply_text(
                "None of these triggers exist, so they weren't removed.", parse_mode=ParseMode.HTML)

        else:
            msg.reply_text(
                "Removed <code>{}</code> triggers from the blacklist. {} did not exist, "
                "so were not removed.".format(successful, len(to_unblacklist) - successful),
                parse_mode=ParseMode.HTML)
    else:
        msg.reply_text("Tell me which words you would like to remove from the blacklist.")


@run_async
@connection_status
@user_not_admin
def del_blacklist(bot: Bot, update: Update):

    chat = update.effective_chat
    message = update.effective_message
    to_match = extract_text(message)

    if not to_match:
        return

    chat_filters = sql.get_chat_blacklist(chat.id)
    for trigger in chat_filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
        if re.search(pattern, to_match, flags=re.IGNORECASE):
            try:
                message.delete()
            except BadRequest as excp:
                if excp.message == "Message to delete not found":
                    pass
                else:
                    LOGGER.exception("Error while deleting blacklist message.")
            break


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(chat_id, user_id):
    blacklisted = sql.num_blacklist_chat_filters(chat_id)
    return "There are {} blacklisted words.".format(blacklisted)


def __stats__():
    return "{} blacklist triggers, across {} chats.".format(sql.num_blacklist_filters(),
                                                            sql.num_blacklist_filter_chats())

BLACKLIST_HANDLER = DisableAbleCommandHandler("blacklist", blacklist, pass_args=True, admin_ok=True)
ADD_BLACKLIST_HANDLER = CommandHandler("addblacklist", add_blacklist)
UNBLACKLIST_HANDLER = CommandHandler(["unblacklist", "rmblacklist"], unblacklist)
BLACKLIST_DEL_HANDLER = MessageHandler(
    (Filters.text | Filters.command | Filters.sticker | Filters.photo) & Filters.group, del_blacklist, edited_updates=True)
dispatcher.add_handler(BLACKLIST_HANDLER)
dispatcher.add_handler(ADD_BLACKLIST_HANDLER)
dispatcher.add_handler(UNBLACKLIST_HANDLER)
dispatcher.add_handler(BLACKLIST_DEL_HANDLER, group=BLACKLIST_GROUP)

__handlers__ = [BLACKLIST_HANDLER, ADD_BLACKLIST_HANDLER, UNBLACKLIST_HANDLER, (BLACKLIST_DEL_HANDLER, BLACKLIST_GROUP)]
