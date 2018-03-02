# Donation portal pledge app in ReactJS

This is a *work in progress* and is not complete.

The app was created from https://github.com/facebook/create-react-app

Serve locally in dev with:

    cd donation_portal/react
    npm start

You'll then load the site here:

    http://localhost:3000/

For using within Django (dev or prod), generate the `build` directory of static files:

    npm run build

That set of files is served by Django in development only as `/pledge2/'.
If Django is running as normal, e.g.:

    cd donation_portal  # root dir, not react
    PYTHONPATH=donation_portal ./manage.py runserver

then the original donation portal site will be visible at:

    http://localhost:8000/pledge

and the react app will be mounted at:

    http://localhost:8000/pledge2


## TODOs:

Look through all files under react/**/* for "TODO".

Major:
- Needs more complete integration with Django, e.g.:
   - data (charities and referrals) 
   - css. (CSS currently copied into react, which is not ideal.)

- Card doesn't work yet. Not hard to complete it some parts of this, but
  there was hesitation around it not doing the validation exactly like the
  existing jQuery way does it.

  A thought was to integrate the existing jQuery forms+logic. Pros and cons.
  This article has some notes:
  http://tech.oyster.com/using-react-and-jquery-together/

- Neither Pin nor Django is called via API yet. These things would be relatively
  straightforward now that the app is integrated with Django, and even better
  if it is better integrated.

- Consider better integration with webpack+config per draftable.

- Some failure cases not fully implemented. Again not too big a task.

- When monthly donation is selected, the "card vs bank" section should change.


