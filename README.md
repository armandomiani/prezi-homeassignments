# Prezi Exam - Armando Miani

A Prezi Exam by a candidate who would love to be living in Budapest.
[Please, do not forget to check out the Architecture Doc](ARCHITECTURE.md)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

In order to run the Prezi Exam Application, you should have installed the Docker Engine and Docker Compose.

Check out below how to install the two pre-requisites:
* Docker - https://docs.docker.com/engine/installation/
* Docker Compose - https://docs.docker.com/compose/install/

After installing, check the versions in order to assure the setup is done.

```
miani@armandomiani:~$ docker -v
> Docker version 1.12.1, build 23cf638

miani@armandomiani:~$ docker-compose -v
> docker-compose version 1.8.1, build 878cff1
```

### Installing

The setup is simple.

1. Get the code:
```
git clone https://gitlab.com/prezi-homeassignments/Armando.Miani-devops.git prezi
```

2. Get into the folder and run the compose:
```
cd prezi/ && docker-compose up
```

3. Do a test request and check if you receive a 200 OK status-code
```
curl -I localhost:9090
> HTTP/1.1 200 OK
Server: nginx/1.6.2
Date: Fri, 26 May 2017 19:03:18 GMT
Content-Type: application/json
Content-Length: 76
Connection: keep-alive
```

## API Usage

The only endpoint present is **GET /prezies** where you are able to search, sort and page 'prezies'.

The max number of rows per request is 30. 
When the *sort* parameter is not provided, the text score is used.

Examples: 
* GET /prezies?title=proident (Search by title)
* GET /prezies?limit=30&offset=6990 (Get 30 rows from the row 6990)
* GET /prezies?sort=utcCreatedAt (Sort by creation date ascending)
* GET /prezies?sort=-utcCreatedAt (Sort by creation date descending)

If you ran using *docker-compose up*, the API is available at http://localhost:9090.
The API is also available at http://104.199.11.69:9090

## Running the tests

In order to run the tests run the command below:

```
docker exec -it prezi-api bash run-tests.sh
```

You should receive a response like this:
```
========================================================================== test session starts ==========================================================================
platform linux -- Python 3.5.3, pytest-3.0.7, py-1.4.33, pluggy-0.4.0
rootdir: /api/src, inifile:
plugins: cov-2.5.1
collected 15 items

tests/test_controller_core.py ........
tests/test_controller_prezies.py .......

----------- coverage: platform linux, python 3.5.3-final-0 -----------
Name                               Stmts   Miss  Cover
------------------------------------------------------
controllers/__init__.py               33      0   100%
controllers/prezies.py                19      0   100%
exceptions.py                         10      0   100%
main.py                                8      0   100%
models/__init__.py                    62      0   100%
tests/test_controller_core.py         40      0   100%
tests/test_controller_prezies.py      21      0   100%
------------------------------------------------------
TOTAL                                193      0   100%


======================================================================= 15 passed in 2.38 seconds =======================================================================
```

## Deployment

In order to deploy the application you should push the code to master branch.

Once a commit is made a pipeline in GitLab CI is triggered.

The pipeline builds the images and pushes to a GitLab Container Registry.

After the building, GitLab sends a signal to Google Container Engine asking for deploy.

Kubernetes receives the signal, pulls the new containers and updates the pods.

## Casting

* [Google Cloud](https://cloud.google.com/) - The Cloud Environment
* [Docker](https://www.docker.com) - The Container engine
* [Python](https://www.python.org/) - The programming language
* [Bottle](https://bottlepy.org/) - The web micro-framework
* [py.test](https://pytest.org) - The Python testing framework
* [MongoDB](http://www.mongodb.com/) - The Database
* [wait-for-it.sh](https://github.com/vishnubob/wait-for-it) - A nice solution to trigger a command when a service is ready

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
