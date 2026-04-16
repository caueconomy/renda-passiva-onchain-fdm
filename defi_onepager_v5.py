"""
DeFi One-Pager v5 — Formadores de Mercado
Layout completamente fixo. Nenhum elemento dinâmico que possa se sobrepor.
Coordenadas calculadas de cima para baixo em mm, convertidas para pts do ReportLab no momento do uso.
"""
import json, math, os
from datetime import datetime
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fontes ───────────────────────────────────────────────────
# Se Sora-Regular.ttf estiver na mesma pasta, usa; caso contrário Helvetica.
_sora_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sora-Regular.ttf")
FONT_REG  = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
if os.path.exists(_sora_path):
    try:
        pdfmetrics.registerFont(TTFont("Sora",   _sora_path))
        pdfmetrics.registerFont(TTFont("SoraBd", _sora_path))
        FONT_REG  = "Sora"
        FONT_BOLD = "SoraBd"
    except Exception:
        pass

# ── Dimensões ────────────────────────────────────────────────
W, H = A4          # 595.28 × 841.89 pts
# Margens laterais fixas
ML = 12 * mm       # margem left
MR = 12 * mm       # margem right
CW = W - ML - MR   # content width (~171mm)

# ── Paleta FDM ───────────────────────────────────────────────
BG         = colors.HexColor("#0f0a1a")
SURF       = colors.HexColor("#1a1228")
SURF2      = colors.HexColor("#231733")
BORDER     = colors.HexColor("#2e1f4a")
PURPLE     = colors.HexColor("#822ee5")
PURPLE_DK  = colors.HexColor("#61358b")
YELLOW     = colors.HexColor("#ffb81c")
MINT       = colors.HexColor("#8ffff8")
BLACK_FDM  = colors.HexColor("#2c2c2c")
WHITE      = colors.white
TEXT_C     = colors.HexColor("#f0eaf8")   # texto principal — branco quente
# Cores de texto clarificadas para contraste sobre fundo escuro (#0f0a1a)
DIM        = colors.HexColor("#c4b5d8")   # era #a98fd4 — agora mais claro
MUTED      = colors.HexColor("#8b70b8")   # era #6b4f9e — agora mais claro
S_GREEN    = colors.HexColor("#4ade80")
S_YELLOW   = colors.HexColor("#facc15")
S_RED      = colors.HexColor("#f87171")
S_BLUE     = colors.HexColor("#60a5fa")
S_ORANGE   = colors.HexColor("#fb923c")

# ── Dados ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "defi_pools.json")) as f:
    POOLS = json.load(f)

# market_data.json: gerado pelo refresh_data.py com dados live
# Fallback para valores hardcoded se arquivo não existir
_MARKET_FALLBACK = {
    "tbill_1y": 3.70, "tbond_10y": 4.30, "tbill_3m": 3.71,
    "hi_yield_savings": 4.50, "sp500_hist_10y": 11.84,
    "selic_meta": 14.75, "cdi_annual": 14.65,
    "ipca_12m": 4.14, "usd_brl": 5.00,
    "selic_usd_hist": 6.50, "selic_real_brl": 10.19,
}
_market_path = os.path.join(BASE_DIR, "market_data.json")
if os.path.exists(_market_path):
    with open(_market_path) as f:
        MARKET = json.load(f)
else:
    MARKET = _MARKET_FALLBACK

# Data de atualização: do market_data.json ou hoje
UPDATE_DATE = datetime.now().strftime("%d/%m/%Y")
if "updated_at" in MARKET:
    try:
        UPDATE_DATE = datetime.fromisoformat(
            MARKET["updated_at"].replace("Z","")).strftime("%d/%m/%Y")
    except Exception:
        pass

TOTAL_POOLS_SCANNED  = 16740   # atualizado a cada refresh (aproximado)
TOTAL_POOLS_SELECTED = len(POOLS)

OUTPUT = os.path.join(BASE_DIR, "renda-passiva-onchain-onepager.pdf")

