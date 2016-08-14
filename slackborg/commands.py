import re

class CommandManager(object):
    commands = []
    default_cmd = None

    def __init__(self):
        pass

    def handle_conversation(self, conversation):
        if not conversation._command:
            for command in self.commands:
                query = conversation.initial_message
                m = command.matcher.search(query)
                if m:
                    conversation._command = command
                break
            else:
                print "No command matched."
                conversation._command = self.default_cmd or DEFAULT

        else:
            print "Existing conversation has command"
        conversation.process_next()

class Command(object):
    def __init__(self, match_string, func, multi_step, flags=None):
        self.matcher = re.compile(match_string, flags=flags)
        self.process_conversation = func
        self.multi_step = multi_step

def command(match_string, flags=None, multi_step=False):
    def wrapper(func):
        CommandManager.commands.append(
            Command(match_string, func, multi_step, flags=flags)
        )
        return func
    return wrapper

def default_command(func):
    cmd = Command('.*', func, False, re.IGNORECASE)
    print cmd
    CommandManager.default_cmd = cmd
    return func

def no_response(conversation):
    pass

DEFAULT = Command('.*', no_response, False, re.IGNORECASE)

# End
