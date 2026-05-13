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

### Fase 1: CI/CD con GitHub Actions ✅
**Objetivo:** Pipeline automatizado para tests y lint en cada PR/push
**Criterios de éxito:**
- [x] `.github/workflows/ci.yml` creado
- [x] Job lint: ESLint (Angular) + ruff (Python)
- [x] Job test: Angular Karma/Jasmine + Python pytest (con test stubs)
- [x] Job build: Angular build + FastAPI syntax check
- [x] Docker build y docker-compose config check
**Archivos afectados:** `.github/workflows/ci.yml`, `chatbot-angular/package.json`, `Backend&Algorithms/requirements.txt`
**Estado:** completada

### Fase 2: Linting completo ✅
**Objetivo:** Code quality tools configuradas y ejecutándose
**Criterios de éxito:**
- [x] ESLint configurado en chatbot-angular con Angular recommended rules
- [x] ruff configurado en Backend&Algorithms (pyproject.toml)
- [x] TypeScript strict rules (noImplicitAny warnings enabled)
- [x] GitHub Actions ejecuta ambos linters en parallel
**Archivos afectados:** `chatbot-angular/.eslintrc.json`, `Backend&Algorithms/pyproject.toml`
**Estado:** completada

### Fase 3: Mejora de tests Angular ✅
**Objetivo:** Tests significativos que verifiquen comportamiento real
**Criterios de éxito:**
- [x] Tests de FinanzasService: mock HTTP con HttpClientTestingModule, verify endpoint calls
- [x] Coverage de todos los métodos del servicio (sendConversation, getHistorial, predict, finalize, resetChat, getReportes, metasAdvice)
**Archivos afectados:** `chatbot-angular/src/app/core/services/finanzas.service.spec.ts`
**Estado:** completada

### Fase 4: Tests backend Python con pytest ✅
**Objetivo:** Tests básicos para endpoints FastAPI
**Criterios de éxito:**
- [x] `tests/test_server.py` con tests de todos los endpoints
- [x] Tests de validacion (422 para inputs invalidos)
- [x] pytest.ini configurado con asyncio_mode auto
**Archivos afectados:** `Backend&Algorithms/tests/test_server.py`, `Backend&Algorithms/pytest.ini`
**Estado:** completada

### Fase 5: GitHub metadata ✅
**Objetivo:** Templates y configuración para colaboración
**Criterios de éxito:**
- [x] `.github/ISSUE_TEMPLATE.md` con bug report template
- [x] `.github/PULL_REQUEST_TEMPLATE.md`
- [x] `CONTRIBUTING.md` con setup instructions y convenciones
- [x] Dependabot configurado para npm + pip (updates semanales)
**Archivos afectados:** `.github/ISSUE_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `CONTRIBUTING.md`, `.github/dependabot.yml`
**Estado:** completada

### Fase 6: GitHub Actions badge y status checks ✅
**Objetivo:** enforce branch protection y mostrar estado en README
**Criterios de éxito:**
- [x] Badge de CI en README.md ([![CI]...](https://github.com/...))
- [x] CODEOWNERS configurado para backend
- [x] Dependabot badge en README
**Archivos afectados:** `.github/CODEOWNERS`, `README.md`
**Estado:** completada

## Estado por fase
| Fase | Nombre | Estado | Completada |
|------|--------|--------|------------|
| 1 | CI/CD con GitHub Actions | completada | 2026-05-13 |
| 2 | Linting completo | completada | 2026-05-13 |
| 3 | Mejora tests Angular | completada | 2026-05-13 |
| 4 | Tests backend Python | completada | 2026-05-13 |
| 5 | GitHub metadata | completada | 2026-05-13 |
| 6 | GitHub Actions badge | completada | 2026-05-13 |

## Siguiente paso
Hacer `git push` para activar el workflow de CI en GitHub Actions.
Luego configurar branch protection rules en Settings del repositorio:
- Require 1 reviewer para PRs
- Require status checks (lint, test, build) antes de merge