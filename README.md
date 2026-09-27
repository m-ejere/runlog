# RunLog

RunLog is a Django-based running log application that allows users to record, manage and review their running activity.

The application was developed as a Code Institute Full Stack Frameworks project.

---

## Live Website

[Visit the live RunLog website](https://runlog-app-e87e6c070f8b.herokuapp.com/)

---

## Project Purpose

The purpose of RunLog is to provide runners with a simple and organised way to keep track of their running activity in one place.

Users can create an account, securely log in, record their runs, view their running history, edit or delete their own records, and monitor basic running statistics.

The project focuses on providing a straightforward user experience while demonstrating full-stack development using Django, relational database management, authentication, CRUD functionality, validation and deployment.

---

## User Experience

RunLog was designed around the needs of a runner who wants a simple way to record and review their running activity.

The main UX goals are:

- Clear and simple navigation.
- Easy account registration and login.
- Quick entry of running information.
- Clear access to previous runs.
- Simple editing and deletion of records.
- Useful running statistics.
- Privacy between user accounts.
- Responsive usability across desktop and mobile screen sizes.

---

## User Stories

The project was developed using the following user stories:

1. As a runner, I want to register for an account so that I can securely access my running records.

2. As a registered user, I want to log in and log out so that I can securely access my account.

3. As a runner, I want to add a run so that I can keep a record of my running activity.

4. As a runner, I want to view my runs so that I can see my running history.

5. As a runner, I want to be able to edit my runs so that I can alter my running history.

6. As a runner, I want to delete my runs so that I can remove records I no longer need.

7. As a runner, I want to see my running statistics so that I can monitor my progress.

8. As a runner, I want my runs to be private so that other users cannot access or modify my records.

---

## UX Design

### Wireframes

Wireframes were created during the planning stage to establish the structure and navigation of the application before development.

The wireframes cover the main user journeys and application screens:

- Login
- Registration
- My Runs / Dashboard
- Add Run
- Edit Run
- Delete confirmation

The wireframes focus on:

- Simple navigation.
- Clear information hierarchy.
- Easy run entry.
- Clear running statistics.
- Accessible edit and delete actions.
- Responsive layout.

![RunLog wireframes](evidence/wireframes.png)

---

## Features

### User Authentication

Users can:

- Register for an account.
- Log in securely.
- Log out securely.
- Access their own running records.
- Keep their running records private from other users.

Authentication is handled using Django's built-in authentication system.

---

### Run Management

Authenticated users can:

- Add a new run.
- View their running history.
- Edit their own runs.
- Delete their own runs.

Each run can contain:

- Date.
- Distance.
- Distance unit.
- Run type.
- Duration.
- Notes.

---

### Distance Units

Users can record their distance using:

- Kilometres.
- Miles.

The application handles distance values consistently when displaying running statistics.

---

### Run Types

Users can select a run type when recording their activity.

This allows their running history to contain additional information about the type of activity completed.

---

### Duration

Users can record the duration of their run using:

- Hours.
- Minutes.
- Seconds.

The application validates the duration to prevent invalid zero-duration runs.

---

### Notes

Users can optionally add notes to each run.

This allows additional information about an individual run to be stored alongside the main running data.

---

### Running Statistics

The dashboard provides statistics based on the user's recorded runs, including:

- Total number of runs.
- Total distance.
- Average distance.
- Running history.

---

### Validation

The application validates user input to help prevent invalid data.

Examples include:

- Preventing future-dated runs.
- Preventing zero or negative duration.
- Restricting users from modifying another user's runs.
- Restricting users from deleting another user's runs.

---

### User Privacy

Each run is associated with the user who created it.

Users can only access and manage their own running records.

Unauthorised users cannot access or modify another user's running data through the application's frontend.

---

## Technologies Used

### Languages

- HTML
- CSS
- Python

### Frameworks

- Django

### Libraries and Packages

- WhiteNoise
- Gunicorn
- dj-database-url
- psycopg2-binary

### Database

- PostgreSQL for production.
- SQLite for local development.

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Heroku
- Code Institute PEP8 Validator
- W3C HTML Validator
- W3C CSS Validator
- Google Lighthouse

---

## Database

RunLog uses Django's Object-Relational Mapper (ORM) to communicate with the database.

The main application data is stored using Django models.

Each run is associated with the authenticated user who created it.

### Production Database

PostgreSQL is used for the deployed application.

### Development Database

SQLite is used during local development.

This allows the project to use a lightweight local database while using PostgreSQL for the production deployment.

---

## Agile Development

The project was developed using an Agile approach.

Development work was organised into user stories and tasks using a GitHub Projects board.

The project board was used to:

- Break the project into manageable user stories.
- Prioritise development requirements.
- Track development tasks.
- Monitor progress.
- Keep the development process focused on the requirements of the application.

### GitHub Project Board

[View the RunLog GitHub Project Board](https://github.com/users/m-ejere/projects/5)

The board contains the project's user stories and development tasks.

---

## MoSCoW Prioritisation

MoSCoW prioritisation was used during the planning stage to identify which requirements were essential to the project.

### Must Have

- User registration.
- User login and logout.
- Adding runs.
- Viewing runs.
- Editing runs.
- Deleting runs.
- User-specific/private run data.
- Running statistics.
- Input validation.

### Should Have

- Responsive design.
- Clear success and error messages.
- Clear navigation.
- Consistent user interface.

### Could Have

- Additional visual refinements.
- Further improvements to the presentation of running information.

### Won't Have

Features outside the core purpose of the application were intentionally excluded from the project scope, including:

- Social networking.
- Leaderboards.
- Messaging.
- Friends/followers.
- GPS tracking.
- Maps.
- Running challenges.
- Achievements.
- Payment functionality.

This helped keep development focused on the core requirements of RunLog.

---

# Testing

Testing was carried out throughout development to identify functional, validation, usability and deployment issues.

Testing included:

- Automated Django testing.
- Manual functional testing.
- HTML validation.
- CSS validation.
- Lighthouse testing.
- Responsive testing.
- PEP8 validation.
- Production testing on Heroku.

---

## Automated Testing

The application contains an automated Django test suite.

The test suite contains **10 tests**, all of which pass successfully.

The tests cover important application functionality including:

- Authentication requirements.
- User login.
- Displaying a user's own runs.
- Adding runs.
- Editing runs.
- Preventing users from editing another user's runs.
- Preventing users from deleting another user's runs.
- Deleting runs.
- Preventing future-dated runs.
- Preventing zero-duration runs.

### Automated Test Evidence

![Automated Django tests](evidence/automated-tests.png)

The following Django commands were also used during development:

```text
python manage.py check

python manage.py test

python manage.py collectstatic --noinput