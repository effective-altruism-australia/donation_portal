# eaa.web.django
#
# Manages the EAA donation portal Django application

{% from 'eaa/map.jinja' import eaa with context %}

include:
  - eaa.sysuser
  - python2
  - postgresql.client

eaa_web_django_venv_create:
  virtualenv.managed:
    - name: {{ eaa.django.venv_path }}
    - user: {{ eaa.system_user.name }}
    - require:
      - sls: eaa.sysuser
      - sls: python2.lang
      - sls: python2.pip
      - sls: python2.packages

eaa_web_django_deps_apt:
  cmd.run:
    - name: apt-get --quiet --assume-yes --option 'Dpkg::Options::=--force-confold' --option 'Dpkg::Options::=--force-confdef' install $(cat "{{ eaa.git.repositories.donation_portal.target }}/{{ eaa.django.apt_file }}")

eaa_web_django_deps_pip:
  pip.installed:
    - requirements: {{ eaa.git.repositories.donation_portal.target }}/{{ eaa.django.pip_file }}
    - bin_env: {{ eaa.django.venv_path }}
    - env_vars:
        PIP_DISABLE_PIP_VERSION_CHECK: 'true'
    - user: {{ eaa.system_user.name }}
    - require:
      - virtualenv: eaa_web_django_venv_create
      - sls: postgresql.client.install

eaa_web_django_config:
  file.managed:
    - name: {{ eaa.git.repositories.donation_portal.target }}/{{ eaa.django.conf_file }}
    - source: {{ eaa.django.conf_template }}
    - template: jinja
    - user: {{ eaa.system_user.name }}
    - group: {{ eaa.system_user.group_name }}
    - mode: 640
    - context:
        config: {{ eaa | json }}
    - require:
      - sls: eaa.sysuser


{# TODO move this into separated frontend state #}
eaa_web_django_frontend_npm:
  npm.bootstrap:
    - name: {{ eaa.git.repositories.donation_portal.target }}/react
    - user: {{ eaa.system_user.name }}
    - require:
      - sls: eaa.sysuser


eaa_web_django_frontend_webpack:
  cmd.run:
    - name: npm run build
    - cwd: {{ eaa.git.repositories.donation_portal.target }}/react
    {# Added as a precaution. See the comment for the Combiner. - SDL #}
    - reset_system_locale: False
    - runas: {{ eaa.system_user.name }}
    - env:
      {% if eaa.django.default_env == 'prod' %}
      - NODE_ENV: 'production'
      {% else %}
      - NODE_ENV: 'development'
      {% endif %}


eaa_web_django_collectstatic:
  cmd.run:
    - name: {{ eaa.django.venv_path }}/bin/python {{ eaa.git.repositories.donation_portal.target }}/manage.py collectstatic --verbosity 0 --no-color --noinput
    - cwd: {{ eaa.git.repositories.donation_portal.target }}
    - runas: {{ eaa.system_user.name }}
    - env:
      - WORKON_HOME: {{ eaa.django.venv_path }}
    - require:
      - pip: eaa_web_django_deps_pip
      - file: eaa_web_django_config

# http://unix.stackexchange.com/questions/192642/wkhtmltopdf-qxcbconnection-could-not-connect-to-display
# https://github.com/JazzCore/python-pdfkit/wiki/Using-wkhtmltopdf-without-X-server
eaa_web_django_wkhtmltopdf_wrapper_1:
  file.managed:
    - name: /usr/bin/wkhtmltopdf.sh
    - source: salt://eaa/web/templates/wkhtmltopdf.sh
    - allow_empty: False
    - mode: 755
    - require:
      - sls: eaa.sysuser

eaa_web_django_wkhtmltopdf_wrapper_2:
  file.symlink:
    - name: /usr/local/bin/wkhtmltopdf
    - target: /usr/bin/wkhtmltopdf.sh
    - require:
      - file: eaa_web_django_wkhtmltopdf_wrapper_1
