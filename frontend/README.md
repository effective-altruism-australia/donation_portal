# A simple dependency free donation form
This form is designed to replace our react-based donation form. The benefits of this form are:

**Dependency free** - no need to regularly update dependencies.
**Easy to deploy** - just copy and paste the HTML into the WordPress site.
**Visually improved** - and matches the design of the rest of our WordPress site.
**Accessible** - follows best practices for accessibility.
**Easy to customise** - just clone this repo and change the HTML/CSS/JS as needed.
**Easy to maintain** - only a few hundred lines of simple code that beginners can grok.

## Compatibility
We try to only use features that are "Widely available" according to [Baseline](https://web.dev/baseline) to ensure compatibility with all modern browsers.

## Requirements
- NodeJS version v22.9.01

## Deployment
Note, I have changed the deployment process to avoid the need for iframes and to allow us to move beyond NodeJS version 8 (the latest version available for our current server). To deploy:

1. Run `node build.js` to concatenate the src files into a single file that will be located at `donation/templates/donation_form.html`.
2. Copy the section between the relevant comments in `donation/templates/donation_form.html` into the WordPress site.

## Development
1. Run the django server with `python manage.py runserver` (or `http-server -p 8000 ../donation/templates/` to save setting up Django).
2. Run `npm run dev` to watch files for changes and rebuild the concatenated file at `donation/templates/donation_form.html`.

