import time

from slackclient import SlackClient as _SlackClient

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

    def run(self):
        if self.client.rtm_connect():
            while True:
                self.handle_messages(self.client.rtm_read())
                time.sleep(self.read_delay)
        else:
            print "Error connecting!"
            print self.bot_id
            print self.bot_token
            print self.client.__dict__
            print self.client.server

    def handle_messages(self, messages):
        for message in messages:
            print message
            if 'text' in message:
                print message['text']

# End
