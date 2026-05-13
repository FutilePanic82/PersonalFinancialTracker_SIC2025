# Plan: Mejoras de calidad GitHub para PersonalFinancialTracker_SIC2025
**Fecha:** 2026-05-13
**Estado global:** en progreso

## Contexto
Repositorio Angular 19 + FastAPI con ML. Detectado:
- Sin CI/CD (no .github/workflows)
- Sin linters (ESLint ausent, ruff/pylint ausentes)
- Tests triviales (solo toBeTruthy), sin tests en backend Python
- CORS hardcoded localhost, sin auth, sin rate limiting
- Code smells: duplicación, globals no thread-safe, violation SRP

## Fases

### Fase 1: CI/CD con GitHub Actions
**Objetivo:** Pipeline automatizado para tests y lint en cada PR/push
**Criterios de éxito:**
- [ ] `.github/workflows/ci.yml` creado
- [ ] Job lint: ESLint (Angular) + ruff (Python)
- [ ] Job test: Angular Karma/Jasmine + Python pytest (con test stubs)
- [ ] Job build: Angular build + FastAPI syntax check
- [ ] Secrets configurados para no hardcodear tokens
**Archivos afectados:** `.github/workflows/ci.yml`, `chatbot-angular/package.json`, `Backend&Algorithms/requirements.txt`
**Estado:** pendiente

### Fase 2: Linting completo
**Objetivo:** Code quality tools configuradas y ejecutándose
**Criterios de éxito:**
- [ ] ESLint configurado en chatbot-angular con Angular recommended rules
- [ ] ruff configurado en Backend&Algorithms (取代 pylint más rápido)
- [ ] Configuración máxima strict para TypeScript (noImplicitAny, strictNullChecks)
- [ ] GitHub Actions ejecuta ambos linters en parallel
**Archivos afectados:** `chatbot-angular/.eslintrc.json`, `Backend&Algorithms/pyproject.toml` (o `.ruff.toml`)
**Estado:** pendiente

### Fase 3: Mejora de tests Angular
**Objetivo:** Tests significativos que verifiquen comportamiento real
**Criterios de éxito:**
- [ ] Tests de FinanzasService: mock HTTP, verify endpoint calls
- [ ] Tests de componentes: verify user interaction, not just render
- [ ] Coverage mínimo 50% (configurable en angular.json)
**Archivos afectados:** `chatbot-angular/src/app/**/*.spec.ts`
**Estado:** pendiente

### Fase 4: Tests backend Python con pytest
**Objetivo:** Tests básicos para endpoints FastAPI
**Criterios de éxito:**
- [ ] `Backend&Algorithms/test_server.py` con tests de endpoints
- [ ] Tests de classifier.py y predictor.py (mockeando ML pesado)
- [ ] pytest.ini configurado
**Archivos afectados:** `Backend&Algorithms/test_server.py`, `Backend&Algorithms/pytest.ini`
**Estado:** pendiente

### Fase 5: GitHub metadata
**Objetivo:** Templates y configuración para colaboración
**Criterios de éxito:**
- [ ] `.github/ISSUE_TEMPLATE.md` con bug/feature templates
- [ ] `.github/PULL_REQUEST_TEMPLATE.md`
- [ ] `CONTRIBUTING.md` con setup instructions
- [ ] Dependabot configurado para npm + pip
**Archivos afectados:** `.github/ISSUE_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `CONTRIBUTING.md`, `.github/dependabot.yml`
**Estado:** pendiente

### Fase 6: GitHub Actions badge y status checks
**Objetivo:** enforce branch protection y mostrar estado en README
**Criterios de éxito:**
- [ ] Branch protection: require 1 reviewer, status checks mandatory
- [ ] Badge de CI en README.md
- [ ] CODEOWNERS configurado
**Archivos afectados:** `.github/CODEOWNERS`, `README.md`
**Estado:** pendiente

## Estado por fase
| Fase | Nombre | Estado | Completada |
|------|--------|--------|------------|
| 1 | CI/CD con GitHub Actions | pendiente | - |
| 2 | Linting completo | pendiente | - |
| 3 | Mejora tests Angular | pendiente | - |
| 4 | Tests backend Python | pendiente | - |
| 5 | GitHub metadata | pendiente | - |
| 6 | GitHub Actions badge | pendiente | - |

## Dependencias
- Fase 2 (Linting) puede ejecutarse en paralelo con Fase 1 (CI) ya que son independientes
- Fase 3 y 4 pueden ejecutarse en paralelo (frontend vs backend)
- Fase 5 y 6 dependen de que CI funcione primero