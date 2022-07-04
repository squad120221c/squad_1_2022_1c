Feature: modificación registro de horas
    
    Scenario Outline: aumento horas cargadas de un recurso a una tarea
        Given un recurso con ID <idRecurso> 
        And una tarea con ID <idTarea>
        And el recurso está asignado a la tarea
        And se registraron <cantidadInicial> horas del recurso en la tarea
        When se intenta aumentar las horas trabajadas del recurso a la tarea a <cantidadNueva> horas
        Then la tarea tendrá <cantidadFinal> horas consumidas del recurso

    Examples:
        | idRecurso | idTarea | cantidadInicial | cantidadNueva | cantidadFinal |
        | 1         | 3       | 2               | 4             | 4             |
        | 2         | 5       | 1               | 3             | 3             |
        | 3         | 7       | 5               | 8             | 8             |

    Scenario Outline: disminuyo horas cargadas de un recurso a una tarea
        Given un recurso con ID <idRecurso> 
        And una tarea con ID <idTarea>
        And el recurso está asignado a la tarea
        And se registraron <cantidadInicial> horas del recurso en la tarea
        When se intenta disminuir las horas trabajadas del recurso a la tarea a <cantidadNueva> horas
        Then la tarea tendrá <cantidadFinal> horas consumidas del recurso

    Examples:
        | idRecurso | idTarea | cantidadInicial | cantidadNueva | cantidadFinal |
        | 2         | 5       | 5               | 2             | 2             |
        | 5         | 2       | 3               | 2             | 2             |
        | 0         | 8       | 8               | 5             | 5             |

    Scenario Outline: no se pueden modificar un registro que no existe
        Given que no existe un registro con ID <idRegistro>
        When se intenta modificar el registro
        Then la modificación debe ser denegada

    Examples:
        | idRegistro |
        | 0          |
        | 1          |
        | 2          |

    Scenario Outline: cambio exitosamente la tarea de un registro
        Given un recurso con ID <idRecurso> 
        And una tarea con ID <idTareaInicial>
        And una tarea con ID <idTareaFinal>
        And existe un registro de la tarea <idRecurso> y el recurso <idTareaInicial>
        And el recurso está asignado a la tarea
        When se intenta modificar la tarea a la tarea con ID <idTareaFinal>
        Then el registro tendrá la tarea con id <idTareaFinal>

    Examples:
        | idRecurso | idTareaInicial | idTareaFinal |
        | 2         | 92             |  56          |
        | 23        | 2              |  6           |
        | 16        | 0              |  621         |

    Scenario Outline: aumento horas cargadas de un recurso a una tarea
        Given un recurso con ID <idRecurso> 
        And una tarea con ID <idTareaInicial>
        And una tarea con ID <idTareaFinal>
        And existe un registro de la tarea <idRecurso> y el recurso <idTareaInicial>
        And el recurso no está asignado a la tarea
        When se intenta modificar la tarea a la tarea con ID <idTareaFinal>
        Then la modificación debe ser denegada
        And el registro tendrá la tarea con id <idTareaInicial>

    Examples:
        | idRecurso | idTareaInicial | idTareaFinal |
        | 4         | 2              |  5           |
        | 6         | 7              |  3           |
        | 5         | 9              |  9           |

    Scenario Outline: falla al intentar disminuir la cantidad de horas a un valor menor a 1
        Given un recurso con ID <idRecurso> 
        And una tarea con ID <idTarea>
        And el recurso está asignado a la tarea
        And se registraron <cantidadInicial> horas del recurso en la tarea
        When se intenta disminuir las horas trabajadas del recurso a la tarea a <cantidadNueva> horas
        Then la modificación es denegeada 
        And la cantidad de horas permanece en <cantidadInicial>

    Examples:
        | idRecurso | idTarea | cantidadInicial | cantidadNueva |
        | 2         | 5       | 5               | 0             |
        | 5         | 2       | 3               | -1            |
        | 0         | 8       | 8               | -5            |

    Scenario Outline: falla al intentar aumentar la cantidad de horas a un valor mayor a 8
        Given un recurso con ID <idRecurso> 
        And una tarea con ID <idTarea>
        And el recurso está asignado a la tarea
        And se registraron <cantidadInicial> horas del recurso en la tarea
        When se intenta aumentar las horas trabajadas del recurso a la tarea a <cantidadNueva> horas
        Then la modificación es denegeada 
        And la cantidad de horas permanece en <cantidadInicial>

    Examples:
        | idRecurso | idTarea | cantidadInicial | cantidadNueva |
        | 3         | 4       | 5               | 9             |
        | 5         | 2       | 3               | 12            |
        | 0         | 8       | 8               | 15            |