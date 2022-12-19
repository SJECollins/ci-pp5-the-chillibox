# The Chillibox
# Testing

Below is the testing performed for the project. Wherever possible, screenshots were taken to document the testing.


## Lighthouse

The site was tested using Lighthouse in Chrome DevTools to check performance, accessibiltiy, best practices and SEO. Where possible, errors and warnings were corrected so all final results were a minimum of 90. The final testing on Lighthouse was run on incognito mode. The results are below.

<details>
<summary>Lighthouse Index</summary>

![Index](readme-docs/testing/lighthouse_index.webp)
</details>

<details>
<summary>Lighthouse FAQ</summary>

![FAQ](readme-docs/testing/lighthouse_faq.webp)
</details>

<details>
<summary>Lighthouse Privacy Policy</summary>

![Privacy Policy](readme-docs/testing/lighthouse_privacy.webp)
</details>

<details>
<summary>Lighthouse Contact Us</summary>

![Contact Us](readme-docs/testing/lighthouse_contact.webp)
</details>

<details>
<summary>Lighthouse Recipe List</summary>

![Recipe List](readme-docs/testing/lighthouse_recipe_list.webp)
</details>

<details>
<summary>Lighthouse Recipe Page</summary>

![Recipe Page](readme-docs/testing/lighthouse_recipe.webp)
</details>

<details>
<summary>Lighthouse Latest Products</summary>

![Latest](readme-docs/testing/lighthouse_latest.webp)
</details>

<details>
<summary>Lighthouse Category</summary>

![Category](readme-docs/testing/lighthouse_category.webp)
</details>

<details>
<summary>Lighthouse Product Page</summary>

![Product](readme-docs/testing/lighthouse_product.webp)
</details>

<details>
<summary>Lighthouse Cart</summary>

![Cart](readme-docs/testing/lighthouse_cart.webp)
</details>

<details>
<summary>Lighthouse Checkout</summary>

![Checkout](readme-docs/testing/lighthouse_checkout.webp)
</details>

<details>
<summary>Lighthouse Checkout Success</summary>

![Checkout Success](readme-docs/testing/lighthouse_checkout_success.webp)
</details>

<details>
<summary>Lighthouse Register</summary>

![Register](readme-docs/testing/lighthouse_register.webp)
</details>

<details>
<summary>Lighthouse Login</summary>

![Login](readme-docs/testing/lighthouse_login.webp)
</details>

<details>
<summary>Lighthouse User Profile</summary>

![Profile](readme-docs/testing/lighthouse_profile.webp)
</details>

<details>
<summary>Lighthouse Profile - User Reviews</summary>

![Profile Reviews](readme-docs/testing/lighthouse_profile_reviews.webp)
</details>

<details>
<summary>Lighthouse Profile - User Recipes</summary>

![Profile Recipes](readme-docs/testing/lighthouse_profile_recipes.webp)
</details>

<details>
<summary>Lighthouse Management Dashboard</summary>

![Management](readme-docs/testing/lighthouse_management.webp)
</details>

<details>
<summary>Lighthouse Management - User Reviews</summary>

![Management Reviews](readme-docs/testing/lighthouse_management_reviews.webp)
</details>

<details>
<summary>Lighthouse Management - Recipes List</summary>

![Management Recipes](readme-docs/testing/lighthouse_management_recipe_list.webp)
</details>

<details>
<summary>Lighthouse Management - Submitted Recipes</summary>

![Management Submitted Recipes](readme-docs/testing/lighthouse_management_submitted.webp)
</details>

<details>
<summary>Lighthouse Management - Recipe Comments</summary>

![Comments](readme-docs/testing/lighthouse_management_comments.webp)
</details>


## HTML Validator

