Feature: carga de horas de recurso

  Scenario Outline: carga de horas a una tarea de un recurso que tiene asignado
    Given un recurso con ID <idRecurso> 
    And una tarea con ID <idTarea>
    And el recurso está asignado a la tarea
    And la tarea no tiene horas cargadas del recurso
    When intento cargar <cantidad> horas trabajadas del recurso a la tarea para la fecha <fecha>
    Then se registran <cantidad> horas consumidas por la tarea del recurso

  Examples:
      | idRecurso | idTarea       | cantidad | fecha      |
      | 7         | 1             | 5        | 2021-06-10 |
      | 9         | 2             | 3        | 2021-06-08 |
      | 43        | 3             | 8        | 2021-06-01 |

  Scenario Outline: no se pueden cargar horas a una tarea de un recurso que no tiene asignado
    Given un recurso con ID <idRecurso> 
    And una tarea con ID <idTarea>
    And el recurso no está asignado a la tarea
    When intento cargar <cantidad> horas trabajadas a la tarea del recurso que no tiene asignado para la fecha <fecha>
    Then la carga debe ser denegada
    And la tarea tendrá 0 horas consumidas del recurso

  Examples:
        | idRecurso | idTarea | cantidad | fecha      |
        | 12        | 23      | 1        | 2021-12-05 |
        | 5         | 5       | 2        | 2022-01-7  |
        | 23        | 3       | 7        | 2022-05-14 |

  Scenario Outline: no se pueden cargar horas de un recurso a una tarea que no existe
    Given un recurso con ID <id>
    When intento cargar <cantidad> horas trabajadas a una tarea que no existe para la fecha <fecha>
    Then la carga debe ser denegada por no seleccionar una tarea existente

  Examples:
    | id | cantidad | fecha      |
    | 0  | 1        | 2022-05-25 |
    | 1  | 2        | 2022-01-07 |
    | 2  | 7        | 2022-02-04 |

  Scenario Outline: no se pueden cargar horas de un recurso que no existe a una tarea
    Given una tarea con ID <idTarea>
    When intento cargar <cantidad> horas trabajadas a la tarea de un recurso que no existe para la fecha <fecha>
    Then la carga debe ser denegada por ingresar mal el recurso

  Examples:
      | cantidad | idTarea | fecha      |
      | 1        | 23      | 2021-04-27 |
      | 3        | 32      | 2021-12-06 |
      | 7        | 99      | 2022-03-09  |
  
  Scenario Outline: carga de horas excede el límite diario
    Given un recurso con ID <id> 
    And una tarea con ID <idTarea>
    And el recurso está asignado a la tarea
    And la tarea no tiene horas cargadas del recurso
    When intento cargar <cantidad> horas de un recurso a una tarea para la fecha <fecha>, incumpliendo el rango de horas permitido
    Then la carga debe ser denegada por superar el límite diario
    Then la tarea tendrá 0 horas consumidas del recurso

  Examples:
    | id | idTarea | cantidad | fecha      |
    | 10 | 52      | 15       | 2022-06-11 |
    | 11 | 27      | 13       | 2022-04-19 |
    | 12 | 105     | 9        | 2020-07-10 |
    | 20 | 223     | -1       | 2022-03-04 |
    | 21 | 34      | 0        | 2022-06-25 |
    | 12 | 521     | -3       | 2020-12-10 |

  Scenario Outline: no se pueden cargar horas a una fecha del futuro
    Given un recurso con ID <id> 
    And una tarea con ID <idTarea>
    And el recurso está asignado a la tarea
    And la tarea no tiene horas cargadas del recurso
    When intento cargar <cantidad> horas de un recurso a una tarea para la <fecha> que todavía no pasó
    Then la carga debe ser denegada por no ser para una fecha del pasado
    And la tarea tendrá 0 horas consumidas del recurso

  Examples:
      | id | idTarea | cantidad | fecha      |
      | 2  | 31      | 1        | 2023-06-11 |
      | 5  | 72      | 6        | 2023-01-01 |
      | 0  | 236     | 7        | 2023-09-05 |