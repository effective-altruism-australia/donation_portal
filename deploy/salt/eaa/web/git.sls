# eaa.web.git
#
# Manages the EAA donation portal Git repository

{% from 'eaa/map.jinja' import eaa with context %}

include:
  - eaa.sysuser
  - git

# TODO: Don't hardcode the repository definition name. - SDL
{% if not eaa.git.repositories.donation_portal.use_ssh_agent %}
  {% if eaa.git.repositories.donation_portal.private_key_file %}
    {% set ssh_key_path = eaa.git.repositories.donation_portal.private_key_file %}
  {% else %}
    {% set ssh_key_path = eaa.system_user.home_dir ~ '/.ssh/id_rsa' %}
  {% endif %}

{% if eaa.git.repositories.donation_portal.private_key %}
eaa_web_git_private_key:
  file.managed:
    - name: {{ ssh_key_path }}
    - contents_pillar: eaa:git:repositories:donation_portal:private_key
    - allow_empty: False
    - user: {{ eaa.system_user.name }}
    - group: {{ eaa.system_user.group_name }}
    - mode: 600
    - makedirs: True
    - dir_mode: 700
    - require:
      - sls: eaa.sysuser
{% else %}
eaa_web_git_private_key:
  file.exists:
    - name: {{ ssh_key_path }}
{% endif %}

{% endif %}
eaa_web_git_known_hosts:
  ssh_known_hosts.present:
    - name: {{ eaa.git.repositories.donation_portal.host }}
    - fingerprint: {{ eaa.git.repositories.donation_portal.fingerprint }}
    {# TODO: Update to use SHA256 hash. - SDL #}
    - fingerprint_hash_type: md5
    - user: {{ eaa.system_user.name }}
    - require:
      - sls: eaa.sysuser

{% if false %}
eaa_web_git_repo_update:
  git.latest:
    - name: {{ eaa.git.repositories.donation_portal.source }}
    - target: {{ eaa.git.repositories.donation_portal.target }}
    - rev: {{ eaa.git.repositories.donation_portal.remote_ref }}
    - branch: {{ eaa.git.repositories.donation_portal.local_branch }}
    - force_checkout: {{ eaa.git.settings.force_checkout }}
    - force_clone: {{ eaa.git.settings.force_clone }}
    - force_fetch: {{ eaa.git.settings.force_fetch }}
    - force_reset: {{ eaa.git.settings.force_reset }}
    - submodules: {{ eaa.git.settings.submodules }}
    {% if not eaa.git.repositories.donation_portal.use_ssh_agent %}
    - identity: {{ ssh_key_path }}
    {% endif %}
    - user: {{ eaa.system_user.name }}
    - require:
      - sls: git.install
      {% if not eaa.git.repositories.donation_portal.use_ssh_agent %}
      - file: eaa_web_git_private_key
      {% endif %}
      - ssh_known_hosts: eaa_web_git_known_hosts
{% endif %}