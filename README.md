# Scripts de digitalizacion de textos

Este proyecto automatiza la transformación de documentos físicos (PDFs escaneados) en texto digital de alta calidad. A diferencia de un OCR convencional que suele entregar resultados con ruidos de lectura, este sistema implementa un flujo de trabajo en tres etapas que garantiza la fidelidad histórica y la fluidez narrativa.


# Arquitectura del Pipeline
El sistema se divide en tres módulos especializados que deben ejecutarse secuencialmente:

**1. Extracción (OCR.PY)**

  Tecnología: pytesseract + pdf2image.

  Función: Convierte las páginas de un PDF en imágenes y realiza el reconocimiento óptico de caracteres inicial.

  Salida: Un archivo de texto bruto (.txt) con el contenido crudo del documento.

**2. Corrección Ortotipográfica (Corrector.py)**

  Tecnología: OpenAI API (gpt-4o-mini).

  Función: Limpieza inteligente del ruido del OCR.

  Acciones: Elimina saltos de línea arbitrarios, reconstruye palabras cortadas por guiones al final de página y elimina cabeceras/numeración de página, todo esto manteniendo el léxico     original.

**3. Refinamiento Estilístico (refinador.py)**

  Tecnología: DeepSeek API (deepseek-chat).

  Función: Actúa como un editor experto en textos históricos.

  Acciones: Mejora la fluidez y coherencia del texto corregido, asegurando que la estructura de los párrafos sea natural sin alterar el significado o la esencia del autor original.
