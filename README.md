# SlackBorg

SlackBorg is a framework for semi-conversational, multi-step workflow Slack Bots. We're just getting started. Have an idea? File an issue. Have some code? Open a pull request.

# Concepts

SlackBorg has two main things you should care about, the `@command` decorator and the `Conversation` class.

## `@command`

`@command` is a decorator you place on a function you implement to respond to a given command. A command can be `multi_step`, which is to say that its function is called on the given conversation each time a new message comes in, until the conversation is explicitly closed. It's up to you how you handle a multi-step conversation. As you'll see, the `Conversation` object includes all the data you need to make decisions each time your handler is called. If your command is not `multi_step`, the conversation is closed immediately after your handler returns. 

### `@command` parameters:
 * `match_string`: A RegEx string that you would pass into `re.compile`. *Required*
 * `flags`: Any flags from the `re` module you would pass into `re.compile`.
 * `multi_step`: Set to `True` if your command is multi-step. Default `False`.

## `Conversation`

The `Conversation` object is the sole parameter to your command handler. Conversations are unique to a given user in a given channel. When a message comes in, the conversation manager checks to see if a conversation exists for the sending user in the channel it is posted to. If it doesn't yet exist, a Conversation object is constructed and the command manager attempts to match a command to the Conversation. If it finds one, its handler is called on the conversation. If a conversation exists, it is updated with the latest message and its command's handler called on the updated Conversation.

### `Conversation` fields:
* user_id: the sender's Slack User ID
* user_data: the sender's full Slack User Data (fetched when the Conversation is first created)
* channel_id: the Conversation's Slack Channel ID
* channel_data: the Conversation's full Slack Channel Data (fetched when the Conversation is first created)
* initial_message: the message that was responsible for the creation of this Conversation.
* messages: the rest of the messages. *Does not include `initial_message`*.
* latest_message: the most recent message.
* context: a dictionary that you can put any data you want to persist in the conversation across messages. This is where the magic is for doing a multi-step command across a conversation.

### `Conversation` methods:
* say(message): send a message to the channel.
* close(): close the conversation.

# Installation

Right now, I'd probably suggest spinning up a `virtualenv` and running `python setup.py develop` inside of it.

# Usage

Write yourself a script to declare your commands and run your bot, like so:

```
import os
import random
import re
import time

from slackborg import *

# Get Bot ID and API Token from env -- make sure to put these in your env!
BOT_ID = os.environ.get('SLACK_BOT_ID')
BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')

# Define a default response to any non-matching commands. The default default is to silently ignore the command and close the conversation.
@default_command
def default_cmd(conversation):
    conversation.say("I see, sir {}".format(conversation.user_data['profile']['first_name']))

# Define a command by a regex string, and optionally any flags you'd give the re.compile method.
@command('hello', flags=re.IGNORECASE)
def hello(conversation):
    conversation.say("Hello! I am C-3PO, human-cyborg relations!")

# By default, a command is single-step and auto-closes its conversation upon the handler returning.
# You can override this.
@command('sum', flags=re.IGNORECASE, multi_step=True)
def do_sum(c):
    print c
    operands = c.context.setdefault('operands', [])
    if len(c.messages):   
        if 'done' in c.latest_message.lower():
            c.say("The sum of {} = {}".format(
                " + ".join(str(o) for o in operands),
                str(sum(operands))
                )
            )
            c.close()
        else:
            try:
                operands.append(int(c.latest_message))
                c.say("So far: {}...".format(
                    " + ".join(str(o) for o in operands)
                ))
            except:
                c.say("That input wasn't a number. Try again!")
    else:
        c.say("Just enter your operands, one by one, and then type done when you're done!")

def main():
    borg = SlackBorg(BOT_ID, BOT_TOKEN)
    borg.run()

if __name__ == '__main__':
    main()

# End


```