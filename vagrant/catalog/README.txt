# Catalog Application Project

This Catalog Application allows a user to view different sports and view the equipment associated with that sport. If a user is logged in they can add a new item and edit/delete items they own.

## Prerequisites

### Installation
In order to run the script make sure to install the following packages:

* `flask`
* `oauth2client`
* `httplib2`
* `json`
* `requests`
* `flask_httpauth`
* `sqlalchemy`

You can install these packages by running the following command for each package:

`$ pip install <package>`
or
`$ pip3 install <package>`

depending on what version of pip you have installed

### Database
In order for this application to run the catalog.db database must be in the same folder as the application.py file. This database can be found [here](https://github.com/mmvulich/fullstack-nanodegree-vm/blob/master/vagrant/catalog/catalog.db)

### Authorization
In order to use the application for more than viewing the database (i.e. new/edit/delete) you will need a google account. If you do not have one you can sign up for one for free [here](https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dsign%2Bup%2Bfor%2Bgoogle%2Baccount%26rlz%3D1C1CHBF_enUS817US817%26oq%3Dsign%2Bup%2Bfor%2Bgoogle%2Baccount%26aqs%3Dchrome..69i57j0l5.3425j1j7%26sourceid%3Dchrome%26ie%3DUTF-8&flowName=GlifWebSignIn&flowEntry=AddSession)

## Usage

### Kicking off Application
To run the Catalog Application script `cd` to the directory where the script is saved and then run the following command:

`$ python application.py'

### Interacting in the Browser
Open your favorite browser and navagate to [http://localhost:8000/](http://localhost:8000/)

This will bring you to the main page of application where you can see a list of all the sports in the catalog and the last 6 equipment items that have been added. You can click on a sport to view all the equipment associated with that sport or click on an equipment item to get a detailed description.

Logging into the application using your google login credentials will allow you to add an item to a sport and edit/delete any items that you own.

