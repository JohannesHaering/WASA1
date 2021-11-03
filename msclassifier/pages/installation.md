# Installation
The backend requires a PostgreSQL database.

## Current State
In the `src` folder run the following commands:
1) `py setup.py install`
2) `py app.py`

This creates a flask app listening to requests on port 5000.

## With working dockerfile
1) To create a docker image from the source code run: `docker build -t <ImageName>`
2) To create a container which executes the image run: `docker run -p 80:5000 <ContainerName> <ImageName>`

Then the backend interfaces are exposed on port 5000.

\<ImageName\> is a placeholder for the name of the image, <\ContainerName\> is a placeholder for the name of the container
