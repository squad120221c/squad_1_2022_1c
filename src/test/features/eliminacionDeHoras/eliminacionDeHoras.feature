Feature: eliminiación de horas de recurso
    
    Scenario Outline: eliminación de un registro de horas exitosamente
        Given un registro de horas con tarea <idTarea>, recurso <idRecurso> y fecha <fecha>
        When elimino el registro de horas 
        Then no existe ningun registro con ese codigo de carga
    
    Examples:
        | idRecurso | idTarea | fecha     |
        | 4         | 2       | 2021-10-2 |
        | 2         | 5       | 2022-03-2 |
        | 3         | 10      | 2022-04-2 |
        | 10        | 3       | 2022-02-2 |

        
    Scenario Outline: eliminación de un registro inexistente
        Given que no existe un registro de horas para la tarea <idTarea>, el recurso <idRecurso> y fecha <fecha> 
        When intento eliminar el registro de horas
        Then la eliminación debe ser denegada
    
    Examples:
        | idRecurso | idTarea | fecha     | cantidad |
        | 4         | 22      | 2022-01-2 | 5        | 
        | 5         | 2       | 2022-02-23| 8        | 
        | 4         | 3       | 2022-02-2 | 6        | 
        | 6         | 4       | 2022-03-22| 10        | 


    
