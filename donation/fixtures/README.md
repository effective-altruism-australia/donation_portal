To install these fixtures,

create a db: `createdb eaa-test`

checkout the commit where the fixtures were made: `git checkout 3802e79e625852bedc1547874766e7bb98c62698`

migrate up to that commit `./manage.py migrate`

load data: `./manage.py loaddata example-data`

checkout the latest dev branch `git checkout develop`

migrate to the latest schema `./manage.py migrate`

At any point you can update these fixtures by running `./manage.py dumpdata > ~/donation_portal/donation/fixtures/example-data.json`

Please also update the commit reference in this README file
