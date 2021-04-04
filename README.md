# Coffee Shop Full Stack

## Full Stack Nano - IAM Final Project

The application can:

1. Display graphics representing the ratios of ingredients in each drink.
2. Allow public users to view drink names and graphics.
3. Allow the shop baristas to see the recipe information.
4. Allow the shop managers to create new drinks and edit existing drinks.


### Backend

The `./backend` directory contains a Flask server with a pre-written SQLAlchemy module. I completed the endpoints, configured, and integrated with Auth0 for authentication.


### Frontend

The `./frontend` directory contains a pre-written Ionic frontend to consume the data from the Flask server. I configured the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app.
