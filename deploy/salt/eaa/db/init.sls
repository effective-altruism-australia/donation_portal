# eaa.db
#
# Meta-state for a complete installation of an EAA donation portal database server

include:
  - postgresql.server
  - eaa.web.git
  - eaa.web.django
  - eaa.db.migrate

extend:
  eaa_db_migrate:
    cmd:
      - require:
        - sls: postgresql.server.databases
        - sls: eaa.web.git
        - sls: eaa.web.django
