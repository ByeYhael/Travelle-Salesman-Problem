# git_release_agent — Prompt (genérico)

Empaqueta el proyecto en git: inicializa el repositorio (rama main), actualiza `.gitignore` y `README.md`, hace commits descriptivos y versiona por releases con tags SemVer (`v0.1.0`…`v0.4.0`). Opcional: publicar con `gh release`. Revisa status/diff antes de commitear; no expongas secretos; confirma antes de push/release.