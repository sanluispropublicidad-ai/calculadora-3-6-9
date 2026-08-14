# CALCULADORA 3-6-9

[![STATUS](https://img.shields.io/badge/STATUS-OPERATIONAL-brightgreen)](https://github.com/agntcy/dir-agent-ts)
[![REJA](https://img.shields.io/badge/REJA-150X-red)](https://github.com/agntcy/dir-agent-ts)
[![STACK](https://img.shields.io/badge/STACK-HTML%2BJS%2BPython-9cf)](https://github.com/agntcy/dir-agent-ts)
[![LANG](https://img.shields.io/badge/LANG-Español-lightgrey)](https://github.com/agntcy/dir-agent-ts)
[![DOCTRINA](https://img.shields.io/badge/DOCTRINA-33X-important)](https://github.com/agntcy/dir-agent-ts)

Herramienta de precios para SAN LUIS PRO. Impone una sola ley sobre toda cifra que sale a cliente:
un precio se emite únicamente si termina en múltiplo de **50** y su **raíz digital** cae en **3**, **6** o **9**.

---

## La ley de la reja

Las dos condiciones parecen independientes. No lo son.

La raíz digital de un número es divisible entre 3 solo cuando el número lo es. Entonces:

```
raíz digital ∈ {3, 6, 9}   ⟺   n divisible entre 3
n múltiplo de 50 y divisible entre 3   ⟺   n múltiplo de 150
```

**Las dos pruebas colapsan en una:** el precio debe ser múltiplo de 150.

Entre $600 y $5,400 existen exactamente **33 escalones válidos**. Ni uno más.

```
600   750   900  1050  1200  1350  1500  1650
1800  1950  2100  2250  2400  2550  2700  2850
3000  3150  3300  3450  3600  3750  3900  4050
4200  4350  4500  4650  4800  4950  5100  5250
5400
```

Cifras que reprueban aunque terminen en 50: **$950** (raíz 5), **$1,900** (raíz 1), **$3,200** (raíz 5), **$4,900** (raíz 4).

---

## Contenido de la carpeta

| Archivo | Qué es |
| :--- | :--- |
| `CALCULADORA_REJA_150X.html` | Dictaminador de reja. Se abre en el navegador, sin instalar nada. |
| `index.html` | Redirige a la calculadora. Punto de entrada del despliegue en línea. |
| `motor_precios_sesion_150X.py` | Motor de barrido con la Ecuación Maestra V3.3. Corre en Git Bash. |
| `salida_motor.txt` | Última corrida del motor, cuatro configuraciones en base 3. |
| `README.md` | Este archivo: doctrina, uso y procedencia de los números. |
| `AGENTS.md` | Reglas operativas del proyecto para agentes de IA. |

---

## En línea

La calculadora está desplegada en Vercel, servida desde un repo público de GitHub:

- **URL en vivo:** https://calculadora-3-6-9.vercel.app
- **Repo:** https://github.com/sanluispropublicidad-ai/calculadora-3-6-9

Cualquier `git push` a `main` redespliega solo. El motor Python es local: no corre en Vercel.

---

## Calculadora

Doble clic en `CALCULADORA_REJA_150X.html`. Es un dictaminador puro, sin armado de paquetes.

**Validador.** Teclado numérico —también responde al teclado físico, con Backspace y Escape— que
dictamina cualquier cifra: si es múltiplo de 50, la suma de sus dígitos escrita completa, su raíz
digital y su escalón. Cuando rechaza, ofrece el escalón de arriba y el de abajo para saltar directo.

**Escalones.** La cinta completa de la reja, de $600 a $5,400. Un toque la lleva al dictamen.

**Extras de lectura.** Desglose de billetes de $100/$50 para la cifra dictaminada, y tema claro/oscuro.

> [!WARNING]
> El redondeo de la casa **siempre sube** al siguiente escalón. Nunca baja al escalón previo.

---

## Motor de barrido

```bash
cd "/c/Users/SAN LUIS PRO/OOAZ_FILES/PROYECTOS/CALCULADORA-3-6-9"
python motor_precios_sesion_150X.py > salida_motor.txt
```

La gasolina base de evento se cambia sin tocar código:

```bash
python motor_precios_sesion_150X.py --gasolina 300 > salida_motor.txt
```

Fuerza la consola a UTF-8 por dentro, así que no truena con el cp1252 de Windows.

Calcula desde la física del jale —traslado, captura, selección, edición, administración— y de ahí
deriva el piso en reja para varias pagas por hora objetivo. Además barre cada escalón calculando
utilidad, paga por hora y utilidad esperada ponderada por probabilidad de cierre.

Compara cuatro configuraciones de contenido en base 3: `6-15-30`, `6-18-36`, `9-18-36` y `3-9-27`,
más el servicio aislado de gala/producción.

**Hallazgo central de la última corrida:** la paga por hora *sube* conforme el paquete crece. El
arranque fijo —salir, montar, volver, administrar— vale alrededor de 1.5 horas y se paga completo
aunque entregues seis fotos. En un paquete grande ese arranque se diluye entre más entregables. Por
eso el paquete chico es el que peor paga tu tiempo, y por eso vender solo el gancho es la peor
estrategia posible.

---

## Procedencia de los números

Cada dato lleva etiqueta. Sin etiqueta no es entregable.

**VERIFICADO** — leído de `00-SANLUISPRO`: gasolina base de evento $250, gasto hormiga $350, foto
impresa $5.50, tope de material 25% del ticket, anticipo 50%, vigencia de cotización 5 días naturales,
hora extra de video en campo $1,500, sesión de gala aislada $4,500 a $5,500.

**INFERIDO** — flujo estándar de retoque, sin ancla documental: edición fina de 7 minutos por foto,
administración 0.70 hr, traslado a 45 km/h promedio en carretera huasteca.

**ESTIMADO** — sin ancla de ninguna clase: la curva de probabilidad de cierre y el costo de atender un
lead. Son hipótesis. **Calibrar con ventas reales contadas** antes de tratarlas como hecho.

La calculadora HTML no usa ninguna capa de datos del motor: es un dictaminador puro. El motor Python
usa VERIFICADO + INFERIDO + ESTIMADO, y por eso sus óptimos son propuestas, no veredictos.

> [!IMPORTANT]
> Los complementos del motor tienen precios independientes entre sí: hora extra de **sesión de foto**
> $600 y hora extra de **video** $1,500 son dos conceptos distintos. No se amarran uno al otro.

---

## Reglas de negocio que la herramienta respalda

- Material arriba del **25%** del ticket vuelve el paquete no rentable. Se aborta.
- Ante objeción de precio se **recortan entregables**, jamás se descuenta sobre la misma entrega.
- La fecha se congela solo con el **50%** de anticipo depositado.
- Nada sale del estudio con saldo pendiente.

---

## Árbol de archivos

```
CALCULADORA-3-6-9/
├── CALCULADORA_REJA_150X.html   # dictaminador de reja (navegador)
├── index.html                   # entrada del despliegue en línea
├── motor_precios_sesion_150X.py # motor de barrido (Python)
├── salida_motor.txt             # última corrida del motor
├── README.md                    # doctrina y uso
└── AGENTS.md                    # reglas operativas para agentes
```

---

Sellado jueves 13 de agosto de 2026, 17:25 hrs (hora local, verificada con `date`).

`[VERIFICADO] [SAN LUIS PRO] [DOCTRINA 33X] [SISTEMA SOTA 2026]`