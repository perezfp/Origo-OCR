from openai import OpenAI
import re
import time

client = OpenAI(
    api_key="tu_api_key_de_deepseek_aqui",
    base_url="https://api.deepseek.com/v1"
)

# === CONFIGURACIÓN ===
INPUT_FILE = "texto_corregido.txt"
OUTPUT_FILE = "texto_final.txt"
MODEL = "deepseek-chat"
SPLIT_STRING = "\n\n"
MAX_ATTEMPTS = 3
RETRY_GAP = 2.0

# === PROMPT ETAPA 2 (REFINAMIENTO) ===
SYSTEM_PROMPT_REFINAMIENTO = """Eres un editor experto en textos históricos en español.
Tu tarea es REFINAR el texto que recibes, que ya ha pasado por una primera corrección.

Enfócate en:
1. FLUIDEZ Y COHERENCIA: Mejora la fluidez del texto, asegurando que las frases sean naturales
2. CONSISTENCIA: Uniformiza estilo, terminología y formato
3. ELIMINAR REDUNDANCIAS: Quita repeticiones innecesarias
4. MEJORAR ESTRUCTURA: Asegura párrafos bien estructurados
5. CONSERVAR esencia histórica y estilo original

**CRÍTICAMENTE IMPORTANTE:**
- NO agregues saltos de línea arbitrarios
- Mantén el texto como flujo continuo natural
- Respeta absolutamente el contenido histórico original
- Solo mejora la presentación, no alteres el significado

Devuelve SOLO el texto refinado, sin comentarios.
"""

# === LECTURA DEL TEXTO CORREGIDO ===
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Dividir en bloques más grandes para refinamiento
chunks = text.split(SPLIT_STRING)
print(f"Texto para refinamiento dividido en {len(chunks)} bloques.")

# === REFINAMIENTO SEGUNDA ETAPA ===
refined_results = []
for i, chunk in enumerate(chunks, start=1):
    if not chunk.strip() or len(chunk.strip()) < 50:
        refined_results.append(chunk)
        continue

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_REFINAMIENTO},
        {"role": "user", "content": f"Texto a refinar:\n\n{chunk}"}
    ]

    for attempt in range(MAX_ATTEMPTS):
        try:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.1  # Un poco de creatividad para refinamiento
            )
            refined = completion.choices[0].message.content
            refined_results.append(refined)
            print(f"🎯 Bloque {i}/{len(chunks)} refinado (Etapa 2).")
            break
        except Exception as e:
            print(f"⚠️ Error refinando bloque {i}: {e}")
            if attempt < MAX_ATTEMPTS - 1:
                time.sleep(RETRY_GAP)
            else:
                refined_results.append(chunk)  # Mantener si falla

# === GUARDAR RESULTADO FINAL ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(SPLIT_STRING.join(refined_results))

print(f"\n🎉 Proceso completo! Texto refinado guardado en {OUTPUT_FILE}")
