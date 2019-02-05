# Linux Server Configuration Project

This is the configuration for a server to host a catalog application that allows a user to view different sports and view the equipment associated with the sport.

## How to Access Server

### SSH

The IP address for the server is 3.92.192.125 and it can be accessed by SSH using port 2200.

### Browser

To access the application follow this link [http://3.92.192.125/catalogs/](http://3.92.192.125/catalogs/)

## Software Installed

The following was installed on the server to run the catalog application.
 
* `flask`
* `httplib2`
* `json`
* `requests`
* `sqlalchemy`

In order to run the application using apache utilizing python3 the following was also installed

* `libapache2-mod-wsgi-py3`

## Configuration 

The server was configured only allow the following applications.

* HTTP port 80
* SSH port 2200
* NTP port 123

Other configurations made to the server include forsed ssh key authentication and restricting access to logging in as root remotely.

### Third Part Resources

In order to help set up the server I utilized this [blog](https://umar-yusuf.blogspot.com/2018/02/deploying-python-flask-web-app-on.html) for additional information outside what was provided in the course.