# Logos locais
_ASSETS = os.path.join(BASE_DIR, "..", "Material de Apoio")
LOGO_VERTICAL = os.path.join(_ASSETS, "VerticalSimbolo_branca-8.png")
LOGO_SYMBOL   = os.path.join(_ASSETS, "Simbolo_branca-8.png")

# ── Helpers ──────────────────────────────────────────────────
def y(mm_from_top):
    """Converte mm do topo para pts do ReportLab (origem no rodapé)."""
    return H - mm_from_top * mm

def rr(c, x_mm, top_mm, w_mm, h_mm, r_mm=3, fc=None, sc=None, sw=0.4):
    """Rounded rect. Recebe tudo em mm (exceto r em mm)."""
    x = x_mm * mm
    yb = y(top_mm + h_mm)   # y bottom = top_mm + h_mm from top
    w = w_mm * mm
    h = h_mm * mm
    r = r_mm * mm
    if fc: c.setFillColor(fc)
    if sc: c.setStrokeColor(sc); c.setLineWidth(sw)
    else:  c.setLineWidth(0)
    c.roundRect(x, yb, w, h, r, fill=1 if fc else 0, stroke=1 if sc else 0)

def txt(c, x_mm, top_mm, text, bold=False, size=8, col=None, align="left"):
    """Texto. x_mm e top_mm em mm do topo."""
    if col: c.setFillColor(col)
    c.setFont(FONT_BOLD if bold else FONT_REG, size)
    s = str(text)
    xp = x_mm * mm
    # baseline ≈ top_mm * mm de baixo + (size * 0.3) para alinhar visualmente
    yp = y(top_mm) + size * 0.1
    if align == "center": c.drawCentredString(xp, yp, s)
    elif align == "right": c.drawRightString(xp, yp, s)
    else: c.drawString(xp, yp, s)

def hline(c, x1_mm, top_mm, x2_mm, col=None, w=0.35):
    c.setStrokeColor(col or BORDER)
    c.setLineWidth(w)
    c.line(x1_mm * mm, y(top_mm), x2_mm * mm, y(top_mm))

def bar(c, x_mm, top_mm, w_mm, h_mm, fc, r_mm=1.5):
    """Barra simples."""
    rr(c, x_mm, top_mm, w_mm, h_mm, r_mm=r_mm, fc=fc)

