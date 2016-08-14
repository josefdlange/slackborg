from utils import at_bot, split_at_bot

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
        key = '{}:{}'.format(conversation.user_id, conversation.channel_id)
        if key in self.conversations:
            del self.conversations[key]


class Conversation(object):
    def __init__(self, manager, client, initial_message):
        self._manager = manager
        self._client = client
        self._command = None
        self.user_id = initial_message['user']
        self.user_data = None 
        self.channel_id = initial_message['channel']
        self.channel_data = None
        self.initial_message = initial_message['text']
        self.messages = []
        self.context = {}

    def load_data_if_necessary(self, force=False):
        if force or self.user_data is None or self.channel_data is None:
            self.user_data = self._client.api_call('users.info', user=self.user_id)['user']
            if self.channel_id.startswith('C'):
                self.channel_data = self._client.api_call('channels.info', channel=self.channel_id)['channel']

    @property
    def latest_message(self):
        try:
            return self.messages[-1]
        except:
            return None

    def add_message(self, message):
        self.messages.append(message['text'])

    def process_next(self):
        self._command.process_conversation(self)

    def say(self, text):
        self._client.rtm_send_message(self.channel_id, text)
        if not self._command.multi_step:
            self.close()

    def close(self):
        self._manager.close_conversation(self)

# End
