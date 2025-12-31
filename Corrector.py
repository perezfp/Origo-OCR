from openai import OpenAI  # Cambiado para usar el nuevo cliente
import tiktoken
import time
from pathlib import Path

# === CONFIGURACIÓN ===
# IMPORTANTE: Coloca tu API Key aquí o usa variables de entorno
client = OpenAI(api_key="TU_API_KEY_DE_OPENAI_AQUI")

INPUT_FILE = "texto_extraido.txt"      # Archivo de entrada
OUTPUT_FILE = "texto_corregido.txt"    # Archivo de salida
MODEL = "gpt-4o-mini"                  # Modelo optimizado para esta tarea
SPLIT_STRING = "\n\n"                  # Criterio de división
MAX_ATTEMPTS = 5                       
RETRY_GAP = 3.0                        

# === PROMPT DEL CORRECTOR ===
SYSTEM_PROMPT = """Eres un corrector experto.
Corrige el siguiente texto en español:
- Ortografía, Gramática y Puntuación.
- Formato: Elimina saltos de línea incorrectos y une palabras interrumpidas por guiones.
- Limpieza: Elimina frases interrumpidas por la maquetación o numeraciones de página (ej: ---Página n--).

**REGLAS CRÍTICAS:**
1. Mantén el estilo y sentido original del autor.
2. No modernices el lenguaje; conserva la ortografía original si es válida históricamente.
3. Devuelve SOLO el texto corregido, sin comentarios adicionales.
"""

# === LECTURA DEL ARCHIVO ===
try:
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        text = f.read()
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo {INPUT_FILE}")
    exit()

# Estimación de tokens
encoding = tiktoken.encoding_for_model("gpt-4")
encoded_text = encoding.encode(text)
print(f"📝 Texto cargado: {len(text)} caracteres (~{len(encoded_text)} tokens)")

# === DIVIDIR EN BLOQUES ===
chunks = [c.strip() for c in text.split(SPLIT_STRING) if c.strip()]
print(f"📦 Se dividió en {len(chunks)} bloques.")

# === PROCESAR Y CORREGIR ===
results = []
tokens_consumed = 0

for i, chunk in enumerate(chunks, start=1):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": chunk}
    ]

    current_retry_gap = RETRY_GAP
    for attempt in range(MAX_ATTEMPTS):
        try:
            # Nueva sintaxis del cliente OpenAI
            completion = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.0
            )
            
            # Acceso por atributos en lugar de diccionarios
            corrected = completion.choices[0].message.content
            results.append(corrected)
            tokens_consumed += completion.usage.total_tokens
            
            print(f"✅ Bloque {i}/{len(chunks)} corregido.")
            break
            
        except Exception as e:
            print(f"⚠️ Error en bloque {i} intento {attempt+1}: {e}")
            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(current_retry_gap)
                current_retry_gap *= 1.5
            else:
                print(f"❌ Falló el bloque {i} tras {MAX_ATTEMPTS} intentos. Se omitirá.")
                results.append(f"[ERROR EN BLOQUE {i}]")

# === GUARDAR RESULTADO ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(SPLIT_STRING.join(results))

print(f"\n🎉 Proceso finalizado.")
print(f"💾 Guardado en: {OUTPUT_FILE}")
print(f"📊 Total tokens consumidos: {tokens_consumed}")
