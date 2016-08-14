import re

class CommandManager(object):
    commands = []
    default_cmd = None

    def __init__(self):
        pass

    def handle_conversation(self, conversation):
        if not conversation.command:
            for command in self.commands:
                query = conversation.initial_message
                m = command.matcher.search(query)
                if m:
                    conversation.command = command
            else:
                print "No command matched."
                conversation.command = self.default_cmd or DEFAULT

        else:
            print "Existing conversation has command"
        conversation.process_next()

class Command(object):
    def __init__(self, match_string, func, multi_step, auto_close, flags=None):
        self.matcher = re.compile(match_string, flags=flags)
        self.process_conversation = func
        self.multi_step = multi_step
        self.auto_close = auto_close

def command(match_string, flags, multi_step=False, auto_close=True):
    def wrapper(func):
        CommandManager.commands.append(
            Command(match_string, func, multi_step, auto_close, flags=flags)
        )
        return func
    return wrapper

def default_command(func):
    cmd = Command('.*', func, False, True, re.IGNORECASE)
    print cmd
    CommandManager.default_cmd = cmd
    return func

def no_response(conversation):
    pass

DEFAULT = Command('.*', no_response, False, True, re.IGNORECASE)

# End
