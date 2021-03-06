# planet_api

Small API for serving assets

## Instructions:

### Use Vagrant (preferred):
* Make sure you have vagrant intalled, with a suitable provider like VirtualBox
* Clone the repo, and 'cd' into the base directory.

`git clone https://github.com/gidj/planet_api.git && cd planet_api`

* As long as you want to use the provided defaults, just issue the following command:

`vagrant up`

* Wait for the box to download and Vagrant to provision the VM
* After provisioning, the base API endpoint is at http://192.168.33.10/api/v1/

### Manully (not really recommended):
* Make sure you have PostgreSQL installed on the machine you will use, and that it is running
* Create the 'planet' user:

`sudo -u postgres psql -c "CREATE USER planet WITH PASSWORD 'planet';"`

* Create the 'planet' database:

`sudo -u postgres createdb planet`

* Clone the planet_api repository, and cd into it:

`git clone https://github.com/gidj/planet_api.git && cd planet_api`

* Create a virtualenv and source it:

`virtualenv venv && source venv/bin/activate`

* Intall the requirements:

`pip install -r requirements.pip`

* Set up the database:

`python manage.py db upgrade`

* Start the app:

`python manage.py runserver`

* Now you should be able to access the API at localhost:5000/api/v1/

## Running the tests:

If you are interested in running the test suite, do the following:
* Change directories to the base of the project:
`cd planet_api`
* Source the virtual environment:
`source venv/bin/activate`
* Run the tests:
` python -m unittest tests`

## Create Sample Records

The project doesn't come with any data preloaded, but if you want to populate the database with some sample resources using the API, open a python shell and run the following:

~~~~
from random import choice
import requests

VALID_TYPES = {
    u'satellite': (u'dove', u'rapideye'),
    u'antenna'  : (u'dish', u'yagi'),
}
ASSETS_ENDPOINT = "http://192.168.33.10/api/v1/assets/"

for number in range(60):
    asset_type = choice(VALID_TYPES.keys())
    asset_class = choice(VALID_TYPES[asset_type])
    data = {
        "name": "Sampl42"+str(number),
        "type": asset_type,
        "class": asset_class,
    }

    r = requests.post(ASSETS_ENDPOINT, json=data)
~~~~

If you are running the app in some way that doesn't use the default Vagrant instructions above, change the ASSETS_ENDPOINT variable accordingly.



