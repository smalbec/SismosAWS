<!-- Output copied to clipboard! -->

<!-----

Yay, no errors, warnings, or alerts!

Conversion time: 0.471 seconds.


Using this Markdown file:

1. Paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β34
* Tue Aug 15 2023 12:12:37 GMT-0700 (PDT)
* Source doc: ProyectoSismosREADME
----->


**Resumen**: Este informe presenta el proceso detallado de resolución de un problema de implementación de una API utilizando AWS API Gateway, AWS Lambda, AWS Glue y AWS Athena. El objetivo era desarrollar una API que habilite a los usuarios para realizar consultas y cargar datos almacenados en Amazon S3, con la restricción de un máximo de 100 registros en memoria.

**Suposiciones consideradas**:



1. Disponibilidad de un método para enviar solicitudes de API (por ejemplo, Postman).
2. Formato esperado de las solicitudes GET (según Código 1).
3. Formato esperado de las solicitudes POST y de su body (según Código 2).

**Pasos de Implementación**:



1. **Creación de un Bucket en AWS S3:**
    * Crear el bucket "crawler-bucket-sks".
    * Definir las carpetas "outputDataGET" y "dataJsonPOST".
    * Cargar ejemplos de archivos JSON para pruebas.
2. **Extracción y Transformación con AWS Glue:**
    * Establecer un rol IAM con los permisos necesarios.
    * Configurar el Crawler de AWS Glue ("test-sks") para rastrear y extraer datos del bucket "crawler-bucket-sks" cuando se agregue un archivo a la carpeta "dataJsonPOST".
    * Crear la base de datos "test-sks" con los esquemas adecuados para recibir los datos extraídos.
    * Programar y ejecutar un Job para mantener actualizada la tabla de AWS Glue.
3. **Creación de Consultas con AWS Athena:**
    * Acceder a la consola de AWS Athena.
    * Escribir consultas SQL para analizar y procesar los datos almacenados en la tabla de AWS Glue.
    * Verificar y ajustar las consultas para obtener los resultados deseados.
4. **Creación de una API REST en API Gateway:**.
    * Crear una API REST con el endpoint /seisms.
    * Agregar los métodos GET y POST.
    * Incluir Request Validator para metodo POST para permitir maximo 100 elementos entregados. (Expuesto en JSONSchemaModel.json)
    * Configurar y desplegar la API para acceso público.
5. **Creación de una Función Lambda e Integración con la API:**
    * Crear una función Lambda y configurar los ajustes esenciales, incluido el rol con los permisos apropiados.
    * Configurar la integración de la API mediante un trigger.
    * Utilizar condicionales para procesar adecuadamente los métodos GET y POST.
    * Extraer parámetros o datos JSON según el método.
    * Ejecutar consultas SQL en AWS Athena y devolver los resultados.
6. **Pruebas de la API:**
    * Utilizar herramientas como Postman o la línea de comandos para enviar solicitudes a la API.
    * Verificar el flujo de solicitud y procesamiento en la función Lambda.
    * Confirmar la comunicación de Lambda con Athena y la devolución de resultados.
    * Confirmar restricción con solicitudes no posibles para el sistema. 

**Restricción de Memoria:** Se implementaron medidas y servicios para cumplir con la restricción de cargar/filtrar/devolver un máximo de 100 registros en memoria. Se utilizó AWS Glue para rastrear y cargar datos desde S3 a una base de datos en AWS Athena, donde las consultas SQL se limitaron a 100 registros. La función Lambda interactúa con Athena para realizar consultas y entregar resultados a los usuarios. El método POST se restringe a través de un Request Validator que utiliza un JSON Schema para solo permitir 100 máximos elementos en el body.

**API Endpoint**: **[https://wuje0z8cxc.execute-api.sa-east-1.amazonaws.com/default/seisms](https://wuje0z8cxc.execute-api.sa-east-1.amazonaws.com/default/seisms)**

**Codigo 1**: Ejemplo y formato de request GET 

https://wuje0z8cxc.execute-api.sa-east-1.amazonaws.com/default/seisms?country=US&dateLower=2013-01-01&dateUpper=2023-08-15&magnitudeLower=3.0&magnitudeHigher=8.0&skip=0

**Codigo 2**: Ejemplo y formato de request POST y su body

https://wuje0z8cxc.execute-api.sa-east-1.amazonaws.com/default/seisms

**Body:**

```

{ "sismos": [

{

    "timestamp": 1550052143,

    "country": "CN",

    "magnitude": 4.4

},

{

    "timestamp": 1687691448,

    "country": "BR",

    "magnitude": 5.0

},

{

    "timestamp": 1327702732,

    "country": "CL",

    "magnitude": 6.6

}

]}

```
