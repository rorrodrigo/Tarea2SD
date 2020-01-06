# Tarea2SD
Tarea 2 de sistemas distribuidos USM, SJ 2019-2\
Rodrigo Álvarez 201573587-5\
Manuel Sandoval 201573604-9

Indicaciones generales para correr cada actividad:

docker-compose build\
docker-compose up
 
 Luego para interacctuar con la consola, ejecutar en dos terminales distintas lo siguiente:
 Para la actividad 1
 docker attach cliente\
 docker attach cliente_2
 
 Para la actividad 2
 docker attach client\
 docker attach client_2
 
 y proceder en ambas actividades ingresando los nombres de usuario a utilizar.
 
 Para conectar un cliente extra en ambas actividades, ejecutar lo siguiente en una nueva terminal:\
 docker-compose run client
 Lo que creará el container correspondiente y desplegará la consola para poder interacctuar con ella.
