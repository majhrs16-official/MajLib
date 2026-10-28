# MajLib

> El arsenal de utilidades de escritorio y automatización de red forjado a pulso en la trinchera.

`MajLib` es una colección modular de componentes de interfaz gráfica minimalista, herramientas de red a bajo nivel y utilidades de sistema desarrolladas originalmente entre **2018 y 2021** (en pleno entorno offline, bajo Python 3.4+ e IDLE). Este repositorio recopila las reliquias rescatadas de MediaFire y viejos respaldos, preservando su código intacto.

## Estructura del Repositorio

```text
.
├── Tk.py                         # Extensión de Tkinter con gestión de contexto (with) y helpers dinámicos
├── Sh.py                         # Navaja suiza de sistema: barras de terminal, sockets, IPs y utilidades
├── BinaryTranslator.py           # Aplicación de traducción de texto a binario en tiempo real con hilos
├── ListenMic.py                  # Herramienta de captura y monitoreo de audio por micrófono
├── RecordTwoMic.py               # Utilidad de grabación multicanal de audio
├── RefreshHost.py                # Automatización de actualizacion del dominio FreeMyIP
├── Minecraft Assets Extractor.py # Extractor de recursos y assets de Minecraft
└── proxymc/                      # Proxy TCP multihilo para Minecraft con dashboard de terminal en vivo
    ├── Proxy.py                  # Núcleo de redirección de bytes a bajo nivel
    └── UI.py                     # Interfaz de monitoreo de ancho de banda y conexiones por consola

```

## Componentes Destacados

### 1. `Tk.py` (Magia Negra de Tkinter)

Un *monkey-patch* a Tkinter para acelerar el desarrollo de GUIs mediante administradores de contexto (expresion `with`):

* **Soporte de Context Managers:** Inicialización de ventana principal y contenedores con `with Tk() as app:`, ejecutando el `mainloop` automáticamente al salir del bloque.
* **Componentes Autocontenidos:** Clases como `Text` que integran scrollbars automáticas y absorben dinámicamente los métodos de geometría (`pack`, `grid`, `place`).

### 2. `Sh.py` (Utilidades de Sistema y Red)

Librería ultra ligera orientada a resolver tareas comunes sin dependencias externas:

* **Detección de IP Local:** Obtención de la interfaz activa mediante sockets UDP (`8.8.8.8`) sin enviar tráfico real.
* **Barra de Progreso en Terminal:** Renderizado en consola mediante caracteres Unicode (`█`) con retorno de carro (`\r`).
* **Decorador de Hilos (`@dThread`):** Simplificación para crear y ejecutar hilos daemonizados en segundo plano.

### 3. `ProxyMC` (Monitoreo de Red en Tiempo Real)

Un proxy TCP completo diseñado para Minecraft que intercepta, redirige y calcula tasas de transferencia (`IOps`) por cliente, mostrando un panel de control dinámico directamente en la terminal.

## Requisitos

* **Python 3.4+** (Diseñado originalmente para correr en entornos minimalistas y versiones clásicas de Windows sin SP1).
* Sin dependencias de terceros obligatorias para los módulos base (`Tk` y `Sh` utilizan exclusivamente la librería estándar de Python).

---

### Licencia

Este proyecto se distribuye bajo los términos de la **GNU General Public License v3.0**. Consulta el archivo de licencia o los encabezados en el código fuente para más detalles.
