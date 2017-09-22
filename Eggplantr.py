import argparse
import time
from slackclient import SlackClient


class Eggplanter:
    def __init__(self, token, users, rate):
        self.users = users
        self.client = SlackClient(token)
        self.rate = rate
        if self.rate is None:
            self.rate = .5

    def listen(self):
        self.client.rtm_connect()

        while True:
            response = self.client.rtm_read()
            for i in response:
                if 'user' in i and i.get('user') in self.users:
                    print(self._send_message(i.get('channel'), i.get('ts')))

            time.sleep(self.rate)

    def _send_message(self, channel, timestamp):
        return self.client.api_call(
            "reactions.add",
            channel=channel,
            name="eggplant",
            timestamp=timestamp
        )


parser = argparse.ArgumentParser(description='Eggplant some hoes')
parser.add_argument('-t', required=True, type=str, help='Your slack legacy token')
parser.add_argument('-u', required=True, type=str, help='Users to eggplant with ease (comma separated)')
parser.add_argument('--rate', type=float, help='Rate of eggplantation')

args = parser.parse_args()

users = [x.strip() for x in args.u.split(',')]
eggplanter = Eggplanter(args.t, users, args.rate)

eggplanter.listen()
