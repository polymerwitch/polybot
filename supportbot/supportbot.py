# -*- coding: utf-8 -*-

from html.parser import HTMLParser


from bot import Bot
from mastodon.streaming import StreamListener


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class SupportListener(StreamListener):

    def set_client(self, client):
        self.client = client
        admin_list = self.client.config.get('support_bot', 'admins')
        self.admins = admin_list.split()

    def on_notification(self, notification):
        # Do stuff with the notification
        if not self.client or notification['type'] != "mention":
            return

        if notification['status']['in_reply_to_id'] is not None:
            return

        isAdmin = notification['account']['username'] in self.admins
        if isAdmin:
            #do not relay if it is no a DM
            if notification['status']['visibility'] != "direct":
                return

            #relay toot
            body = strip_tags(notification['status']['content']) + "\n\n--@" + notification['account']['username']
            if body.startswith('@' + self.client.config.get('support_bot', 'username') + ' '):
                body = body[9:]
            self.client.get_client().status_post(body, visibility='public')
        else:
            #reply with help message
            body = "Hi, @" + notification['account']['username'] + "\n\n"
            body += "Thank you for using toot.cat! I'm just a support catbot, but I'm sure our admins will help you soon"
            body += "\n\n"
            body += "cc) "
            for admin in self.admins:
                body += "@" + admin + " "
            self.client.get_client().status_post(body, in_reply_to_id=notification['status']['id'], visibility='private')


class SupportBot(Bot):

    def main(self):
        masto_service = self.get_service_by_name("mastodon")
        listener = SupportListener()
        listener.set_client(masto_service)
        masto_service.stream_user(listener)