HTML was tested through validation by copying the source code of pages into the direct input on [W3C HTML Validator](https://validator.w3.org/#validate_by_input).
Any errors found where then corrected to meet the validator's standards. Below are the results after templates were edited to meet the requirements.

<details>
<summary>Index</summary>

![Index](readme-docs/testing/validate_index.webp)
</details>

<details>
<summary>FAQ</summary>

![FAQ](readme-docs/testing/validate_faq.webp)
</details>

<details>
<summary>Privacy Policy</summary>

![Privacy Policy](readme-docs/testing/validate_privacy.webp)
</details>

<details>
<summary>Latest Products</summary>

![Latest Products](readme-docs/testing/validate_latest.webp)
</details>

<details>
<summary>Category</summary>

![Category](readme-docs/testing/validate_category.webp)
</details>

<details>
<summary>Product</summary>

![Product](readme-docs/testing/validate_product.webp)
</details>

<details>
<summary>Profile</summary>

![Profile](readme-docs/testing/validate_profile.webp)
</details>

<details>
<summary>Profile Reviews</summary>

![Profile Reviews](readme-docs/testing/validate_profile_reviews.webp)
</details>

<details>
<summary>Profile Recipes</summary>

![Profile Recipes](readme-docs/testing/validate_profile_recipe.webp)
</details>

<details>
<summary>Management Dashboard</summary>

![Management Dashboard](readme-docs/testing/validate_mgmt_products.webp)
</details>

<details>
<summary>Management Reviews</summary>

![Management Reviews](readme-docs/testing/validate_mgmt_reviews.webp)
</details>

<details>
<summary>Management Recipes</summary>

![Management Recipes](readme-docs/testing/validate_mgmt_recipes.webp)
</details>

<details>
<summary>Management Comments</summary>

![Management Comments](readme-docs/testing/validate_mgmt_comments.webp)
</details>

<details>
<summary>Management Submitted Recipes</summary>

![Submitted Recipes](readme-docs/testing/validate_mgmt_submitted.webp)
</details>


## CSS Validator

No errors were found in the CSS was manually copied into the [W3C CSS Validatory](https://jigsaw.w3.org/css-validator/validator)
![CSS Validation](readme-docs/testing/validate_css.webp)

<p>
    <a href="http://jigsaw.w3.org/css-validator/check/referer">
        <img style="border:0;width:88px;height:31px"
            src="http://jigsaw.w3.org/css-validator/images/vcss-blue"
            alt="Valid CSS!" />
    </a>
</p>


## JavaScript Testing

JavaScript validation was performed using [JSHint](https://jshint.com/) to check quality of the JS scripts. During validation the code "/* jshint -W033 *\/" to surpress warnings related to "missing semicolons", and "/\* globals exampleVariable */" was used to surpress warnings related to global variables. There remained two warnings related to "unused variables" in the script for the Google Map.

<details>
<summary>JSHint Modal</summary>

![Modal](readme-docs/testing/jshint_modal.webp)
</details>

<details>
<summary>JSHint Product Page Add To Cart</summary>

![Product](readme-docs/testing/jshint_product_page.webp)
</details>

<details>
<summary>JSHint Cart Adjust Quantity</summary>

![Cart](readme-docs/testing/jshint_cart_quantity.webp)
</details>

<details>
<summary>JSHint Checkout and Stripe</summary>

![Stripe](readme-docs/testing/jshint_stripe.webp)
</details>

<details>
<summary>JSHint EmailJS</summary>

![EmailJS](readme-docs/testing/jshint_emailjs.webp)
</details>

<details>
<summary>JSHint Google Map</summary>

![Map](readme-docs/testing/jshint_gmap.webp)
</details>


## Python Testing

Python validation for PEP8 compliance was performed using [pycodestyle](https://pycodestyle.pycqa.org/en/latest/index.html) to check linting errors. Where appropriate, in a small number of cases "# noqa" was used, especially for "errors" in Django generated files. 

[CI Python Linter](https://pep8ci.herokuapp.com/) was used to double check some pages by copy and pasting code, as a back up to confirm there were no linting issues.

<details>
<summary>Python Problems</summary>

![Problems](readme-docs/testing/python_validation.webp)
</details>


## Automated Testing

Automated testig was performed using Django's testing tools and measured using coverage. The pages of the coverage report are below.

<details>
<summary>Coverage Pg1</summary>

![Coverage 1](readme-docs/testing/coverage_one.webp)
</details>

<details>
<summary>Coverage Pg2</summary>

![Coverage 2](readme-docs/testing/coverage_two.webp)
</details>

<details>
<summary>Coverage Pg3</summary>

![Coverage 3](readme-docs/testing/coverage_three.webp)
</details>


## Manual Testing
Below the steps for manual testing of the site have been arranged into tables. User stories are matched to the manual tests which demonstrate their fulfillment in the User Story column. The User Story numbers can be found on the project board under their Epics or in the main README file under Agile Methodology - Epics & User Stories.

The fulfillment of acceptance criteria for user stories is not the focus of the manual testing as this was documented when features were implemented in comments on each user story on the project board.

<details>
<summary>Manual Testing for User Authentication</summary>

![User Authentication](readme-docs/testing/testing_allauth.webp)
</details>

<details>
<summary>Manual Testing for User Profiles</summary>

![User Profiles](readme-docs/testing/testing_profiles.webp)
</details>

<details>
<summary>Manual Testing for Home</summary>

![Home](readme-docs/testing/testing_home.webp)
</details>

<details>
<summary>Manual Testing for Products</summary>

![Products](readme-docs/testing/testing_products.webp)
</details>

<details>
<summary>Manual Testing for Cart</summary>

![Cart](readme-docs/testing/testing_cart.webp)
</details>

<details>
<summary>Manual Testing for Checkout</summary>

![Checkout](readme-docs/testing/testing_checkout.webp)
</details>

<details>
<summary>Manual Testing for Management Pt1</summary>

![Managment Pt1](readme-docs/testing/testing_management.webp)
</details>

<details>
<summary>Manual Testing for Management Pt2</summary>

![Management Pt2](readme-docs/testing/testing_management_2.webp)
</details>

<details>
<summary>Manual Testing for Recipes</summary>

![Recipes](readme-docs/testing/testing_recipes.webp)
</details>


## Browser Compatibility

The website was tested on:

- Chrome Version 108.0.5359.125
- Firefox Version 108.0
- Edge Version 108.0.1462.54
- Safari iOS Version 16.1.1


## Bugs
### Fixed Bugs

- Comment options:
    - **Issue**: "Edit" and "Delete" options for comment available for everyone
    - **Description**: On launch, the "Edit" and "Delete" options for every comment was available for everyone. This was due to a error in the if statement of the template checking the user. It check if the user matched the "comment.commenter" when it should have been checking against "comment.user".
    - **Fix**: Edit template to check for "comment.user"

- Accessing profile:
    - **Issue**: Unable to access user profiles
    - **Description**: Following changes to the order model when integrating Stripe webshooks, users were unable to access their profiles and user accounts were unable to be altered in admin. This was due to migrations not being done on the live site.
    - **Fix**: Migrated tables on the live site.

- Stock:
    - **Issue**: Users able to add more items than in stock
    - **Description**: When users added the maximum amount of stock to their cart, they were able to reload the page and even with 0 quantity of a product variant in stock they could add to their cart (but only 1 item). This was due to the "Add To Cart" button not being disabled when a variant was selected.
    - **Fix**: Edit script to check for and disable "Add To Cart" when stock is 0

### Known Bugs
There are currently no known bugs.