# ══════════════════════════════════════════════════════════════
def build():
    c = rl_canvas.Canvas(OUTPUT, pagesize=A4)
    c.setTitle("Renda Passiva On-chain — Formadores de Mercado")

    # ── Background ──────────────────────────────────────────
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Glow roxo top-right
    for i in range(5, 0, -1):
        c.setFillColor(colors.HexColor(f"#{0x10+i*4:02x}{0x08+i*2:02x}{0x28+i*5:02x}"))
        c.circle(W - 10*mm, H - 5*mm, i * 18*mm, fill=1, stroke=0)

    # ── SEÇÃO 1: HEADER (topo=4mm, h=28mm) ─────────────────
    H_TOP = 4;  H_HT = 33   # aumentado para acomodar subtítulo 2 linhas + pills
    rr(c, 12, H_TOP, 186, H_HT, r_mm=4, fc=colors.HexColor("#120c24"), sc=BORDER, sw=0.4)
    rr(c, 12, H_TOP, 3,   H_HT, r_mm=2, fc=PURPLE)   # accent

    # Logo real — versão vertical (símbolo + "Formadores de Mercado")
    try:
        logo_h_mm = 16
        logo_w_mm = logo_h_mm * (1484/385)   # aspect ratio real: 1484×385
        if logo_w_mm > 52: logo_w_mm = 52; logo_h_mm = logo_w_mm * (385/1484)
        logo_top = H_TOP + (H_HT - logo_h_mm) / 2   # centralizado verticalmente
        c.drawImage(
            LOGO_VERTICAL,
            x=16*mm, y=y(logo_top + logo_h_mm),
            width=logo_w_mm*mm, height=logo_h_mm*mm,
            preserveAspectRatio=True, mask='auto'
        )
        title_x = 16 + logo_w_mm + 5
    except Exception:
        txt(c, 17, H_TOP + 7, "Formadores de Mercado", bold=True, size=11, col=WHITE)
        title_x = 17

    # Título
    txt(c, title_x, H_TOP + 9, "Renda Passiva On-chain", bold=True, size=13, col=WHITE)

    # Subtítulo — 1 linha curta (cabe sem conflito com info)
    txt(c, title_x, H_TOP + 16,
        "Rendimento real em dolar, acima do mercado tradicional",
        size=7.5, col=DIM)

    # Pills (linha 21..26mm) — apenas 3 pills curtas, ficam em ~139mm
    pills = [("USDT · USDC", PURPLE), ("ETH · Base · ARB", PURPLE_DK), (UPDATE_DATE, BORDER)]
    px = title_x
    for plbl, pcol in pills:
        pw = len(plbl) * 1.5 + 6
        rr(c, px, H_TOP + 21, pw, 5, r_mm=2.5, fc=pcol)
        txt(c, px + pw/2, H_TOP + 22.5, plbl, bold=True, size=6, col=WHITE, align="center")
        px += pw + 2

    # Info removida do header — será colocada na linha do subtítulo do gráfico

    # ── SEÇÃO 2: GRÁFICO (começa logo após header: H_TOP + H_HT + 4mm) ──
    G_TOP = H_TOP + H_HT + 4   # = 4 + 33 + 4 = 41mm

    txt(c, 12, G_TOP + 4, "Rentabilidade Anual — DeFi vs Mercado Tradicional",
        bold=True, size=8.5, col=WHITE)
    # Subtítulo à esquerda + info à direita na mesma linha — sem sobreposição pois
    # o subtítulo tem ~85mm e a info começa em ~148mm (gap de ~63mm)
    txt(c, 12,  G_TOP + 8, f"APY live DeFiLlama · FedReserve H.15 · BCB · Atualizado {UPDATE_DATE}",
        size=6, col=DIM)
    txt(c, 198, G_TOP + 8, "16.740 pools rastreados · 20 selecionados",
        size=6, col=DIM, align="right")
    hline(c, 12, G_TOP + 10.5, 198)

    # Configuração das barras
    LABEL_W  = 47.0   # mm para o label
    BAR_X    = 12 + LABEL_W + 1   # onde começa a barra (mm)
    BADGE_W  = 9.0
    BAR_W    = 198 - BAR_X - BADGE_W - 2  # largura máx da barra
    # MAX_APY calculado dinamicamente em BAR_ROWS acima
    ROW_H    = 5.5    # altura barra mm
    ROW_GAP  = 1.6    # gap entre barras mm
    ROW_STEP = ROW_H + ROW_GAP

    # Dados das barras: (label, apy, apy30d, hex_color, categoria)
    # Uso apenas os mais representativos (6 DeFi + sep + 3 US + 2 BR)
    # ── Barras 100% dinâmicas — vindas do JSON + MARKET ───────
    # Selecionar 6 pools DeFi representativos: top APY excluindo risco alto,
    # com variedade de projetos
    _HIGH_RISK = {"maple","goldfinch","yo-protocol"}
    _chart_pools = [p for p in POOLS if p["project"] not in _HIGH_RISK]
    # Dedup por projeto — pegar melhor APY por projeto
    _seen_proj = {}
    for p in _chart_pools:
        pj = p["project"]
        if pj not in _seen_proj or p["apy"] > _seen_proj[pj]["apy"]:
            _seen_proj[pj] = p
    # Ordenar por APY desc, pegar top 6
    _top6 = sorted(_seen_proj.values(), key=lambda x: x["apy"], reverse=True)[:6]

    def _pname(p):
        return p["project"].replace("-v3","").replace("-v2","").replace("-dex","") \
                           .replace("-"," ").title()[:20] + f" ({p['symbol'][:8]})"

    BAR_ROWS = [(
        _pname(p), p["apy"], p["apy30d"],
        "#6d28d9" if p["apy"] >= 8 else "#822ee5",
        "DeFi"
    ) for p in _top6]

    # Separador + TradFi + Brasil — todos vindos do MARKET (live ou fallback)
    BAR_ROWS += [
        None,
        ("US T-Bill 1 ano",
         MARKET["tbill_1y"], MARKET["tbill_1y"], "#374151", "USD"),
        ("US T-Bond 10 anos",
         MARKET["tbond_10y"], MARKET["tbond_10y"], "#374151", "USD"),
        ("Hi-Yield Savings EUA",
         MARKET["hi_yield_savings"], MARKET["hi_yield_savings"], "#374151", "USD"),
        ("Selic adj. USD (hist.)",
         MARKET["selic_usd_hist"], MARKET["selic_usd_hist"], "#6b7280", "BRL"),
    ]
    MAX_APY = max(r[1] for r in BAR_ROWS if r) * 1.15  # 15% de padding visual

    cur_top = G_TOP + 13   # começa aqui

    for row in BAR_ROWS:
        if row is None:
            # Separador
            hline(c, 12, cur_top + 1.5, 198, col=BORDER, w=0.3)
            txt(c, 105, cur_top + 0.5, "── Mercado Tradicional abaixo ──",
                size=5.5, col=MUTED, align="center")
            cur_top += 4.5
            continue

        label, apy, apy30, hx, cat = row
        fc = colors.HexColor(hx)

        # Sem trilho de fundo — evita qualquer fantasma visual

        # Barra principal
        w_bar = max(1.0, (apy / MAX_APY) * BAR_W)
        rr(c, BAR_X, cur_top, w_bar, ROW_H, r_mm=1.5, fc=fc)

        # Label — todos visíveis, DeFi em branco quente, TradFi em cinza claro
        lcol = TEXT_C if cat == "DeFi" else DIM
        txt(c, 12, cur_top + ROW_H * 0.5 - 0.5, label, size=7, col=lcol)

        # Valor APY (à direita da barra)
        val_x = BAR_X + w_bar + 1.5
        txt(c, val_x, cur_top + ROW_H * 0.5 - 0.5,
            f"{apy:.2f}%", bold=(cat=="DeFi"), size=7.5, col=fc)

        # Badge categoria (extrema direita)
        bx = 198 - BADGE_W
        bdg_col   = {"DeFi": colors.HexColor("#170930"), "USD": colors.HexColor("#0d1a0d"),
                     "BRL": colors.HexColor("#0a1a0a")}.get(cat, SURF)
        bdg_tcol  = {"DeFi": MINT, "USD": DIM, "BRL": S_GREEN}.get(cat, DIM)
        rr(c, bx, cur_top + 0.5, BADGE_W - 0.5, ROW_H - 1, r_mm=2, fc=bdg_col)
        txt(c, bx + (BADGE_W-0.5)/2, cur_top + ROW_H*0.5 - 0.5,
            cat, bold=True, size=5.5, col=bdg_tcol, align="center")

        cur_top += ROW_STEP

    # Legenda — fundo escuro por trás para garantir contraste
    cur_top += 2
    # Box de fundo para a legenda inteira
    rr(c, 12, cur_top - 1, 186, 6, r_mm=2, fc=colors.HexColor("#0d0818"))

    LEG = [("DeFi — APY atual", "#822ee5"),
           ("TradFi USD",       "#4b5563"),
           ("Selic adj. USD",   "#6b7280")]
    lx = 13.0
    for ll, lc in LEG:
        rr(c, lx, cur_top + 0.5, 8, 3, r_mm=1.5, fc=colors.HexColor(lc))
        txt(c, lx + 10, cur_top + 1.5, ll, size=7, col=TEXT_C)
        lx += 40

    chart_end = cur_top + 5   # onde termina o gráfico

    # ── SEÇÃO 3: KPI CARDS — gap aumentado para distribuir espaço vertical
    KPI_TOP = chart_end + 5   # +2mm de respiro
    KPI_H   = 22.0            # era 19mm — +3mm para cards mais altos
    KPI_GAP = 3.5
    KPI_W   = (186 - 3 * KPI_GAP) / 4

    # Calcular KPIs reais
    safe_pools = [p for p in POOLS if p["project"] not in ("maple","goldfinch","yo-protocol")]
    best_safe  = max(safe_pools, key=lambda x: x["apy"]) if safe_pools else POOLS[0]
    best_all   = max(POOLS, key=lambda x: x["apy"])
    sim_safe   = round(10000 * (math.pow(1 + best_safe["apy"]/100/12, 12) - 1))
    trad_1y    = round(10000 * 0.037)

    sim_tbill  = round(10000 * MARKET["tbill_1y"] / 100)
    sim_selic  = round(10000 * MARKET["selic_usd_hist"] / 100)

    KPIS = [
        ("Melhor APY DeFi",      f"{best_all['apy']:.2f}%",
         best_all['project'].replace('-',' ').title()[:20],
         f"vs 3.70% T-Bill EUA",     PURPLE),
        ("Rendimento conservador", f"{best_safe['apy']:.2f}%",
         best_safe['project'].replace('-',' ').title()[:20],
         "Risco baixo/medio",         YELLOW),
        ("Simulacao $10k / 12m",  f"+${sim_safe:,}",
         "Rendimento estimado DeFi",
         f"vs +${sim_tbill} T-Bill",   S_GREEN),
        # KPI 4: desvantagem da Selic em USD — deixa claro que DeFi é superior
        ("Selic em dolar (hist.)",  f"+${sim_selic:,}",
         "Selic adj. USD / $10k / 12m",
         f"Selic {MARKET['selic_meta']:.2f}% BRL → USD ~{MARKET['selic_usd_hist']:.1f}%",
         S_RED),
    ]

    for i, (lbl, val, sub, note, col) in enumerate(KPIS):
        kx = 12 + i * (KPI_W + KPI_GAP)
        rr(c, kx, KPI_TOP, KPI_W, KPI_H, r_mm=3.5, fc=SURF, sc=BORDER, sw=0.4)
        rr(c, kx, KPI_TOP, 2.5, KPI_H, r_mm=2, fc=col)
        txt(c, kx+4.5, KPI_TOP + 4,    lbl.upper(), size=5.5, col=DIM)
        txt(c, kx+4.5, KPI_TOP + 10.5, val, bold=True, size=12, col=col)
        txt(c, kx+4.5, KPI_TOP + 16,   sub, size=6.5, col=TEXT_C)
        txt(c, kx+4.5, KPI_TOP + 20,   note, size=5.5, col=DIM)

    # ── SEÇÃO 4: TABELA — gap aumentado
    TBL_TOP = KPI_TOP + KPI_H + 6   # era +4, agora +6

    txt(c, 12, TBL_TOP + 4.5,
        f"Top Protocolos — Live DeFiLlama  (20 selecionados · 16.740 rastreados)",
        bold=True, size=8, col=WHITE)
    hline(c, 12, TBL_TOP + 6.5, 198)

    # Colunas: [label, largura_mm]
    # Colunas redistribuídas para 186mm total (CW = 210 - 12*2 = 186mm)
    COLS = [
        ("Protocolo (Ativo)",   55),   # +5
        ("Rede",                16),
        ("APY",                 18),   # +1
        ("APY 30d",             18),   # +1
        ("TVL",                 21),   # +1
        ("Risco",               18),   # +1
        ("URL",                 40),   # +6
    ]
    assert sum(c2 for _, c2 in COLS) == 186, f"cols sum={sum(c2 for _,c2 in COLS)}"

    ROW_TH = 6.5    # altura header tabela (era 6.0)
    ROW_TR = 6.5    # altura linha dados (era 6.2) — mais respiro entre linhas

    # Header
    H_Y = TBL_TOP + 7.5
    rr(c, 12, H_Y, 186, ROW_TH, r_mm=1.5, fc=SURF2)
    cx = 12.0
    for hdr, cw in COLS:
        txt(c, cx+1.5, H_Y + 1.5, hdr, bold=True, size=6, col=TEXT_C)
        cx += cw

    # Dados — max 10 linhas para não sair da área
    RISK_MAP = {
        # Alto — crédito privado, histórico curto, ou risco de contraparte elevado
        "maple":          "Alto",
        "goldfinch":      "Alto",
        "yo-protocol":    "Alto",
        # Médio — protocolos estabelecidos mas com componentes variáveis (AMM, perps, incentivos)
        "avantis":        "Medio",
        "fluid-lending":  "Medio",
        "curve-dex":      "Medio",
        "convex-finance": "Medio",
        "euler-v2":       "Medio",
        "yearn-finance":  "Medio",
        "merkl":          "Medio",
        # sparklend removido daqui — está corretamente em Baixo abaixo
        "dolomite":       "Medio",
        "gmx-v2-perps":   "Medio",
        "aerodrome-v1":   "Medio",
        "aerodrome-slipstream": "Medio",
        "velodrome-v2":   "Medio",
        "uniswap-v3":     "Medio",
        "uniswap-v4":     "Medio",
        # Baixo — protocolos com TVL bilionário, múltiplas auditorias, anos de track record
        "aave-v3":        "Baixo",
        "compound-v3":    "Baixo",
        "spark-savings":  "Baixo",
        "sparklend":      "Baixo",
        "sky-lending":    "Baixo",
    }
    RISK_COL = {"Baixo": S_GREEN, "Medio": S_YELLOW, "Alto": S_RED}
    CHAIN_SHORT = {"Ethereum":"ETH","Base":"BASE","Arbitrum":"ARB","Optimism":"OP"}

    # Tabela: mesmos critérios do dashboard
    # - excluir risco Alto (Maple, Goldfinch, Yo Protocol) — não são recomendações
    # - ordenar por APY desc (melhor oportunidade primeiro)
    # - max 10 linhas
    HIGH_RISK = {"maple", "goldfinch", "yo-protocol"}
    # Excluir também pools com WBTC/BTC no par — não são stablecoin pura
    EXCLUDE_SYMBOLS = {"WBTC.B-USDC", "WBTC-USDC", "WBTC-USDT"}
    pools_filtered = [
        p for p in POOLS
        if p["project"] not in HIGH_RISK
        and p["symbol"] not in EXCLUDE_SYMBOLS
    ]
    pools_sorted = sorted(pools_filtered, key=lambda x: x["apy"], reverse=True)

    shown = 0
    dy = H_Y + ROW_TH
    for pool in pools_sorted:
        if shown >= 10: break
        if dy + ROW_TR > TBL_TOP + 7.5 + ROW_TH + 10 * ROW_TR + 2:
            break  # safety

        if shown % 2 == 1:
            c.setFillColor(colors.HexColor("#110a20"))
            c.rect(12*mm, y(dy + ROW_TR), 186*mm, ROW_TR*mm, fill=1, stroke=0)

        risk  = RISK_MAP.get(pool["project"], "Medio")
        rcol  = RISK_COL[risk]
        chain = CHAIN_SHORT.get(pool["chain"], pool["chain"][:4])
        pname = pool["project"].replace("-v3","").replace("-v2","").replace("-"," ").title()[:22]
        sym   = pool["symbol"][:10]
        tvl   = f"${pool['tvlM']:.0f}M" if pool["tvlM"] < 1000 else f"${pool['tvlM']/1000:.1f}B"
        url   = pool.get("url","").replace("https://","").split("/")[0][:24]

        row_vals = [
            (f"{pname} ({sym})", True,  TEXT_C, 7),
            (chain,              False, TEXT_C, 7),
            (f"{pool['apy']:.2f}%", True, PURPLE, 7.5),
            (f"{pool['apy30d']:.2f}%", False, TEXT_C, 7),
            (tvl,                True,  TEXT_C, 7),
            (risk,               False, rcol,   7),
            (url,                False, colors.HexColor("#7c3aed"), 6.5),
        ]

        cx = 12.0
        row_mid = dy + ROW_TR * 0.5 - 0.5
        for (val, bld, col, sz), (_, cw) in zip(row_vals, COLS):
            txt(c, cx + 1.5, row_mid, val, bold=bld, size=sz, col=col)
            cx += cw

        dy  += ROW_TR
        shown += 1

    # ── SEÇÃO 5: BRASIL — gap e altura maiores para preencher a página
    BR_TOP = dy + 5
    BR_H   = 27.0      # +3mm extra para hierarquia visual clara título→dados

    # Narrativa: mostrar que Selic não é solução — DeFi supera mesmo o "melhor do Brasil"
    rr(c, 12, BR_TOP, 186, BR_H, r_mm=3,
       fc=colors.HexColor("#0f0820"), sc=BORDER, sw=0.4)

    # Título na primeira linha com mais respiro
    txt(c, 105, BR_TOP + 5,
        "Por que a Selic nao protege em dolar — e o DeFi sim",
        bold=True, size=7.5, col=YELLOW, align="center")

    # Linha separadora fina abaixo do título
    hline(c, 14, BR_TOP + 8.5, 196, col=colors.HexColor("#1a1030"), w=0.3)

    # 3 colunas — dados abaixo da linha separadora
    _defi_range_lo = min(p["apy"] for p in POOLS if p["project"] not in _HIGH_RISK)
    _defi_range_hi = max(p["apy"] for p in POOLS if p["project"] not in _HIGH_RISK)
    BR_COLS = [
        ("Inflacao (IPCA)",
         f"-{MARKET['ipca_12m']:.2f}%", "Corroi poder de compra BRL", S_RED),
        ("Selic adj. USD",
         f"~{MARKET['selic_usd_hist']:.1f}%", "Selic real apos deprec. cambial", DIM),
        ("DeFi (USDC/USDT)",
         f"{_defi_range_lo:.1f}-{_defi_range_hi:.0f}%", "Em dolar · saque livre · 24h", PURPLE),
    ]
    bcw = 186 / 3
    for bi, (blbl, bval, bnote, bcol) in enumerate(BR_COLS):
        bx = 12 + bi * bcw + 3
        txt(c, bx, BR_TOP + 11,  blbl,  size=6.5, col=MUTED)
        txt(c, bx, BR_TOP + 16.5, bval, bold=True, size=12, col=bcol)
        txt(c, bx, BR_TOP + 21,  bnote, size=6,   col=MUTED)

    # ── FOOTER ─────────────────────────────────────────────
    FOOT_TOP = BR_TOP + BR_H + 3

    # Se o footer ficou perto do limite, forçar mínimo
    if FOOT_TOP > 285:
        FOOT_TOP = 285  # nunca abaixo de 12mm do rodapé

    hline(c, 12, FOOT_TOP + 0.5, 198)

    # Símbolo logo pequeno
    try:
        c.drawImage(
            LOGO_SYMBOL,
            x=12*mm, y=y(FOOT_TOP + 7),
            width=6*mm, height=6*mm,
            preserveAspectRatio=True, mask='auto'
        )
    except Exception:
        pass

    # Footer — duas linhas para não sobrepor
    # Linha 1: Logo + wordmark + data
    txt(c, 20, FOOT_TOP + 4,  "Formadores de Mercado", bold=True, size=6.5, col=DIM)
    txt(c, 198, FOOT_TOP + 4, f"Atualizado: {UPDATE_DATE}  ·  Nao constitui recomendacao de investimento",
        size=5.5, col=MUTED, align="right")
    # Linha 2: fontes
    txt(c, 198, FOOT_TOP + 8,
        "defillama.com/yields  ·  federalreserve.gov  ·  bcb.gov.br",
        size=5.5, col=MUTED, align="right")

    c.save()

    # Diagnóstico
    print(f"PDF gerado: {OUTPUT}")
    print(f"  chart_end={chart_end:.1f}mm  KPI_TOP={KPI_TOP:.1f}mm  TBL_TOP={TBL_TOP:.1f}mm")
    print(f"  BR_TOP={BR_TOP:.1f}mm  FOOT_TOP={FOOT_TOP:.1f}mm")
    print(f"  Linhas tabela: {shown}")
    print(f"  Altura total usada: {FOOT_TOP + 7:.1f}mm / 297mm")

build()
