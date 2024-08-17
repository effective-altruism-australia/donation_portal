# A simple dependency free donation form
This form is designed to replace our react-based donation form. The benefits of this form are:

**Dependency free** - no need to regularly update dependencies to keep the code maintainable.
**Easy to deploy** - just copy and paste the HTML into the WordPress site.
**Visually improved** - and matches the design of the rest of our WordPress site.
**Easy to customise** - just clone this repo and change the HTML/CSS/JS as needed.
**Easy to maintain** - only a few hundred lines of simple code that beginners can grok.

## Requirements
- NodeJS version 8+
 
## Deployment
1. Run `node build.js` to concatenate the src files into a single file at `./donation/templates/donation_form.html`.
2. Copy the section between the relevant comments in `./donation/templates/donation_form.html` into the WordPress site.