# Web Scraper Project

Ejercicio de gestión de entornos virtuales y dependencias con `uv`.

## Configurar el entorno de desarrollo

Desde la carpeta `scrape_project`, ejecutar los siguientes comandos en PowerShell.

**1. Crear el entorno virtual**

```powershell
uv venv
```

**2. Activar el entorno**

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Sincronizar las dependencias de desarrollo**

```powershell
uv pip sync requirements-dev.txt
```

**4. Ejecutar los tests**

```powershell
python -m pytest
```

## Dependencias

- `requirements-base.in`: dependencias directas de producción.
- `requirements-dev.in`: dependencias de desarrollo, incluidas las de producción.
- `requirements-base.txt`: versiones bloqueadas para producción.
- `requirements-dev.txt`: versiones bloqueadas para desarrollo.

Para regenerar los archivos bloqueados después de modificar las dependencias:

```powershell
uv pip compile requirements-base.in -o requirements-base.txt
uv pip compile requirements-dev.in -o requirements-dev.txt
```

## Git

Los entornos virtuales `.venv` no se incluyen en el repositorio. Se reconstruyen utilizando `uv` y los archivos de dependencias versionados.
