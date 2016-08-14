class ConversationManager(object):
    def __init__(self, client):
        self.client = client
        self.conversations = {}

    def process_message(self, message):
        user = message.get('user')
        channel = message.get('channel')
        key = '{}:{}'.format(user, channel)
        conversation = None

        if user:
            conversation = self.conversations.get(key)
            if conversation:
                print "Existing convesation"
                conversation.add_message(message)
            else:
                print "New conversation"
                conversation = Conversation(self, self.client, message)
                self.conversations[key] = conversation
        else:
            print "No user?"

        return conversation

    def close_conversation(self, conversation):
        key = '{}:{}'.format(conversation.user, conversation.channel)
        if key in self.conversations:
            del self.conversations[key]


class Conversation(object):
    def __init__(self, manager, client, initial_message):
        self.manager = manager
        self.client = client
        self.user = initial_message['user']
        self.user_data = self.client.api_call('users.info', user=self.user)['user']
        self.channel = initial_message['channel']
        self.command = None
        self.initial_message = initial_message['text']
        self.messages = []
        self.context = {}

    @property
    def latest_message(self):
        try:
            return self.messages[-1]
        except:
            return None

    def add_message(self, message):
        self.messages.append(message['text'])

    def process_next(self):
        self.command.process_conversation(self)

    def say(self, text):
        self.client.rtm_send_message(self.channel, text)
        if not self.command.multi_step and self.command.auto_close:
            self.close()

    def close(self):
        self.manager.close_conversation(self)

# End
