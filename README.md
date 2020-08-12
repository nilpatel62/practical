#Steps for run the project successfully
1. clone the repo using command: "git clone https://github.com/nilpatel62/practical.git"
2. create virtualenv for install the dependencies command: "virtualenv -p python3 enve"
3. active the virtual environment using command: ". enve/bin/activate"
4. need to install all requirements which are in requirements.txt file command: "pip3 install -r requirements.txt"
5. after install all requirements need to change database credentials in settings.py for the mysql
    a) need to change username for the MySQL Database
    b) need to change host for the MySQL Database
    c) need to change database name for the MySQL Database
    d) need to change password for the MySQL Database
6. after change the credentials need to execute command: "python3 manage.py makemigrations"
7. after run last command need to execute command: "python3 manage.py migrate"
8. need to start django server: "python3 manage.py runserver"
9. open browser and paste the command: "http://127.0.0.1:8000/"