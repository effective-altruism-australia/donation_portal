# eaa.web
#
# Meta-state for a complete installation of the EAA donation portal

{% from 'eaa/map.jinja' import eaa with context %}

include:
  - eaa.web.git
  - eaa.web.django
  {% if eaa.roles.web.install_supervisor %}
  - eaa.web.supervisor
  {% endif %}
  {% if eaa.roles.web.install_nginx %}
  - nginx
  {% endif %}

extend:
  eaa_web_django_venv_create:
    virtualenv:
      - require:
        - sls: eaa.web.git
  eaa_web_django_deps_apt:
    cmd:
      - require:
        - sls: eaa.web.git
  eaa_web_django_config:
    file:
      - require:
        - sls: eaa.web.git
  {% if eaa.roles.web.install_supervisor %}
  supervisor_include_donations_create:
    file:
      - require:
        - sls: eaa.web.django
  {% endif %}
