# Science Rock Database

MRover's custom database and associated user interface for querying information about rocks, for use at URC and possibly CIRC. This wiki is meant for setting up on a basestation laptop.

## Setup Backend

Install node:

    $ sudo apt install nodejs
    $ sudo apt install npm

Install necessary packages in the backend folder:

    $ cd node-express-mongodb
    node-express-mongodb $ npm install express mongoose body-parser cors --save

Make a folder for the database folder to be stored in:

    node-express-mongodb $ sudo mkdir -p /data/db

## Run Backend

To start the backend server:

    node-express-mongodb $ sudo mongod

In a new terminal:

    node-express-mongodb $ node server.js

If successful, you should see the following output (it may take a few seconds):

    Server is now running on port 8080.
    Connected to the database!
