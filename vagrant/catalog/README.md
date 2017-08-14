# Item Catalog Project #

## Description ##

This is a site to store character builds for the game Path of Exile. You can log in with a Google account to store your favorite builds and and new ones to the list.

## Download ##

This project is available on [GitHub](https://github.com/brewerdave/fullstack-nanodegree-vm/tree/master/vagrant/catalog)

## Requirements ##

* VirtualBox
* Vagrant

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
