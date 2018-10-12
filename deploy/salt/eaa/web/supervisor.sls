# eaa.web.supervisor
#
# Manages the EAA donation portal Supervisor configuration

{% from 'eaa/map.jinja' import eaa with context %}

{% extends 'supervisor/includes.sls' %}

{% block extend_supervisor_state_dict %}
{% do supervisor.included_confs.update({
  'donations': {
    'enabled': true,
    'always_restart': true,
    'conf_template': 'salt://eaa/web/templates/supervisor.conf.jinja',
    'conf_settings': {
      'directory': eaa.git.repositories.donation_portal.target,
      'user_name': eaa.system_user.name,
      'venv_path': eaa.django.venv_path,
    },
  },
}) %}
{% endblock %}
