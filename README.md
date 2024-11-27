# RIDER APP

This is a Ride hailing app that allows users to request for a ride and drivers to accept the request, well with some added feature


## Technology
- Python
- PostGIS
- Redis
- Celery & Celery beat
- Django, Django Rest Framework, Django Channels
- Docker

## Geting started
- Clone the app and cd into the directory
- Create a `.env` file and populate it with your own values, needed keys are provided in the `.env.example` file
- Run `make build` to build the docker image
- Run `make up` to start the containers

## Further information
- Other management commands are provided in the `Makefile`
- You can access the email server at `http://localhost:8025`
- You can access the admin panel at `http://localhost:8000/admin`
- You can access the API documentation at `http://localhost:8000/`


Happy Hacking  🚀
