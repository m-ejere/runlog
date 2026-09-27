# RunLog

RunLog is a Django-based running log application that allows users to record, manage and review their running activity.

The application was created as a Code Institute Full Stack Frameworks project.

## Live Website

[RunLog](https://runlog-app-e87e6c070f8b.herokuapp.com/)

## Project Purpose

The purpose of RunLog is to provide runners with a simple way to keep track of their runs in one place.

Users can create an account, record their runs, view their running history and see statistics based on their recorded activity.

## Features

### User Authentication

- Users can register for an account.
- Users can log in and log out.
- Run information is associated with the logged-in user.
- Users can only manage their own runs.

### Run Management

Authenticated users can:

- Add a new run.
- Edit their own runs.
- Delete their own runs.
- Record the date of a run.
- Record the distance.
- Select kilometres or miles.
- Select a run type.
- Record the duration.
- Add notes.

### Validation

The application validates user input to prevent invalid run data.

Examples include:

- Preventing runs from being recorded for a future date.
- Preventing a run from having a zero or negative duration.
- Restricting users from editing or deleting another user's runs.

### Running Statistics

The dashboard provides statistics based on the user's recorded runs, including:

- Total distance.
- Average distance.
- Number of runs.
- Running history.

Distance values are handled consistently when users record runs using different units.

## User Experience

The application is designed to be simple and straightforward.

The main goals are:

- Clear navigation.
- Easy run entry.
- Simple access to running history.
- Clear presentation of statistics.
- Responsive layout for different screen sizes.

## Technologies Used

### Languages

- HTML
- CSS
- Python

### Frameworks and Libraries

- Django
- WhiteNoise
- Gunicorn
- psycopg2
- dj-database-url

### Database

- PostgreSQL in production
- SQLite for local development

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Heroku

## Database

The application uses Django's ORM to interact with the database.

The main application data is stored using Django models, with each run associated with its user.

PostgreSQL is used for the deployed production application.

## Testing

The application includes automated Django tests covering important functionality.

The test suite checks:

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

The test suite currently contains 10 tests and all tests pass successfully.

Additional checks performed during development include:

```text
python manage.py check
python manage.py test
python manage.py collectstatic --noinput