# eaa.web.testing
#
# Setup specific to testing the EAA Django application

{% from 'eaa/map.jinja' import eaa with context %}

include:
  - google.chrome
  - google.chromium
