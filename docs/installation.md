# Instalación
--------------

## Linux

Instalar dependencias previas:

```
sudo apt-get install git
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```

Si no tenemos Python (por defecto en el sistema deberíamos tenerlo disponible, debemos instalar una versión de Python >3.5
A continuación podemos instalar virtualenv para crear entornos virtuales de python en el que instalar las dependencias de nuestro proyecto.
```
sudo python3-pip
pip install virtualenvwrapper
```

Añadimos el virtualenv a nuestro perfil de bash (normalmente editando el fichero `~/.bashrc`), añadiendo las siguientes líneas al final:

```
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh
```

Creamos nuestro virtualenv
```
mkvirtualenv mes
workon mes
```

Clonamos el repositorio
```
git clone https://github.com/Mercado-Social-de-Madrid/gestionMES.git
cd gestionMES
```

Instalamos mySQL (nos pedirá introducir la constraseña de root):
```
sudo apt-get install mysql-server
sudo apt-get install python-dev libmysqlclient-dev
sudo systemctl mysql start
```

Entramos en la consola de mySQL(`mysql -u root -p`) y creamos la base de datos:
```
create database mes;
grant all privileges on mes.* to 'insuler'@'localhost' identified by "insula";
```


Instalamos las dependencias del proyecto:
```
pip install -r requirements.txt
```

Para empezar a ejecutar el proyecto, necesitamos hacer una mínima configuración local mediante un fichero
que no queda registrado en Git. Para ello, podemos copiar el fichero de plantilla y editar a partir del mismo:

```
cp mes/settings_secret.py.template mes/settings_secret.py
```

En este fichero tenemos que introducir nuestra configuración concreta, siendo lo más importante la configuración
de la base de datos (con la tabla y usuario que hemos creado antes) y dos campos relativos a la URL donde se
encontrará nuestro servidor: `BASESITE_URL` y `ALLOWED_HOSTS`.
Una vez configurado, realizamos las migraciones iniciales, copiamos los ficheros estáticos y creamos el usuario admin:
```
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```


### Apache

Instalamos el módulo wsgi de Apache:
```
sudo apt-get install apache2
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
        WSGIScriptAlias / /home/username/MusicCity/musiccity/wsgi.py
        WSGIDaemonProcess musiccity python-home=/home/username/.virtualenvs/musiccity python-path=/home/username/MusicCity
        WSGIProcessGroup musiccity

        <Directory /home/username/MusicCity/musiccity>
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

## Nginx

Creamos los directorios externos y añadimos al usuario al grupo web:

```
mkdir media
chmod +777 static/
chmod +777 media/
sudo usermod -aG www-data <username>
```

Creamos un directorio `configs` en el que almacenar las distintas configuraciones (que luego tendrán un enlace simbólico).
Para no tener que crearlos de cero, tenemos en el repositorio unos archivos de configuración de ejemplo
para Nginx y uWSGI que funcionan directamente:

```
mkdir congigs
cp MusicCity/docs/uwsgi_params configs/
cp MusicCity/docs/uwsgi.ini configs/
cp MusicCity/docs/nginx.conf configs/
```

Instalamos Nginx y copiamos los ficheros de configuración a los sitios disponibles y activos:

```
sudo apt-get install nginx
sudo /etc/init.d/nginx start
sudo ln -s /home/<username>/configs/nginx.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/
```

Instalamos uWSGI (**importante**: fuera del virtualenv) y añadimos los ficheros de configuración:

```
deactivate
sudo apt-get install libpcre3 libpcre3-dev
sudo pip install uwsgi
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /home/boniato/configs/uwsgi.ini /etc/uwsgi/vassals/
```

Probamos que funciona correctamente ejecutándolo de forma local:

```
sudo uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
```

Si todo funciona correctamente, añadimos el emperor de uWSGI para que se ejecute al arranque del sistema, configurándolo
como un servicio del sistema más. Para ello, creamos el fichero de configuración `/etc/systemd/system/uwsgi.service`
(tendremos que tener permisos de superusuario) en el que introducimos lo siguiente:

```
[Unit]
Description=uWSGI instance
After=syslog.target

[Service]
ExecStartPre=-/bin/bash -c 'mkdir -p /run/uwsgi; chown www-data:www-data /run/uwsgi;'
ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all

[Install]
WantedBy=multi-user.target
```

Una vez hecho esto, lo añadimos al sistema y lo ejecutamos:

```
sudo systemctl enable uwsgi
sudo systemctl start uwsig
```


```
/usr/local/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data --daemonize /var/log/uwsgi-emperor.log
```
