# A simple dependency free donation form

The goals of this form are to be:

**Dependency free** - no need to regularly update dependencies.
**Easy to deploy** - just copy and paste the HTML into the WordPress site.
**Accessible** - follows best practices for accessibility.
**Easy to customise** - just clone this repo and change the HTML/CSS/JS as needed.
**Easy to maintain** - only a few hundred lines of simple code that beginners can grok.

## Allocation terminology
| Term   | Description   |
|--------|---------------|
| Most effective (default) | This option allocates the donation to the most effective charities (according to us), based on evidence and need. This option is selected by default in the standard form. |
| Specific charity (or charities)  | This option allows donors to allocate their donation to our various partner charities. This option can be selected in the standard form. |
| Direct link charity | A direct link charity is an EAA partner charity selected by visiting our  `/donate`  url with  `?charity=charity_name`  appended to the end. Direct link charities are not relevant to the standard form. |

## Compatibility
We try to only use features that are "Widely available" according to [Baseline](https://web.dev/baseline) to ensure compatibility with all modern browsers.

## Testing
TODO