SupportBot is a Mastodon bot built in the Polybot framework to help have one
point of contact for instance users to contact for support.

## Features

* Upon receiving a mention from an admin the bot will publicly post the message
* If a user mentions the bot, then the bot responds tagging all admins

To install dependencies:

    pip install -r requirements.txt

To configure the accounts the bot uses, just run:

    python supportbot --setup

You'll be guided through authenticating and a config file will be
automatically created.

Use the `--profile [name]` to save and use a specific state/config.

To run the bot:

    python supportbot

