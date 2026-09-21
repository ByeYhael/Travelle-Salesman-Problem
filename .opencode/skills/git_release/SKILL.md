---
name: git_release
description: "Gestiona un repositorio git para un proyecto: git init, .gitignore, README, commits, versionado semántico, tags y releases (git tag y gh release). GENÉRICA. Incluye comandos y convenciones."
---

# Git Release (genérica)

Empaqueta y versiona un proyecto en git con control de versiones y releases.

## Procedimiento genérico

### 1. Inicializar y configurar
```bash
git init
git branch -M main
```

### 2. `.gitignore`
Excluir siempre: artefactos generados, resultados, cachés y dependencias.
```gitignore
# Resultados y temporales
outputs/
__pycache__/
*.pyc
.ipynb_checkpoints/

# Entorno / dependencias
node_modules/
.env
venv/
.venv/
```
> Si ya existe `.gitignore`, **añadir** (no borrar) las entradas faltantes.

### 3. `README.md`
Documentar: qué hace el proyecto, estructura de carpetas, requisitos, cómo ejecutar y cómo interpretar los resultados. Mantener conciso.

### 4. Primer commit
```bash
git add .
git commit -m "chore: estructura inicial"
```

### 5. Versionado semántico (SemVer)
`MAJOR.MINOR.PATCH`:
- **MAJOR**: cambios incompatibles.
- **MINOR**: funcionalidad nueva compatible.
- **PATCH**: correcciones.

### 6. Tags (versiones)
```bash
git tag -a v0.1.0 -m "release 0.1.0: estructura del ecosistema"
git tag -a v0.2.0 -m "release 0.2.0: datos y matriz de distancias"
git tag -a v0.3.0 -m "release 0.3.0: ejecución del algoritmo genético"
git tag -a v0.4.0 -m "release 0.4.0: resultados y gráficas"
git push origin --tags
```

### 7. GitHub Releases (opcional, con `gh`)
```bash
gh release create v0.4.0 --title "Release 0.4.0" --notes "Resultados finales"
```

## Reglas
- NO exponer secretos; verificar que no se commitean `.env` ni claves.
- Revisar `git status` y `git diff` antes de cada commit.
- Mensajes de commit descriptivos y en minúscula inicial.
- Confirmar con el usuario antes de hacer `push` o publicar releases.