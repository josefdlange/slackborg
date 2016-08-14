def at_bot(bot_id, message_text):
    at_bot_string = "<@{}>:".format(bot_id)
    return at_bot_string in message_text

def split_at_bot(bot_id, message_text):
    at_bot_string = "<@{}>:".format(bot_id)
    return message_text.replace(at_bot_string, "").strip()
