# eaa.envs.dev
#
# Meta-state for an EAA development environment

{% from 'eaa/map.jinja' import eaa with context %}

include:
  - redis
  - eaa.web
  - eaa.db

{% if eaa.roles.web.install_supervisor %}
extend:
  supervisor_include_donations_create:
    file:
      - require:
        - sls: eaa.db.migrate
        - sls: redis.service
{% endif %}
