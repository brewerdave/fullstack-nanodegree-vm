# Item Catalog Project #

## Description ##

This is a site to store character builds for the game Path of Exile. You can log in with a Google account to store your favorite builds and and new ones to the list.

## Download ##

This project is available on [GitHub](https://github.com/brewerdave/fullstack-nanodegree-vm/tree/master/vagrant/catalog)

## Requirements ##

* VirtualBox
* Vagrant
* Javascript should be enabled to view the website properly

## To Run ##

Download or fork the repository.

Start Vagrant by navigating to vagrant folder and running:

```bash
vagrant up
vagrant ssh
```

Start the program inside the vm with:

```python
redis-server
cd /vagrant/catalog
python3 project.py
```

To reinitialize the database with sample data, from catalog directory:

```bash
rm pathofexile.db
python3 setup_database.py
python3 load_database.py
```
Visit http://localhost:5000/buildfinder to see the website.

## API ##
Visit http://localhost:5000/buildfinder/api/v1/token in a browser to get a one hour token.

You can send cURL requests such as (replacing TOKEN with your token and adding any needed parameters to the JSON):

```bash
curl -H "Content-Type: application/json" -X GET -d '{"token":"TOKEN"}' http://localhost:5000/buildfinder/api/v1/builds
```

For http://localhost:5000/buildfinder/api/v1/builds:
* GET request returns all builds
* POST adds a build
  * Required Parameters
    * title : Title of build
    * url : Forum link of build
    * short_description : Short overview of build
    * long_description : Text of actual build
    * character_class_name : Character class
    * game_version : Version build is for (eg. 2.6 or 3.0)
    * author : Author of the build

For http://localhost:5000/buildfinder/api/v1/build/ID (where ID is the build's integer id):

* GET returns the build
* DELETE deletes the build
* PUT edits the build
  * Optional Paramters
    * title : Title of build
    * url : Forum link of build
    * short_description : Short overview of build
    * long_description : Text of actual build
    * character_class_name : Character class
    * game_version : Version build is for (eg. 2.6 or 3.0)
    * author : Author of the build