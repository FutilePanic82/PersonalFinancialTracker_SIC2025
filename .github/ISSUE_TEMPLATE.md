name: Bug Report
description: Report something that is not working as expected
title: "[Bug] "
labels: ["bug"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ## Describe el problema
        Describe claramente qué está fallando y cuál es el comportamiento esperado.

  - type: textarea
    id: steps
    attributes:
      label: Pasos para reproducir
      placeholder: |
        1. Ve a...
        2. Haz clic en...
        3. Observa el error...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Comportamiento esperado
      placeholder: Cuál debería ser el resultado correcto
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Comportamiento actual
      placeholder: Qué sucede actualmente
    validations:
      required: true

  - type: dropdown
    id: severity
    attributes:
      label: Severidad
      options:
        - Low
        - Medium
        - High
        - Critical
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Logs o stack trace (opcional)
      placeholder: Pegar aquí cualquier error relevante