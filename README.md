# Arquitectura Modelo - Vista - Template

## Estructura del Directorio

- myshop: Directorio que almacena el código fuente del Sistema de Compras Myshop.
- docs: Directorio que almacena documentos auxiliares para este archivo.

## Sistema de Compras - Myshop

-- Descripción --

-- Diagrama --

## Prerrequisitos
- Clonar el repositorio:
   ```shell
   $ git clone https://gitlab.com/tareas-arquitectura-de-software-curso/modelo-vista-template.git

   $ cd modelo-vista-template

   $ cd myshop

   ```

- Instalamos Docker. La manera recomendada para implementar este sistema es utilizando [Docker](https://www.docker.com/), para instalarlo puedes seguir las instrucciones para cada sistema operativo haciendo clic [aquí](https://docs.docker.com/install/). Una vez instalado docker podemos ejecutar el siguiente comando (verificar que el servicio de Docker se encuentra corriendo):

    ```shell
    $ docker-compose up -d db
    ```

    Este comando correrá el contenedor de docker con la base de datos a utilizar en el sistema de compras myshop, el cual seguirá corriendo en background hasta que sea detenido explícitamente.

- Para el correcto funcionamiento del sistema es necesario crear la base de datos, para esto debemos abrir una conexión con el contenedor de mysql, para lograrlo escribimos en la consola lo siguiente:

    ```shell
    $  docker-compose exec db sh
    ```

- Otra forma de hacerlo es desde el cliente de docker, seleccionando la opción CLI del contenedor myshop_db como se muestra en la imagen:

    <p align="center">
        <img src="docs/proceso_mysql.png" width="80%" height="80%">
    </p>

    Con la conexión abierta, ingresamos a la base de datos con el siguiente comando, indicando el usuario y la contraseña (user = root, password = root):

    ```shell
    $  mysql -u root -p
    ```
    Dentro de mysql, ejecutamos el siguiente comando para crear la base de datos:

    ```shell
    mysql>  CREATE DATABASE myshop CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
    ```

   Si la operación fue exitosa, salimos de mysql y cerramos la conexión con el contenedor escribiendo 'exit' y dando click en el botón enter o simplemente cerrando la consola.

- Antes de iniciar el contenedor de la aplicación django debemos realizar algunos pasos previos. 

    1. Nos dirigimos al archivo myshop/myshop/.env y modificamos los siguientes campos:
        - EMAIL_HOST_USER
        - EMAIL_HOST_PASSWORD
        - DEFAULT_FROM_EMAIL
        
        Esta información es importande debido a que la aplicación envía un correo electrónico cuando se genera una orden, para que esto funcione correctamente es necesario que añada esta información (utilizando un correo gmail).
    
    2. Modificamos la línea 88 del archivo myshop/orders/views.py, en donde se encuentra la etiqueta '<your_email>' colocamos nuestro correo de gmail (el mismo correo agregado en la variable EMAIL_HOST_USER en el archivo .env).

        Ahora que se ha completado el archivo .env procederemos a realizar algunas configuraciones en su cuenta gmail para que permita el envío de correos electrónicos.

    3. Iniciamos sesión en el correo gmail del cual ingresó la información en el archivo .env.

    4. Damos click en nuestro usuario y seleccionamos la opción 'Gestionar tu cuenta de Google'.

    <p align="center">
        <img src="docs/proceso_email.png" width="30%" height="30%">
    </p>

    5. En el menú que se encuentra en el lado izquierdo seleccionamos la opción de 'Seguridad'.

    <p align="center">
        <img src="docs/proceso_email2.png" width="70%" height="70%">
    </p>

    6. Navegamos hasta encontrar el apartado 'Acceso de aplicaciones poco seguras', si se encuentra desactivada la opción, procedemos a activarla.

    <p align="center">
        <img src="docs/proceso_email3.png" width="70%" height="70%">
    </p>

    Nota: Al realizar estos pasos quedaría lista la configuración, posiblemente llegue a su bandeja de correo un email indicando el inicio de sesión, eso se debe a que la aplicación django está haciendo uso de su cuenta para el envío de correos.

    Al momento de subir el proyecto a un repositorio recomendamos remover las credenciales del archivo .env.


- Ahora procederemos a iniciar el servicio de la aplicación django, para esto ejecutamos el siguiente comando:

    ```shell
    $ docker-compose up -d web
    ```

    Este comando levantará el contenedor de docker con el sistema de compras myshop, el cual seguirá corriendo en background hasta que sea detenido explícitamente.

- Si el comando anterior se ejecutó con éxito, procederemos a aplicar las migraciones necesarias para django. Esto lo realizamos de la siguiente manera:

    Primero nos conectamos al contenedor myshop_web de la misma forma en que nos conectamos al contenedor de mysql. Ejecutamos el siguiente comando en una terminal:

    ```shell
    $ docker-compose exec web sh
    ```

    Después de conectarnos, ejecutaremos los siguientes comandos:

    ```shell
    $ python manage.py makemigrations

    $ python manage.py migrate
    ```

- Si el comando fue exitoso, podremos ingresar a nuestro navegador y verificar que el sistema se ha iniciado con éxito, para esto, ingresamos a la siguiente url: 

   > http://localhost:8000/

    Cerramos la conexión con el contenedor escribiendo 'exit' y dando click al botón enter o simplemente cerrando la consola.

   
- Para completar el proceso será necesario importar los datos contenidos en el archivo .docker/setup.sql. Para esto nos conectamos al contenedor de myshop_db (mysql) de la misma forma que lo hicimos anteriormente:

    ```shell
    $  docker-compose exec db sh
    ```

   Ya conectados, ejecutamos el siguiente comando indicando el usuario y la contraseña (user = root, password = root):

    ```shell
    $ mysql -u root -p myshop < docker-entrypoint-initdb.d/setup.sql

    ```
   
   Si la operación fue exitosa, salimos de mysql y cerramos la conexión con el contenedor escribiendo 'exit' y dando click al botón enter o simplemente cerrando la consola.

- Si el comando fue exitoso, podremos ingresar al nuestro navegador y verificar que el sistema sigue funcionando con éxito y podemos ver los productos de la tienda en línea. Para esto, ingresamos a la siguiente url: 

   > http://localhost:8000/

- Otra manera de acceder al sistema myshop desde nuestro navegador es desde el cliente de Docker, dando click en el botón 'Open in Browser' del contenedor myshop_web como se muestra en la imagen:

    <p align="center">
        <img src="docs/proceso_myshop2.png" width="80%" height="80%">
    </p>

## Ejecución

- Para correr nuestros contenedores (después de realizar los pasos anteriores) debemos ejecutar los siguientes comandos:

    ```shell
    $ docker-compose up -d web

    $ docker-compose up -d db

    ```
    De esta forma podremos acceder al sistema myshop desde nuestro navegador.

- Otra manera de iniciar los contenedores es desde el cliente de Docker, dando click en el botón 'Start' como se muestra en la imagen:

    <p align="center">
        <img src="docs/proceso_myshop1.png" width="80%" height="80%">
    </p>

- Para corroborar que nuestros contenedores se encuentran corriendo podemos ejecutar el siguiente comando:

    ```shell
    $ docker ps

    ```
    Este comando nos mostrará los contenedores que se encuentran corriendo, en la columna Status, debemos observar la palabra UP en los contenedores myshop_web y myshop_db. 

- Otra manera de verificar que nuestros contenedores se encuentran activos es desde el cliente de Docker, debemos observar el ícono del contenedor de color verde como se muestra en la imagen:

    <p align="center">
        <img src="docs/proceso_myshop1_1.png" width="80%" height="80%">
    </p>

- Cada vez que realicemos cambios en nuestra aplicación django, los veremos reflejados de forma casi inmediata, esto debido a las configuraciones que se agregaron en el archivo docker-compose. Sin embargo, si observamos que alguna configuración no se ve reflejada, deberemos reiniciar nuestro contenedor; para esto podemos utilizar el siguiente comando:

    ```shell
    $ docker restart <container_name>

    ```

- Otra manera de reiniciar nuestros contenedores es desde el cliente de Docker, dando click en el botón 'Restart' como se muestra en la imagen:

    <p align="center">
        <img src="docs/proceso_myshop3.png" width="80%" height="80%">
    </p>


- Si necesitamos acceder al contenedor de la base de datos o de la aplicación django, lo hacemos de la misma forma que lo hicimos en los prerrequisitos. Ejecutamos alguno de los siguientes comandos según corresponda:

    ```shell
    $  docker-compose exec db sh

    $  docker-compose exec web sh
    ```

- Otra manera de acceder a la consola de nuestros contenedores es desde el cliente de Docker, dando click en el botón 'CLI' como se muestra en la imagen:

    <p align="center">
        <img src="docs/proceso_myshop.png" width="80%" height="80%">
    </p>


- Finalmente, si deseamos detener alguno de nuestros contenedores, ejecutamos el siguiente comando:

    ```shell
    $  docker stop <container_name>
    ```

- Otra manera de detener nuestros contenedores es desde el cliente de Docker, dando click en el botón 'Stop' como se muestra en la imagen:

    <p align="center">
        <img src="docs/proceso_myshop4.png" width="80%" height="80%">
    </p>


## Fuente

- El código base de este proyecto fue obtenido del siguiente repositorio:

   > https://github.com/PacktPublishing/Django-By-Example/tree/master/Chapter%207/myshop


## Versión

1.0.0 - Marzo 2021

## Autores

* **Perla Velasco**
* **Jorge Alfonso Solís**