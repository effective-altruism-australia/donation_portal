#!/bin/bash

# pinpayments is no longer being maintained and is using an old version "gettext_lazy" called "ugettext_lazy".
# This patch allows pinpayments to load for us so that we can run the server.
patch -p1 < /workspaces/donation_portal-python3/patches/pinpayments-admin.patch
patch -p1 < /workspaces/donation_portal-python3/patches/pinpayments-gettext.patch