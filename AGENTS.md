---
name: calculadora-3-6-9-agents
version: 4.0.0
schema: universal-agent-spec-v4
compatibility: [antigravity, opencode, cline, claude-code, cursor, commandcode, agy]
last_updated: 2026-08-13
priority: 100
allowed_tools: [view_file, write_to_file, replace_file_content, run_command, grep_search, search_web, read_url_content]
flags:
  strict_verification: true
  anti_slop: true
  no_destructive_commands: true
  require_empirical_proof: true
---

# AGENTS.md — CALCULADORA 3-6-9

Reglas operativas del proyecto para agentes de IA. Léelo completo antes de tocar cualquier archivo.

---

<kernel_directives>

## Propósito

Herramienta de precios de SAN LUIS PRO. Una sola ley sobre toda cifra que sale a cliente:

```
precio válido  ⟺  múltiplo de 50  ⟺  raíz digital ∈ {3,6,9}  ⟺  múltiplo de 150
```

Entre $600 y $5,400 hay exactamente **33 escalones** (paso de 150). Ni uno más.

## Fuentes de verdad (leer antes de actuar)

- `README.md` — doctrina, uso y procedencia de los números.
- `C:\Users\SAN LUIS PRO\OOAZ_FILES\00-SANLUISPRO\` — datos de negocio verificados (tarifas, reglas).
- `C:\Users\SAN LUIS PRO\OOAZ_FILES\AGENTS.md` — reglas universales del sistema.

## Comandos

```bash
# Corrida estándar del motor (salida a archivo)
cd "/c/Users/SAN LUIS PRO/OOAZ_FILES/PROYECTOS/CALCULADORA-3-6-9"
python motor_precios_sesion_150X.py > salida_motor.txt

# Gasolina base de evento editable sin tocar código
python motor_precios_sesion_150X.py --gasolina 300 > salida_motor.txt
```

La calculadora HTML no requiere comando: doble clic y abre en el navegador.

## Reglas inmutables

1. **La reja manda**: toda cifra nueva que salga a cliente debe caer en múltiplo de 150 dentro de la reja.
2. **Redondeo siempre arriba**: el ajuste sube al siguiente escalón. Nunca baja al previo.
3. **Cero tarifas inventadas**: todo número lleva etiqueta `VERIFICADO` (leído de disco), `INFERIDO` (flujo estándar) o `ESTIMADO` (sin ancla, calibrar con ventas). Sin etiqueta no es entregable.
4. **Complementos independientes**: hora extra de sesión de foto ($600) y hora extra de video ($1,500) son conceptos distintos. Prohibido anclarlos uno al otro.
5. **Material >25% del ticket** = paquete no rentable, se aborta.
6. **Ante objeción de precio**: recortar entregables, jamás descontar sobre la misma entrega.
7. **Anticipo del 50%** congela la fecha. Nada sale del estudio con saldo pendiente.

## Decisiones tomadas (no revertir sin orden)

- El **armado de paquetes** se eliminó de la calculadora: es dictaminador puro (validador + escalones + billetes + tema).
- El **añadible** se eliminó (nombre, precio y toggle).
- La **foto extra** quedó fija en **$30** y el **look** en **$150** (constantes internas del armado eliminado, no del motor).
- La **gasolina** del motor es editable por flag `--gasolina` (default 250), no por constante.
- `HORA_CAMPO_EXTRA` ($1,500) y `ANTICIPO` (50%) existen como datos verificados en el motor pero **no participan en la salida**. No eliminarlas ni amarrarlas a otras cifras sin orden expresa.

</kernel_directives>

<prohibited_actions>

1. No inventar precios, costos ni probabilidades. Usar los etiquetados o preguntar.
2. No mezclar las cifras de la calculadora (dictaminador) con las del motor (barrido financiero).
3. No borrar `salida_motor.txt` ni el README sin regenerar el primero.
4. No anclar la hora extra de sesión de foto ($600) a la hora extra de video ($1,500): son conceptos independientes.
5. No revertir decisiones tomadas (armado, añadible, tarifas fijas, gasolina por flag) sin orden expresa.

</prohibited_actions>

<operator_identity>

- Operador: OOAZ (Osiel Omar Aparicio Zamudio) — SAN LUIS PRO, fotografía y video.
- Proyecto: `C:\Users\SAN LUIS PRO\OOAZ_FILES\PROYECTOS\CALCULADORA-3-6-9\`
- En línea: https://calculadora-3-6-9.vercel.app · repo https://github.com/sanluispropublicidad-ai/calculadora-3-6-9
- Despliegue: `git push` a `main` redespliega solo en Vercel. El motor Python es local, no corre en Vercel.
- Negocio verificado: `C:\Users\SAN LUIS PRO\OOAZ_FILES\00-SANLUISPRO\`
- Reglas universales: `C:\Users\SAN LUIS PRO\OOAZ_FILES\AGENTS.md`
- No-técnico en construcción, experto en evaluación del resultado: entregar hecho, nunca tutorial.

</operator_identity>

<code_conventions>

- Español en UI, etiquetas y salidas.
- El motor Python fuerza UTF-8 en stdout (Windows cp1252 no debe romper el box-drawing).
- Sin placeholders, sin código muerto nuevo, sin sobre-ingeniería: cambiar solo lo pedido.
- Verificar después de tocar: `node --check` sobre el `<script>` del HTML y corrida del motor con `$LASTEXITCODE` en 0.

</code_conventions>

<error_handling>

- Si una corrida del motor falla: revisar `$LASTEXITCODE` y stderr antes de tocar lógica.
- Si el HTML no abre o el script truena: extraer el `<script>` y correr `node --check` para aislar el error de sintaxis.
- Ante duda de cifra: consultar `00-SANLUISPRO` o preguntar. Prohibido inventar el dato.

</error_handling>

<output_format>

- Respuestas cortas, BLUF: resultado primero, desglose escaneable después.
- Cifras con etiqueta de procedencia cuando se entregan: [VERIFICADO] [INFERIDO] [ESTIMADO].
- Reportar corridas con evidencia: exit code y líneas clave de `salida_motor.txt`.

</output_format>

<definition_of_done>

1. Motor: corre con `$LASTEXITCODE` 0 y `salida_motor.txt` regenerado.
2. HTML: `node --check` sin errores sobre el script.
3. Documentación: README y AGENTS.md coherentes con el estado real de los archivos.
4. Cero placeholders, cero cifras sin etiqueta, cero cambios fuera del alcance pedido.

</definition_of_done>

<protected_zones>

- `C:\Users\SAN LUIS PRO\OOAZ_FILES\00-SANLUISPRO\` — datos de negocio: solo lectura, jamás editar.
- `C:\Users\SAN LUIS PRO\OOAZ_FILES\AGENTS.md` — reglas universales: editar solo por orden expresa.
- `salida_motor.txt` — regenerable, nunca borrar sin regenerar.

</protected_zones>

---

<!-- DYNAMIC_RULES_START -->
- [2026-08-13] AGENTS.md creado al formato Híbrido SOTA v4.0 (frontmatter + tags XML + zona dinámica).
- [2026-08-13] Desplegado en Vercel: https://calculadora-3-6-9.vercel.app · repo público https://github.com/sanluispropublicidad-ai/calculadora-3-6-9 · push a main redespliega.
<!-- DYNAMIC_RULES_END -->