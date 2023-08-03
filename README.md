#AI_Planet_Project

## Requirements

This project requires Python and several Python packages to run. You can find the list of required packages in the `requirements.txt` file. To set up the project locally, follow these steps:

1. Create a virtual environment using your preferred virtual environment manager (e.g., virtualenv, pipenv).
2. Activate the virtual environment.
3. Install the required packages listed in the `requirements.txt` file using `pip`:
```
pip install -r requirements.txt
```
Once the dependencies are installed, you can run the project locally on your machine after necessary migrations.
Go to the project directory(hackathons) and run the following to make migrations

```
py manage.py makemigrations
py manage.py migrate
```

To run the server

```
py manage.py runserver
```
