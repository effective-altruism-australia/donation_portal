Payment backend for Effective Altruism Australia.

Configuration is via [salt](https://docs.saltstack.com/en/latest/) but we haven't open-sourced the salt pillar and
states yet. Currently you won't be able to run this without salt either as settings are missing, but we'll change that
ASAP.

How to get a dev instance up and running:

1. Wait a month or so.
2. Check back here and follow the instructions.


Note: On Ubuntu 14.04, I have to work around [this issue](https://github.com/saltstack/salt/issues/19532) in salt. The
workaround is to grant rw permissions on /tmp/usr/0 to the user you're installing the app for.
