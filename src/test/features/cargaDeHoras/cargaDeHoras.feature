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

#   Scenario Outline: no se pueden cargar horas a una tarea de un recurso que no tiene asignado
#     Given un recurso con ID <idRecurso> 
#     And una tarea con ID <idTarea>
#     And el recurso no está asignado a la tarea
#     When intento cargar <cantidad> horas trabajadas del recurso a la tarea para la fecha <fecha>
#     Then la carga debe ser denegada
#     And la tarea tendrá 0 horas consumidas del recurso

# #   Examples:
# #       | idRecurso | idTarea | tituloTarea   | cantidad | fecha      |
# #       | 12        | 23      | "Refactorizar"| 1        | 5-12-2021  |
# #       | 5         | 5       | "Debuggear"   | 2        | 7-10-2022  |
# #       | 23        | 3       | "Testing"     | 7        | 14-05-2022 |

#   Scenario Outline: no se pueden cargar horas de un recurso a una tarea que no existe
#     Given un recurso con ID <id>
#     And el recurso realiza un trabajo sobre una tarea que no existe
#     When intento cargar <cantidad> horas trabajadas a una tarea que no existe para la fecha <fecha>
#     Then la carga debe ser denegada por ingresar mal la tarea

# #   Examples:
# #       | id | cantidad | fecha      |
# #       | 0  | 1        | 25-05-2022 |
# #       | 1  | 0        | 07-01-2022 |
# #       | 2  | 7        | 04-02-2022 |

#   Scenario Outline: no se pueden cargar horas de un recurso que no existe a una tarea
#     Given una tarea con título <tituloTarea>
#     And se realiza un trabajo sobre la tarea
#     When intento cargar <cantidad> horas trabajadas del recurso que no existe a la tarea para la fecha <fecha>
#     Then la carga debe ser denegada por ingresar mal el recurso

# #   Examples:
# #       | cantidad | tituloTarea    | fecha      |
# #       | 1        | "Refactorizar" | 27-04-2021 |
# #       | 0        | "Debuggear"    | 06-12-2021 |
# #       | 7        | "Testing"      | 9-09-2022  |
  
#   Scenario Outline: carga de horas excede el límite diario
#     Given un recurso con ID <id> 
#     And una tarea con título <tituloTarea>
#     And el recurso está asignado a la tarea
#     And el recurso no tiene horas cargadas en la tarea
#     When intento cargar <cantidad> horas de un recurso a una tarea superando el límite diario permitido para la fecha <fecha>
#     Then la carga debe ser denegada por superar el límite diario
#     Then la tarea tendrá 0 horas consumidas de recurso

# #   Examples:
# #     | id | tituloTarea   | cantidad | fecha      |
# #     | 10 | "Refactorizar"| 15       | 11-06-2022 |
# #     | 11 | "Debuggear"   | 13       | 19-07-2022 |
# #     | 12 | "Testing"     | 9        | 10-07-2020 |

#   Scenario Outline: carga de horas no alcanza el mínimo a cargar
#     Given un recurso con ID <id> 
#     And una tarea con título <tituloTarea>
#     And el recurso está asignado a la tarea
#     And el recurso no tiene horas cargadas en la tarea
#     When intento cargar <cantidad> horas de un recurso a una tarea no alcanzando el mínimo diario para la fecha <fecha>
#     Then la carga debe ser denegada por no alcanzar el mínimo de carga de horas
#     Then la tarea tendrá 0 horas consumidas de recurso

#     Examples:
#       | id | tituloTarea   | cantidad | fecha      |
#       | 20 | "Refactorizar"| 0.1      | 04-09-2022 |
#       | 21 | "Debuggear"   | 0        | 25-06-2022 |
#       | 12 | "Testing"     | 0.9      | 10-12-2020 |

#   Scenario Outline: no se pueden cargar horas a una fecha del futuro
#     Given un recurso con ID <id> 
#     And una tarea con título <tituloTarea>
#     And el recurso está asignado a la tarea
#     And el recurso no tiene horas cargadas en la tarea
#     When intento cargar <cantidad> horas de un recurso a una tarea para el día <fecha>
#     Then la carga debe ser denegada por no ser para una fecha del pasado
#     Then la tarea tendrá 0 horas consumidas de recurso

# #   Examples:
# #       | id | tituloTarea   | cantidad | fecha      |
# #       | 2  | "Refactorizar"| 1        | 11-06-2023 |
# #       | 5  | "Debuggear"   | 6        | 1-01-2023  |
# #       | 0  | "Testing"     | 7        | 5-09-2023  | 