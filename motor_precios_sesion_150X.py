#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MOTOR DE PRECIOS — SESIONES FOTOGRÁFICAS · SAN LUIS PRO
=========================================================
Regla de reja OOAZ:
  · Redondeo de 50 (nunca 20 ni 80)
  · Raíz digital del precio ∈ {3, 6, 9}  (gematría Tesla)
  · Ambas condiciones a la vez  ⟺  el precio es múltiplo de 150

Demostración: raíz_digital(N) ∈ {3,6,9} ⟺ N divisible por 3.
              N múltiplo de 50 y divisible por 3 ⟺ N múltiplo de 150.

Motor financiero: Ecuación Maestra V3.3 (dos momentos)
  Π_exec = P − (M + Λ + hormiga) − wT
  Π_lead = q_book × Π_exec − C_quote
"""

from math import exp, ceil
import sys, io, argparse

# Consola Windows en cp1252: forzar UTF-8 o el box-drawing truena
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ═══════════════════════════════════════════════════════════════════
# BLOQUE 1 · PARÁMETROS
# ═══════════════════════════════════════════════════════════════════

# --- VERIFICADO en disco (00-SANLUISPRO) ---
GASOLINA_EVENTO   = 250.00   # tablas bautizo/comunión
GASTO_HORMIGA     = 350.00   # colchón por evento (Checklist Maestro)
COSTO_FOTO_IMPRESA=   5.50   # SERVICIOS Y VARIABLES · costos directos
TOPE_MATERIAL     =   0.25   # >25% del ticket = paquete NO rentable
HORA_CAMPO_EXTRA  = 1500.00  # Ley 1 · hora extra de video en efectivo
ANTICIPO          =   0.50

# --- INFERIDO (flujo estándar de retoque, no hay dato en disco) ---
MIN_EDICION_FOTO  =   7.0    # minutos de edición fina por foto
MIN_EDICION_GALA  =   8.0    # edición fina de producción
HR_ADMIN          =   0.70   # descarga, respaldo, WhatsApp, entrega
HR_CULL_BASE      =   0.15
HR_CULL_X_FOTO    =   0.008
HR_CAPTURA_BASE   =   0.40
HR_CAPTURA_CAMBIO =   0.55

# --- ESTIMADO (sin ancla en disco · calibrar con ventas reales) ---
HORA_OBJETIVO     = 350.00   # paga/hora de dueño con 8 años de oficio
C_QUOTE           = 140.00   # costo de atender el lead (0.4 hr)

# Reja de precios permitidos
PASO_REJA = 150

# ═══════════════════════════════════════════════════════════════════
# BLOQUE 2 · UTILIDADES DE REJA Y GEMATRÍA
# ═══════════════════════════════════════════════════════════════════

def raiz_digital(n: int) -> int:
    """Reduce n sumando dígitos hasta un solo dígito."""
    n = abs(int(n))
    if n == 0:
        return 0
    return 1 + (n - 1) % 9

def cumple_reja(n: int) -> bool:
    """Múltiplo de 50 Y raíz digital en {3,6,9}."""
    return n % 50 == 0 and raiz_digital(n) in (3, 6, 9)

def sube_a_reja(valor: float) -> int:
    """Redondea hacia ARRIBA al siguiente múltiplo de 150."""
    return int(ceil(valor / PASO_REJA) * PASO_REJA)

def baja_a_reja(valor: float) -> int:
    """Redondea hacia ABAJO al múltiplo de 150 previo."""
    return int((valor // PASO_REJA) * PASO_REJA)

def reja(desde: int, hasta: int):
    """Todos los precios válidos en el rango."""
    ini = sube_a_reja(desde)
    return list(range(ini, hasta + 1, PASO_REJA))

# ═══════════════════════════════════════════════════════════════════
# BLOQUE 3 · MODELO DE TIEMPO Y COSTO
# ═══════════════════════════════════════════════════════════════════

class Tier:
    """Un nivel de sesión. El tiempo se computa, no se adivina."""

    def __init__(self, nombre, fotos, cambios, radio_km,
                 min_edicion=MIN_EDICION_FOTO, material=0.0,
                 p50=None, k=None):
        self.nombre      = nombre
        self.fotos       = fotos
        self.cambios     = cambios
        self.radio_km    = radio_km
        self.min_edicion = min_edicion
        self.material    = material     # impresiones, USB, etc.
        self.p50         = p50          # precio con 50% de cierre (ESTIMADO)
        self.k           = k            # ancho de la curva de demanda

    # ---------- TIEMPO ----------
    @property
    def hr_traslado(self):
        # 45 km/h promedio en carretera huasteca, ida y vuelta
        return round((self.radio_km * 2) / 45.0, 2)

    @property
    def hr_captura(self):
        return HR_CAPTURA_BASE + HR_CAPTURA_CAMBIO * self.cambios

    @property
    def hr_culling(self):
        return HR_CULL_BASE + HR_CULL_X_FOTO * self.fotos

    @property
    def hr_edicion(self):
        return self.fotos * self.min_edicion / 60.0

    @property
    def horas(self):
        return round(self.hr_traslado + self.hr_captura +
                     self.hr_culling + self.hr_edicion + HR_ADMIN, 2)

    @property
    def hr_arranque(self):
        """Costo fijo de existir: salir, montar, volver, administrar."""
        return round(self.hr_traslado + HR_ADMIN + HR_CAPTURA_BASE, 2)

    # ---------- COSTO ----------
    @property
    def gasolina(self):
        if self.radio_km <= 12:
            return 120.0
        return round(GASOLINA_EVENTO * (self.radio_km / 40.0), 0)

    @property
    def hormiga(self):
        return GASTO_HORMIGA if self.radio_km > 12 else 180.0

    @property
    def costos_duros(self):
        return round(self.gasolina + self.hormiga + self.material, 2)

    # ---------- PRECIO ----------
    def piso_reja(self, hora_objetivo=HORA_OBJETIVO):
        crudo = self.horas * hora_objetivo + self.costos_duros
        return sube_a_reja(crudo), crudo

    def utilidad(self, precio):
        return round(precio - self.costos_duros, 2)

    def por_hora(self, precio):
        return round(self.utilidad(precio) / self.horas, 2)

    def ratio_material(self, precio):
        return round(self.material / precio, 4) if precio else 0.0

    # ---------- PROBABILIDAD ----------
    def q_book(self, precio):
        """Curva logística de cierre. ESTIMADO — calibrar con ventas."""
        if self.p50 is None:
            return None
        return 1.0 / (1.0 + exp((precio - self.p50) / self.k))

    def pi_lead(self, precio):
        q = self.q_book(precio)
        if q is None:
            return None
        return round(q * self.utilidad(precio) - C_QUOTE, 2)

# ═══════════════════════════════════════════════════════════════════
# BLOQUE 4 · CONFIGURACIONES EN BASE 3 (TESLA 3-6-9)
# ═══════════════════════════════════════════════════════════════════

CONFIGS = {
    "A · 6-15-30": [
        Tier("EXPRESS",  fotos=6,  cambios=1, radio_km=10, p50=1150, k=230),
        Tier("ESENCIAL", fotos=15, cambios=1, radio_km=25, p50=2150, k=430),
        Tier("COMPLETA", fotos=30, cambios=2, radio_km=35, p50=3450, k=700),
    ],
    "B · 6-18-36": [
        Tier("EXPRESS",  fotos=6,  cambios=1, radio_km=10, p50=1150, k=230),
        Tier("ESENCIAL", fotos=18, cambios=1, radio_km=25, p50=2150, k=430),
        Tier("COMPLETA", fotos=36, cambios=2, radio_km=35, p50=3450, k=700),
    ],
    "C · 9-18-36": [
        Tier("EXPRESS",  fotos=9,  cambios=1, radio_km=10, p50=1150, k=230),
        Tier("ESENCIAL", fotos=18, cambios=1, radio_km=25, p50=2150, k=430),
        Tier("COMPLETA", fotos=36, cambios=2, radio_km=35, p50=3450, k=700),
    ],
    "D · 3-9-27": [
        Tier("EXPRESS",  fotos=3,  cambios=1, radio_km=10, p50=1150, k=230),
        Tier("ESENCIAL", fotos=9,  cambios=1, radio_km=25, p50=2150, k=430),
        Tier("COMPLETA", fotos=27, cambios=2, radio_km=35, p50=3450, k=700),
    ],
}

GALA = Tier("GALA", fotos=50, cambios=3, radio_km=40,
            min_edicion=MIN_EDICION_GALA, material=200.0,
            p50=5100, k=1000)

# ═══════════════════════════════════════════════════════════════════
# BLOQUE 5 · SALIDA
# ═══════════════════════════════════════════════════════════════════

def linea(c="─", n=104):
    print(c * n)

def bloque_reja():
    print("\n█ REJA DE PRECIOS VÁLIDOS · múltiplo de 50 + raíz digital 3/6/9")
    linea()
    validos = reja(600, 5400)
    print(f"  Total de precios permitidos entre $600 y $5,400: {len(validos)}")
    print(f"  Paso de la reja: ${PASO_REJA}  (todo múltiplo de 150)")
    print()
    fila = []
    for p in validos:
        fila.append(f"{p:>5}({raiz_digital(p)})")
    for i in range(0, len(fila), 8):
        print("   " + "  ".join(fila[i:i+8]))
    print()
    print("  Contraprueba de números REPROBADOS por la reja:")
    for mal in (950, 1900, 3200, 4900, 1420, 2880):
        rd = raiz_digital(mal)
        m50 = "sí" if mal % 50 == 0 else "no"
        print(f"    ${mal:>5}  ·  múltiplo de 50: {m50}  ·  raíz digital: {rd}  →  RECHAZADO")

def bloque_fisica(tiers):
    print("\n█ FÍSICA DEL TIEMPO · de dónde sale cada hora")
    linea()
    print(f"  {'TIER':<10} {'FOTOS':>6} {'TRASL':>7} {'CAPT':>6} {'CULL':>6} "
          f"{'EDIC':>6} {'ADMIN':>6} {'TOTAL':>7} {'ARRANQ':>7} {'COSTOS':>8}")
    linea("·")
    for t in tiers:
        print(f"  {t.nombre:<10} {t.fotos:>6} {t.hr_traslado:>7.2f} {t.hr_captura:>6.2f} "
              f"{t.hr_culling:>6.2f} {t.hr_edicion:>6.2f} {HR_ADMIN:>6.2f} "
              f"{t.horas:>7.2f} {t.hr_arranque:>7.2f} {t.costos_duros:>8.0f}")

def bloque_pisos(tiers):
    print("\n█ PISO EN REJA POR HORA OBJETIVO")
    linea()
    print(f"  {'TIER':<10} " + "".join(f"{f'${h}/hr':>13}" for h in (250, 300, 350, 400)))
    linea("·")
    for t in tiers:
        celdas = ""
        for h in (250, 300, 350, 400):
            p, crudo = t.piso_reja(h)
            celdas += f"{f'${p:,}':>13}"
        print(f"  {t.nombre:<10} " + celdas)
    print("\n  (crudo antes de subir a reja)")
    for t in tiers:
        vals = "  ".join(f"${t.piso_reja(h)[1]:,.0f}" for h in (250, 300, 350, 400))
        print(f"    {t.nombre:<10} {vals}")

def bloque_barrido(t):
    print(f"\n█ BARRIDO DE REJA · {t.nombre}  ({t.fotos} fotos · {t.horas} hr · costos ${t.costos_duros:,.0f})")
    linea()
    print(f"  {'PRECIO':>8} {'RAÍZ':>5} {'UTILIDAD':>10} {'$/HORA':>9} "
          f"{'q_book':>8} {'Π_lead':>10} {'MAT%':>7}  MARCA")
    linea("·")
    mejor_pi, mejor_p = -1e9, None
    filas = []
    lo  = baja_a_reja(t.costos_duros + 200)
    hi  = sube_a_reja(t.piso_reja(520)[1])
    for p in reja(max(lo, PASO_REJA), hi):
        u   = t.utilidad(p)
        ph  = t.por_hora(p)
        q   = t.q_book(p)
        pil = t.pi_lead(p)
        if pil is not None and pil > mejor_pi:
            mejor_pi, mejor_p = pil, p
        filas.append((p, u, ph, q, pil, t.ratio_material(p)))
    for (p, u, ph, q, pil, mat) in filas:
        marca = ""
        if p == mejor_p:
            marca += "◄ MÁXIMO Π_lead "
        if ph >= HORA_OBJETIVO and (p - PASO_REJA) and t.por_hora(p - PASO_REJA) < HORA_OBJETIVO:
            marca += f"◄ cruza ${HORA_OBJETIVO:.0f}/hr"
        qs  = f"{q*100:>7.1f}%" if q is not None else "     n/d"
        pls = f"${pil:>9,.0f}" if pil is not None else "      n/d"
        alerta = " ⚠MAT" if mat > TOPE_MATERIAL else ""
        print(f"  {f'${p:,}':>8} {raiz_digital(p):>5} {f'${u:,.0f}':>10} "
              f"{f'${ph:,.0f}':>9} {qs} {pls} {mat*100:>6.1f}%{alerta}  {marca}")
    return mejor_p

def bloque_veredicto(nombre, tiers, optimos):
    print(f"\n█ VEREDICTO · CONFIG {nombre}")
    linea()
    print(f"  {'TIER':<10} {'FOTOS':>6} {'PISO350':>10} {'ÓPTIMO':>10} "
          f"{'RAÍZ':>5} {'$/HORA':>9} {'UTILIDAD':>10} {'q_book':>8} {'Π_lead':>10}")
    linea("·")
    total_pi = 0
    for t, op in zip(tiers, optimos):
        piso = t.piso_reja(HORA_OBJETIVO)[0]
        q    = t.q_book(op)
        pil  = t.pi_lead(op)
        total_pi += pil or 0
        print(f"  {t.nombre:<10} {t.fotos:>6} {f'${piso:,}':>10} {f'${op:,}':>10} "
              f"{raiz_digital(op):>5} {f'${t.por_hora(op):,.0f}':>9} "
              f"{f'${t.utilidad(op):,.0f}':>10} {q*100:>7.1f}% {f'${pil:,.0f}':>10}")
    linea("·")
    print(f"  Π_lead sumado de la escalera: ${total_pi:,.0f}")
    ph = [t.por_hora(op) for t, op in zip(tiers, optimos)]
    asc = all(ph[i] < ph[i+1] for i in range(len(ph)-1))
    print(f"  $/hora ascendente por tier: {'SÍ ✓' if asc else 'NO ✗ (fuga de margen)'}  "
          f"→ {' → '.join(f'${x:,.0f}' for x in ph)}")
    pr = [op for op in optimos]
    razones = [round(pr[i+1]/pr[i], 2) for i in range(len(pr)-1)]
    print(f"  Razón entre tiers: {' · '.join(f'{r}x' for r in razones)}")
    return total_pi

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Motor de precios · sesiones fotográficas · SAN LUIS PRO")
    ap.add_argument("--gasolina", type=float, default=GASOLINA_EVENTO,
                    help="Gasolina base de evento en pesos (default: 250)")
    args = ap.parse_args()
    GASOLINA_EVENTO = args.gasolina

    print("╔" + "═" * 102 + "╗")
    print("║" + "  MOTOR DE PRECIOS · SESIONES FOTOGRÁFICAS · SAN LUIS PRO".ljust(102) + "║")
    print("║" + "  Reja: múltiplo de 50 + raíz digital 3/6/9  =  múltiplo de 150".ljust(102) + "║")
    print("║" + f"  Gasolina base de evento: ${GASOLINA_EVENTO:,.0f} · editable con --gasolina".ljust(102) + "║")
    print("╚" + "═" * 102 + "╝")

    bloque_reja()

    resultados = {}
    for nombre, tiers in CONFIGS.items():
        print("\n\n" + "═" * 104)
        print(f"  CONFIGURACIÓN {nombre}")
        print("═" * 104)
        bloque_fisica(tiers)
        bloque_pisos(tiers)
        optimos = []
        for t in tiers:
            op = bloque_barrido(t)
            optimos.append(op)
        total = bloque_veredicto(nombre, tiers, optimos)
        resultados[nombre] = (total, optimos, tiers)

    print("\n\n" + "═" * 104)
    print("  COMPARATIVO FINAL DE CONFIGURACIONES")
    print("═" * 104)
    print(f"  {'CONFIG':<14} {'PRECIOS EN REJA':<34} {'Π_lead TOTAL':>14}  {'$/HORA POR TIER':<30}")
    linea("·")
    for nombre, (total, optimos, tiers) in sorted(resultados.items(),
                                                  key=lambda x: -x[1][0]):
        precios = " · ".join(f"${p:,}" for p in optimos)
        phs     = " → ".join(f"${t.por_hora(p):,.0f}" for t, p in zip(tiers, optimos))
        print(f"  {nombre:<14} {precios:<34} {f'${total:,.0f}':>14}  {phs:<30}")

    # ---- GALA ----
    print("\n\n" + "═" * 104)
    print("  SERVICIO AISLADO · GALA / PRODUCCIÓN  (Ley 2 — fuera de la escalera)")
    print("═" * 104)
    bloque_fisica([GALA])
    bloque_pisos([GALA])
    op_gala = bloque_barrido(GALA)
    print(f"\n  Rango declarado en disco (Ley 2): $4,500 – $5,500")
    en_reja = [p for p in reja(4500, 5500)]
    print(f"  Precios de reja dentro de ese rango: {' · '.join(f'${p:,} (raíz {raiz_digital(p)})' for p in en_reja)}")
    print(f"  Óptimo por Π_lead: ${op_gala:,}  ·  ${GALA.por_hora(op_gala):,.0f}/hr  ·  "
          f"utilidad ${GALA.utilidad(op_gala):,.0f}")

    # ---- COMPLEMENTOS EN REJA ----
    print("\n\n" + "═" * 104)
    print("  COMPLEMENTOS · también en reja")
    print("═" * 104)
    print(f"  {'CONCEPTO':<34} {'PRECIO':>9} {'RAÍZ':>5} {'COSTO':>9} {'MARGEN':>9}")
    linea("·")
    comps = [
        ("Fotografía extra editada (c/u)",  30, COSTO_FOTO_IMPRESA),
        ("Look / cambio de ropa adicional", 450, 0.0),
        ("Hora extra de sesión en campo",   600, 0.0),
        ("Traslado fuera de radio (>40 km)",300, 250.0),
    ]
    for c, p, costo in comps:
        m = (p - costo) / p * 100 if p else 0
        ok = "" if (p % 50 == 0 and raiz_digital(p) in (3,6,9)) or p < 50 else "  ⚠ fuera de reja"
        print(f"  {c:<34} {f'${int(p):,}':>9} {raiz_digital(p):>5} {f'${costo:,.2f}':>9} {f'{m:.1f}%':>9}{ok}")

    print("\n" + "═" * 104)
    print("  ETIQUETAS: VERIFICADO = leído de disco · INFERIDO = flujo estándar · ESTIMADO = sin ancla")
    print("  q_book y C_QUOTE son ESTIMADO. Calibrar con ventas reales antes de tratarlos como hecho.")
    print("═" * 104)
