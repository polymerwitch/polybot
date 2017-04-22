# -*- coding: utf-8 -*-

from .bot import Bot
from .mastodon.streaming import StreamListener


ADMINS = [
    "polymerwitch",
    "cyrinsong",
    "wavebeem",
    "ashkitten"
]

class SupportListener(StreamListener):

    def set_client(self, client):
        self.client = client

    def on_notification(self, notification):
        """Notification:
        { id: <The notification ID>,
          type:	<One of: "mention", "reblog", "favourite", "follow">,
          created_at: <The time the notification was created>,
          account: <The Account sending the notification to the user>,
          status: <The Status associated with the notification, if applicable>
        }"""

        # Do stuff with the notification
        if not self.client or notification.type != "mention":
            return

        isAdmin = notification.account.username in ADMINS
        if isAdmin:
            #relay toot
            body = notification.status.content + "\n\n--@" + notification.account.username
            self.client.get_client().status_post(body, visibility='public')
        else:
            #reply with help message
            body = "Hi, @" + notification.account.username + "\n\n"
            body += "Thank you for using toot.cat! I'm just a support catbot, but I'm sure our admins will help you soon"
            body += "\n\n"
            body += "cc) @polymerwitch @cyrinsong @wavebeem @ashkitten"
            self.client.get_client().status_post(body, in_reply_to_id=notification.status.id, visibility='private')


class SupportBot(Bot):

    def main(self):
        masto_service = self.get_service_by_name("mastodon")
        listener = SupportListener()
        listener.set_client(masto_service)
        masto_service.stream_user(listener)
