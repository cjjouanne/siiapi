# SIIAPI

[SIIAPI.ga](https://siiapi.ga/), tal como indica su nombre es una API gratuita de codigo abierto que permite obtener informacion de tus cuentas en el Servicio de Impuestos Internos de Chile 🇨🇱 ([SII.cl](https://zeusr.sii.cl//AUT2000/InicioAutenticacion/IngresoRutClave.html?https://misiir.sii.cl/cgi_misii/siihome.cgi)). A través de llamadas a la API Puesdes consultar tu libro de Compras y Ventas.

## Como utilizar la API?
Para usar las diferentes llamadas a la API puedes utilizar tu API Key de usuario o bien la API Key correspondiente cada empresa registrada. Con estas puedes obtener el resumen del libro de compras o ventas, la version exportable detallada del libro de compras o ventas, y puedes consultar el detalle por tipo de documentos. Para más info, consulta la documentación disponible [aqui](https://siiapi.ga/docs).

## Quieres Colaborar?
Puedes solicitar nuevas funcionalidades en el form de contacto disponible [aqui](https://siiapi.ga/contact), o puedes abrir un _**pull request**_ a través de GitHub incorporando tus nuevas ideas.


## Como correr la API de manera local

### Requisitos
Debes tener instalado:
* **Python 3.9** o posterior,
* Algun gestor de bases de datos como **PostgreSQL** o **SQLite**.

### Instala las dependencias
Ejecuta el siguiente comando en la terminal
```
pip3 install -r requirements.txt
```

y ya estás listo para ejectutar la app en la terminal con el comando
```
python3 run.py
```

