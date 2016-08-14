import time

from slackclient import SlackClient as _SlackClient
from conversations import ConversationManager
from commands import CommandManager

class SlackClient(_SlackClient):
    # I'm not sure if it's my local environment, but the Slack Client
    # swallows an error where the websocket client beneath can't find
    # the root CA file. 
    def __init__(self, *args, **kwargs):
        super(SlackClient, self).__init__(*args, **kwargs)

        def patched_connect_slack_websocket(self, ws_url):
            try:
                import websocket
                import ssl
                sslopt_ca_certs = {}
                ssl_defaults = ssl.get_default_verify_paths()
                if ssl_defaults is not None:
                    sslopt_ca_certs = {'ca_certs': ssl_defaults.cafile}
                self.websocket = websocket.create_connection(ws_url, sslopt=sslopt_ca_certs)
            except Exception as e:
                print e
                print 'Failed WebSocket Connection.'
        self.server.__class__.connect_slack_websocket = patched_connect_slack_websocket



class SlackBorg(object):
    def __init__(self, bot_id, bot_token, **kwargs):
        self.bot_id = bot_id
        self.bot_token = bot_token
        self.client = SlackClient(bot_token)
        self.read_delay = kwargs.get('read_delay', 1)

        self.conversation_manager = ConversationManager(self.client)
        self.command_manager = CommandManager()

        self.triggers = kwargs.pop('triggers', []) + ["<@{}>:".format(self.bot_id)]

    def run(self):
        if self.client.rtm_connect():
            while True:
                self.handle_messages(self.client.rtm_read())
                time.sleep(self.read_delay)
        else:
            print "Error connecting to Slack RTM API!"

    def handle_messages(self, messages):
        for message in messages:
            print message
            if 'message' in message.get('type', '') and 'text' in message and 'user' in message:
                conversation = self.conversation_manager.process_message(message)
                if conversation.user_id == self.bot_id:
                    print "Message from myself. Ignoring!"
                    conversation.close()
                elif conversation._command or ((self.does_trigger(message['text']) or self.is_dm(message['channel']))):
                    conversation.load_data_if_necessary()
                    self.command_manager.handle_conversation(conversation)
                else:
                    print "I don't care about this conversation. Ignoring!"
                    conversation.close()

    def is_dm(self, channel_id):
        channels = self.client.api_call('im.list').get('ims', [])
        return any([c['id'] == channel_id for c in channels])

    def does_trigger(self, message_text):
        return any([t in message_text for t in self.triggers])

# End
