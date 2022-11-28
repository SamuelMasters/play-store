# Play.com - eCommerce Store


**Developer: Samuel Masters**

💻 [Visit live website](https://play-store-samuel-masters.herokuapp.com/)

## Table of Contents
  - [About](#about)
  - [User Goals](#user-goals)
  - [Site Owner Goals](#site-owner-goals)
  - [User Experience](#user-experience)
  - [User Stories](#user-stories)
  - [Design](#design)
    - [Colours](#colours)
    - [Fonts](#fonts)
    - [Structure](#structure)
      - [Website pages](#website-pages)
      - [Database](#database)
    - [Wireframes](#wireframes)
  - [Technologies Used](#technologies-used)
  - [Features](#features)
  - [Validation](#validation)
  - [Testing](#testing)
  - [Bugs](#bugs)
  - [Configuration](#configuration)
    - [Heroku Deployment](#heroku-deployment)
  - [Credits](#credits)

### About

This project, "play-store", is an eCommerce web application where users can browse video game and board game products, add them to a basket, and purchase them via Stripe payments. 

### User Goals

- PLACEHOLDER_TEXT

### Site Owner Goals

- PLACEHOLDER_TEXT



## User Experience

### Target Audience

- PLACEHOLDER_TEXT

### User Requirements and Expectations

- PLACEHOLDER_TEXT

##### Back to [top](#table-of-contents)


## User Stories

User stories were created at project start and were arranged planned out using Lucidchart...

### Users

1.	As a user, I can ....


### Site Owner
2.	As an admin, I can ...


##### Back to [top](#table-of-contents)


## Design

### Colours

The colour scheme uses ...

### Fonts

Google Fonts was used to provide the font for the website. [PLACEHOLDER_TEXT](#) was chosen as the universal font for the page, and was chosen for...

### Structure

#### Website Pages

The website uses different templates / pages to comprise it's structure.

The top of each page features a PLACEHOLDER_TEXT navbar...

The bottom of each page features PLACEHOLDER_TEXT.

- The website consists of the following sections:
  - PLACEHOLDER_TEXT

#### Database

- Data for this project is stored is an ElephantSQL database.

The following models were setup for this project:

##### User Model
- Django-allauth provided a user model that was used in this project. The model was not customised.

##### Product Model
- This model contains information about each individual post created on the site.
- It contains the following fields:
  - PLACEHOLDER_TEXT

##### Category Model
- This model contains information about different categories to which posts can be assigned.
- It contains the following fields:
  - name
  - friendly_name

##### Order Model
- This model contains information about comments which can be left on posts by users.
- It contains the following fields:
  - post
  - name
  - body
  - created_on
  - approved

### Wireframes

<details><summary>PC / Laptop or Desktop</summary>
<img src="">
</details>
<details><summary>Tablet</summary>
<img src="">
</details>
<details><summary>Mobile</summary>
<img src="">
</details>
<details><summary>Model Planning</summary>
<img src="">
</details>
<details><summary>User Stories</summary>
<img src="">
</details>

## Technologies Used

### Languages & Frameworks

- HTML
- CSS
- Javascript
- Python
- Django


### Libraries & Tools

- [PLACEHOLDER_TEXT]() was used to PLACEHOLDER_TEXT

##### Back to [top](#table-of-contents)

--- 

## Features

### Navigation Bar
- Consistent across all pages, the navigation bar is setup in the base.html template, which all other templates extend.
- Contains links to Home, and:
  - If the user is authenticated:
      - PLACEHOLDER_TEXT
  - If the user is not authenticated:
      - PLACEHOLDER_TEXT


### Home
- PLACEHOLDER_TEXT

<details>

![Home](docs/readme/home.png)
</details>

### Post Detail
- PLACEHOLDER_TEXT

### Authentication (Login, Logout, Register)
- PLACEHOLDER_TEXT

<details>

![Edit](docs/readme/edit.png)
</details>

#### Sign-in
<details>

![Sign-in](docs/readme/sign-in.png)
</details>

#### Sign-out
<details>

![Sign-out](docs/readme/sign-out.png)
</details>

#### Sign-up
<details>

![Sign-up](docs/readme/sign-up.png)
</details>

### Footer
- Basic footer, setup in the base.html template, and appears at the bottom of each page. 

<details>

![Footer](docs/readme/footer.png)
</details>

### Feedback messages
- The user receives a pop-up message when...

<details>

![Messages](docs/readme/message.png)
</details>

##### Back to [top](#table-of-contents)

---

## Validation

The [W3C Validator](https://validator.w3.org/nu/) was used for validation of the HTML files in this project.
<details><summary>Home</summary>
<img src="docs/validators/index.html validator result.png">
</details>

<details><summary>Home (Filtered)</summary>
<img src="docs/validators/index (filtered).png">
</details>

<details><summary>Post Detail</summary>
<img src="docs/validators/post_detail.html validator result.png">
</details>

<details><summary>Sign-in</summary>
<img src="docs/validators/login.html validator result.png">
</details>

<details><summary>Sign-out</summary>
<img src="docs/validators/logout.html validator result.png">
</details>

<details><summary>Sign-up</summary>
<img src="docs/validators/signup.html validator result.png">
</details>

### CSS Validation
The [Jigsaw CSS validator](https://jigsaw.w3.org/css-validator/) was used for validation of the CSS files in this project.

<details>
<img src="docs/validators/style.css validator result.png">
</details>

### JavaScript Validation
[JSHint](https://jshint.com/) was used for validation of the JS files in this project. The validation was done via raw input, meaning the contents of script.js were copied into the validator.

<details>
<img src="">
</details>

### PEP8 Validation
[PEP8 Online](http://pep8online.com/) was used for validation of the Python files in this project.

<details><summary>settings.py</summary>
<img src="">
</details>



##### Back to [top](#table-of-contents)

---

## Testing

The project was tested throughout development, manually. Automated tests were not utilised for this project.

##### Back to [top](#table-of-contents)

---

## Bugs

1. UNRESOLVED - 

##### Back to [top](#table-of-contents)

---

## Configuration

### Heroku Deployment
This application has been deployed from GitHub to Heroku by following the steps:

1. Create or log in to your account at [heroku.com](https://heroku.com)
2. Create a new app, choose a unique app name for your app, and select your region.
3. Click "Create app".
4. Under the resources tab, type "postgres", and add a Postgres database to the app (a "Hobby" plan was used for this app).
5. Install the plugins dj-database-url and psycopg2-binary from the CLI in your workspace.
6. Install django and gunicorn from the CLI in your workspace.
7. Use the terminal command "pip3 freeze --local > requirements.txt" to generate your requirements.txt file, required for Heroku deployment.
8. Create a Procfile in your app and enter the following, replacing PROJECT_NAME with your app name: 
   (web: gunicorn PROJECT_NAME.wsgi)
9.  Ensure that your settings.py file is connected to your new Postgres database from Heroku.
10. In settings.py, check that Debug = False.
11. Under the "ALLOWED_HOSTS" variable in settings.py, make sure that 'localhost' and the deployed Heroku root url are included. 
12. Go to Settings in your Heroku and set the environment variables in the Config Vars
    ![Heroku config vars](docs/readme/config-vars.png)
13. Remove DISABLE_COLLECTSTATIC from Heroku settings.
14. Push the code to Heroku using the command "git push heroku main" from your CLI.

Final steps:

- PLACEHOLDER_TEXT


### Forking the GitHub Repository
1. Go to the GitHub repository
2. Click on the fork icon in top right corner
3. You will then have am identical copy of that repository.
   

##### Back to [top](#table-of-contents)

---

## Credits

- [TEST](https://google.com/) for ...

##### Back to [top](#table-of-contents)