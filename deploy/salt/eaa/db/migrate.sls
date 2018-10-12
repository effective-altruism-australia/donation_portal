# eaa.db.migrate
#
# Manages the EAA donation portal database migrations

{% from 'eaa/map.jinja' import eaa with context %}
{% from 'postgresql/map.jinja' import postgresql with context %}

eaa_db_migrate:
  cmd.run:
    - name: {{ eaa.django.venv_path }}/bin/python {{ eaa.git.repositories.donation_portal.target }}/manage.py migrate --noinput --no-color
    - cwd: {{ eaa.git.repositories.donation_portal.target }}
    - runas: {{ eaa.system_user.name }}
    - env:
      - WORKON_HOME: {{ eaa.django.venv_path }}
