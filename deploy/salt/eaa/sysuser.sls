# eaa.sysuser
#
# Manages the operating system user account for EAA

{% from 'eaa/map.jinja' import eaa with context %}

eaa_sysuser_create:
  user.present:
    - name: {{ eaa.system_user.name }}
    {% if eaa.system_user.name != eaa.system_user.group_name %}
    - gid: {{ eaa.system_user.group_name }}
    {% endif %}
    - fullname: {{ eaa.system_user.full_name }}
    - system: {{ eaa.system_user.system }}
    - home: {{ eaa.system_user.home_dir }}
    - shell: {{ eaa.system_user.shell }}
    - remove_groups: False
