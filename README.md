# item-catalog
To run this project, you can use vagrant as follows,
1) Place the entire project folder in vagrant folder on your machine
2) On your terminal go to vagrant path and type in
vagrant up
and then
vagrant ssh

3) Once the vagrant is up, cd to /vagrant/ItemCatalog which is the path of this project
4) Run database_setup.py by typing
python database_setup.py

5) Then run lotsofitems.py to populate database with values
python lotsofitems.py

6) Next, run application.py
python application.py

This will start the project on localhost:8000

localhost:8000\login will open login page where you can login with Google plus credentials
