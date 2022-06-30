Feature: modificacion de horas

    Scenario Outline: disminuyo horas cargadas de un recurso a una tarea
        Given un recurso con ID <id> 
        And una tarea con título <tituloTarea>
        And el recurso está asignado a la tarea
        And el recurso tiene <cantidadInicial> horas cargadas en la tarea
        When se intenta disminuir las horas trabajadas del recurso a la tarea en <cantidad>
        Then la tarea tendrá <cantidadFinal> horas consumidas del recurso

    Examples:
        | id | tituloTarea   | cantidadInicial | cantidad | cantidadFinal |
        | 2  | "Refactorizar"| 5               | 2        | 3             |
        | 5  | "Debuggear"   | 3               | 3        | 0             |
        | 0  | "Testing"     | 8               | 5        | 3             |


    Scenario Outline: aumento horas cargadas de un recurso a una tarea
        Given un recurso con ID <id> 
        And una tarea con título <tituloTarea>
        And el recurso está asignado a la tarea
        And el recurso tiene <cantidadInicial> horas cargadas en la tarea
        When se intenta aumentar las horas trabajadas del recurso a la tarea en <cantidad>
        Then la tarea tendrá <cantidadFinal> horas consumidas del recurso

    Examples:
        | id | tituloTarea   | cantidadInicial | cantidad | cantidadFinal |
        | 1  | "Refactorizar"| 2               | 2        | 4             |
        | 2  | "Debuggear"   | 1               | 3        | 4             |
        | 3  | "Testing"     | 5               | 3        | 8             |


    Scenario Outline: no se pueden modificar horas de un recurso a una tarea que no existe
        Given un recurso con ID <id>
        And el recurso realiza un trabajo sobre una tarea que no existe
        When se intenta aumentar <cantidad> horas trabajadas del recurso a una tarea que no existe
        Then la carga debe ser denegada por ingresar mal la tarea

    Examples:
        | id | cantidad |
        | 0  | 1        |
        | 1  | 0        |
        | 2  | 7        |   

    Scenario Outline: no se pueden modificar horas de un recurso a un recurso que no existe
        Given una tarea con título <tituloTarea>
        And se realiza un trabajo sobre la tarea 
        When se intenta aumentar <cantidad> horas trabajadas de un recurso que no existe a la tarea
        Then la carga debe ser denegada por ingresar mal la tarea

    Examples:
        | tituloTarea          | cantidad |
        | "Modelo de Dominio"  | 1        |
        | "Diagrma de clases"  | 0        |
        | "Arreglar bug main"  | 7        | 

    Scenario Outline: no puedo disminuir las horas en una cantidad mayor a las que están cargadas
        Given un recurso con ID <id> 
        And una tarea con título <tituloTarea>
        And el recurso está asignado a la tarea
        And el recurso tiene <cantidadInicial> horas cargadas en la tarea
        When se intenta disminuir las horas trabajadas del recurso a la tarea en <cantidad>
        Then la modificación debe ser denegada por superar la cantidad de horas cargadas a disminuir
        And la tarea tendrá <cantidadInicial> horas consumidas del recurso

    Examples:
        | id | tituloTarea   | cantidadInicial | cantidad |
        | 1  | "Refactorizar"| 5               | 7        |
        | 2  | "Debuggear"   | 1               | 2        |
        | 3  | "Testing"     | 2               | 5        |

    Scenario Outline: no puedo aumentar la cantidad de horas y superar las 8 horas diarias
        Given un recurso con ID <id> 
        And una tarea con título <tituloTarea>
        And el recurso está asignado a la tarea
        And el recurso tiene <cantidadInicial> horas cargadas en la tarea el día <fecha>
        When se intenta aumentar <cantidad> la cantidad horas trabajadas superando el límite diario
        Then la modificación debe ser denegada por superar el límite de carga diario
        And la tarea tendrá <cantidadInicial> horas consumidas del recurso

    Examples:
        | id | tituloTarea   | cantidadInicial | fecha      |cantidad  |
        | 7  | "Refactorizar"| 5               | 10-06-2022 | 4        |
        | 2  | "Debuggear"   | 6               | 24-12-2019 | 4        |
        | 83 | "Testing"     | 2               | 27-07-2017 | 7        |