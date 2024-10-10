# A simple dependency free donation form
This form is designed to replace our react-based donation form. The goals of this form are to be:

**Dependency free** - no need to regularly update dependencies.
**Easy to deploy** - just copy and paste the HTML into the WordPress site.
**Visually improved** - and matches the design of the rest of our WordPress site.
**Accessible** - follows best practices for accessibility.
**Easy to customise** - just clone this repo and change the HTML/CSS/JS as needed.
**Easy to maintain** - only a few hundred lines of simple code that beginners can grok.

## Terminology

| Term   | Description   |
|--------|---------------|
| Default allocation | This option allocates the donation to the most effective charities (according to us), based on evidence and need. This option is selected by default in the standard form. |
| Custom allocation  | This option allows donors to allocate their donation to our various partner charities. This option can be selected in the standard form. |
| Specific charity | A specific charity is an EAA partner charity selected by visiting our  `/donate`  url with  `?charity=charity_name`  appended to the end. Specific charities are not relevant to the standard form. |

## Compatibility
We try to only use features that are "Widely available" according to [Baseline](https://web.dev/baseline) to ensure compatibility with all modern browsers.

## Requirements
- NodeJS version v22.9.01

## Deployment
__Note: the deployment process has changed to allow us to avoid iframes and to move beyond NodeJS version 8 (the latest version available for our current server). To deploy, do the following on your *local* machine:__

1. Run `node build.js` to concatenate the src files into a single file that will be located at `donation/templates/donation_form.html`.
2. Copy the section between the relevant comments in `donation/templates/donation_form.html` into the WordPress site.

## Development

### Without Django (recommended)
If you're just working on the frontend, you can avoid setting up Django.
1. Run `npx http-server -p 8000 ../donation/templates/` from the `frontend` directory to serve the files.
2. Run `npm run dev` from the `frontend` directory to watch files for changes and rebuild the concatenated file at `donation/templates/donation_form.html`.
3. Visit the page at `localhost:8000/donation_form.html` to see the form.

### With Django
1. Follow the instructions to setup and run the Django server (`python manage.py runserver`).
2. Run `npm run dev` from the `frontend` directory to watch files for changes and rebuild the concatenated file at `donation/templates/donation_form.html`.
3. Visit the page at `localhost:8000/pledge_new` to see the form.

## Testing

### With VSCode Playwright extension (recommended)
1. Run `npm install` and then `npx playwright install` to install the necessary dependencies.
2. Install the Playwright VSCode extension. This is particularly useful for creating new tests as it lets you record your actions in the browser.
3. Run the tests from VSCode's "Testing" sidebar.

### Commandline
1. Run `npm install` and then `npx playwright install` to install the necessary dependencies.
2. Run `npx playwright test` to run the tests from the command line.

## Todo:
* Test all submit cases