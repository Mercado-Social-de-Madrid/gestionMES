# Instalación
--------------

## Linux

Instalar dependencias previas:

```
sudo apt-get install git
sudo apt-get install apache2
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```

Instalar Python
```
wget https://www.python.org/ftp/python/2.7.13/Python-2.7.13.tgz
tar xzf Python-2.7.13.tgz
cd Python-2.7.13
./configure
make
sudo make install
```

Instalar pip y virtualenv
```
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
sudo python get-pip.py
sudo pip install virtualenvwrapper
```

Añadimos el virtualenv a nuestro perfil de bash (), añadiendo las siguientes líneas al final:
```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh
```

Creamos nuestro virtualenv
```
mkvirtualenv alcalasuena
workon alcalasuena
```

Clonamos el repositorio
```
git clone https://github.com/InsulaCoworking/AlcalaSuena.git
cd AlcalaSuena
```

Instalamos las dependencias del proyecto:
```
pip install -r requirements.txt
```

Instalamos mySQL (nos pedirá introducir la constraseña de root):
```
sudo apt-get install mysql-server
sudo apt-get install python-dev libmysqlclient-dev
sudo systemctl mysql start
```

Entramos en la consola de mySQL (`mysqladmin -u root -p`):
```
create database alcalasuena;
grant all privileges on alcalasuena.* to 'insuler'@'localhost' identified by "insula";
```

### Apache

Instalamos el módulo wsgi de Apache:
```
sudo apt-get install libapache2-mod-wsgi
```

Editamos el fichero de configuración de nuestro sitio (en este ejemplo el de por defecto)
```
sudo nano /etc/apache2/sites-available/000-default.conf
```

Dentro de este fichero, tenemos que añadir las reglas para configurar nuestra app de Django:
```
		Alias /static/ /home/username/static/
        Alias /media/ /home/username/media/
        WSGIScriptAlias / /home/username/AlcalaSuena/alcalasuena/wsgi.py
        WSGIDaemonProcess alcalasuena python-home=/home/username/.virtualenvs/alcalasuena python-path=/home/username/AlcalaSuena
        WSGIProcessGroup alcalasuena

        <Directory /home/username/AlcalaSuena/alcalasuena>
         <Files wsgi.py>
            Require all granted
         </Files>
         </Directory>

		 <Directory /home/username/static>
           Require all granted
        </Directory>

        <Directory /home/username/media>
           Require all granted
        </Directory>
```

Una vez guardado, actualizamos el servicio de Apache:
```
sudo service apache2 restart
```
