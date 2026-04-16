"""
refresh_data.py — Renda Passiva On-chain · Formadores de Mercado
================================================================
Atualiza TODOS os dados do framework em um único comando:
  python refresh_data.py

Fontes:
  - DeFiLlama Yields API  → APY, TVL, pools USDC/USDT
  - Federal Reserve H.15  → T-Bill, T-Bond
  - BCB (Banco Central)   → Selic, CDI, IPCA, USD/BRL
  - Cálculo interno       → Selic adj. USD, Selic real BRL

Outputs:
  - defi_pools.json        → 20 melhores pools (lido pelo PDF e HTML)
  - market_data.json       → benchmarks TradFi + BR (lido pelo HTML)
  - Roda defi_onepager_v5.py automaticamente ao final
"""

import urllib.request
import json
import sys
import os
import subprocess
from datetime import datetime, timezone

# Windows: forçar UTF-8 no stdout para suportar emojis nos prints
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# ── PATHS ──────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
POOLS_JSON  = os.path.join(BASE_DIR, "defi_pools.json")
MARKET_JSON = os.path.join(BASE_DIR, "market_data.json")
PDF_SCRIPT  = os.path.join(BASE_DIR, "defi_onepager_v5.py")
OUTPUT_DIR  = BASE_DIR   # JSONs ficam na própria pasta do projeto

# ── FILTROS ────────────────────────────────────────────────────
TARGET_CHAINS    = {"Ethereum", "Base", "Arbitrum", "Optimism"}
STABLE_SYMBOLS   = {"USDT","USDC","USDC.E","USDBC"}
EXCLUDE_PROJECTS = {"maple", "goldfinch", "yo-protocol"}          # risco alto
EXCLUDE_SYMBOLS  = {"WBTC.B-USDC","WBTC-USDC","WBTC-USDT"}       # pares com BTC
MIN_TVL_M        = 10.0    # TVL mínimo em USD milhões
MIN_APY          = 1.5     # APY mínimo % (1.5 evita pools de ruído no limiar do filtro)

# URLs diretas por protocolo (fallback quando DeFiLlama não fornece)
PROTO_URLS = {
    "aave-v3":          "https://app.aave.com/markets/",
    "fluid-lending":    "https://fluid.instadapp.io/lending/",
    "euler-v2":         "https://app.euler.finance/",
    "compound-v3":      "https://app.compound.finance/",
    "maple":            "https://app.maple.finance/earn",
    "spark-savings":    "https://spark.fi/savings",
    "sparklend":        "https://app.spark.fi/markets/",
    "sky-lending":      "https://app.sky.money/",
    "curve-dex":        "https://curve.fi/#/ethereum/pools",
    "aerodrome-v1":     "https://aerodrome.finance/earn",
    "avantis":          "https://www.avantisfi.com/",
    "goldfinch":        "https://app.goldfinch.finance/earn",
    "convex-finance":   "https://www.convexfinance.com/stake",
    "yearn-finance":    "https://yearn.fi/",
    "uniswap-v3":       "https://app.uniswap.org/",
    "uniswap-v4":       "https://app.uniswap.org/",
    "dolomite":         "https://dolomite.io/",
    "gmx-v2-perps":     "https://app.gmx.io/#/earn",
    "merkl":            "https://app.merkl.xyz/",
    "yo-protocol":      "https://yo.xyz/",
    "zerobase-cedefi":  "https://app.zerobase.pro/en",
    "lazy-summer-protocol": "https://summer.fi/",
    "termmax":          "https://ts.finance/termmax/",
}


def fetch(url, timeout=20):
    """HTTP GET simples, retorna dict ou None."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  ⚠️  fetch({url[:60]}…): {e}", file=sys.stderr)
        return None


# ══════════════════════════════════════════════════════════════
# 1. DEFI POOLS — DeFiLlama
# ══════════════════════════════════════════════════════════════
def fetch_defi_pools():
    print("📡 DeFiLlama Yields API…")
    data = fetch("https://yields.llama.fi/pools")
    if not data:
        return None

    pools = data.get("data", [])
    print(f"   {len(pools):,} pools recebidos")

    results = []
    for p in pools:
        chain  = p.get("chain", "")
        sym    = p.get("symbol", "")
        apy    = p.get("apy") or 0
        tvl    = p.get("tvlUsd") or 0
        proj   = p.get("project", "")
        apy30  = p.get("apyMean30d") or apy

        parts  = sym.upper().replace("-","_").replace("/","_").split("_")
        has_stable  = any(s in STABLE_SYMBOLS for s in parts)
        has_exclude = any(s in {"WETH","ETH","WBTC","BTC","SOL","WSOL",
                                "ARB","OP","MATIC","AERO","CBBTC","TBTC",
                                "RAVE","XAUT","FRAX","CRVUSD","GHO","MSUSD",
                                "USDE","AAVEGHO"} for s in parts)

        if (chain in TARGET_CHAINS
                and has_stable
                and not has_exclude
                and sym not in EXCLUDE_SYMBOLS
                and tvl / 1e6 >= MIN_TVL_M
                and apy >= MIN_APY
                and apy30 >= MIN_APY):   # APY30d também acima do mínimo — filtra ruído
            url = p.get("url") or PROTO_URLS.get(proj, f"https://defillama.com/protocol/{proj}")
            # Substituir URLs genéricas do DeFiLlama
            if "defillama.com/protocol" in url and proj in PROTO_URLS:
                url = PROTO_URLS[proj]
            results.append({
                "project":  proj,
                "symbol":   sym,
                "chain":    chain,
                "apy":      round(apy, 2),
                "apy30d":   round(apy30, 2),
                "tvlM":     round(tvl / 1e6, 1),
                "url":      url,
            })

    # Dedup: manter melhor APY por projeto+symbol+chain
    seen = {}
    for r in results:
        k = f"{r['project']}|{r['symbol']}|{r['chain']}"
        if k not in seen or r["apy"] > seen[k]["apy"]:
            seen[k] = r

    # Ordenar por TVL desc, pegar top 30
    final = sorted(seen.values(), key=lambda x: x["tvlM"], reverse=True)[:30]
    print(f"   ✅ {len(final)} pools selecionados (TVL>{MIN_TVL_M}M, APY>{MIN_APY}%)")
    return final


# ══════════════════════════════════════════════════════════════
# 2. MERCADO TRADICIONAL
# ══════════════════════════════════════════════════════════════

def _fred_csv(series_id: str) -> float | None:
    """Busca última observação de uma série FRED via CSV público (sem API key)."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            lines = r.read().decode().strip().split("\n")
            for line in reversed(lines):
                parts = line.split(",")
                if len(parts) == 2 and parts[1].strip() not in (".", ""):
                    return round(float(parts[1].strip()), 2)
    except Exception as e:
        print(f"   ⚠️  FRED {series_id}: {e}", file=sys.stderr)
    return None


def fetch_federal_reserve():
    """
    Federal Reserve / FRED — taxas selecionadas via CSV público (sem autenticação).

    Séries:
      DGS1    → T-Bill 1 ano
      DGS10   → T-Bond 10 anos
      DGS3MO  → T-Bill 3 meses
      SOFR    → Secured Overnight Financing Rate (proxy para Hi-Yield Savings)

    Hi-Yield Savings: bancos online (Ally, Marcus, SoFi) precificam ~SOFR + 40 bps.
    Não existe endpoint público com a taxa exata — SOFR + 0.40% é a melhor aproximação
    automatizável. Valor atual típico: 4.0–4.6%.
    """
    print("📡 Federal Reserve / FRED…")
    SERIES = {
        "tbill_1y":  "DGS1",
        "tbond_10y": "DGS10",
        "tbill_3m":  "DGS3MO",
        "sofr":      "SOFR",
    }
    result = {}
    for key, series_id in SERIES.items():
        val = _fred_csv(series_id)
        if val is not None:
            result[key] = val

    if result:
        print(f"   ✅ Fed: {result}")
    else:
        print("   ⚠️  Fed inacessível — usando valores do cache")
    return result


def fetch_bcb():
    """
    Banco Central do Brasil — Selic meta, IPCA e USD/BRL.
    APIs públicas do BCB (sem autenticação).
    """
    print("📡 Banco Central do Brasil…")
    result = {}

    # Selic meta (série 432)
    selic_data = fetch("https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json")
    if selic_data and len(selic_data) > 0:
        result["selic_meta"] = round(float(selic_data[0]["valor"]), 2)

    # CDI diário acumulado anual — série 12 (taxa DI over)
    cdi_data = fetch("https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados/ultimos/1?formato=json")
    if cdi_data and len(cdi_data) > 0:
        # CDI vem como taxa diária, converter para anual
        cdi_daily = float(cdi_data[0]["valor"]) / 100
        cdi_annual = round((pow(1 + cdi_daily, 252) - 1) * 100, 2)
        result["cdi_annual"] = cdi_annual

    # IPCA acumulado 12 meses — série 13522
    ipca_data = fetch("https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1?formato=json")
    if ipca_data and len(ipca_data) > 0:
        result["ipca_12m"] = round(float(ipca_data[0]["valor"]), 2)

    # USD/BRL câmbio — cotação de venda (série 1)
    fx_data = fetch("https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/1?formato=json")
    if fx_data and len(fx_data) > 0:
        result["usd_brl"] = round(float(fx_data[0]["valor"]), 4)

    if result:
        print(f"   ✅ BCB: {result}")
    else:
        print("   ⚠️  BCB inacessível — usando valores do cache")
    return result


# ══════════════════════════════════════════════════════════════
# 3. CONSOLIDAR E SALVAR
# ══════════════════════════════════════════════════════════════

# Valores de fallback (usados se APIs estiverem fora)
FALLBACK_MARKET = {
    "tbill_1y":        3.70,
    "tbond_10y":       4.30,
    "tbill_3m":        3.71,
    "hi_yield_savings":4.50,   # derivado de SOFR + 0.40% — atualizado automaticamente
    "sofr":            4.10,   # fallback caso FRED esteja inacessível
    "sp500_hist_10y":  11.84,
    "selic_meta":      14.75,
    "cdi_annual":      14.65,
    "ipca_12m":        4.14,
    "usd_brl":         5.00,
    "selic_usd_hist":  6.50,   # calculado: Selic - deprec. BRL histórica (~8%)
    "selic_real_brl":  None,   # calculado abaixo
}


def build_market_data(fed: dict, bcb: dict) -> dict:
    """Mescla dados live com fallback e calcula derivados."""
    m = dict(FALLBACK_MARKET)

    # Aplicar dados live do Fed
    for k in ("tbill_1y", "tbond_10y", "tbill_3m", "sofr"):
        if k in fed:
            m[k] = fed[k]

    # Hi-Yield Savings: SOFR + 40 bps (bancos online como Ally, Marcus, SoFi)
    # Sem API pública com taxa exata — SOFR + 0.40% é a melhor aproximação automática
    m["hi_yield_savings"] = round(m["sofr"] + 0.40, 2)

    # Aplicar dados live do BCB
    for k in ("selic_meta", "cdi_annual", "ipca_12m", "usd_brl"):
        if k in bcb:
            m[k] = bcb[k]

    # Calcular derivados
    selic = m["selic_meta"]
    ipca  = m["ipca_12m"]
    m["selic_real_brl"]  = round((((1 + selic/100) / (1 + ipca/100)) - 1) * 100, 2)
    # Selic adj. USD: Selic BRL − depreciação histórica BRL/USD (~8%/a média)
    m["selic_usd_hist"]  = round(selic - 8.0, 2)

    m["updated_at"] = datetime.now(timezone.utc).isoformat()
    return m


def update_html_dashboard(pools: list, market: dict):
    """
    Injeta dados frescos diretamente no HTML do dashboard.
    Substitui:
      - LIVE_POOLS  → array com os pools atuais do defi_pools.json
      - MARKET_DATA → objeto com benchmarks atuais do market_data.json
    """
    import re

    html_path = os.path.join(BASE_DIR, "defi-yield-dashboard.html")
    if not os.path.exists(html_path):
        print("   ⚠️  defi-yield-dashboard.html não encontrado — pulando")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    # ── 1. LIVE_POOLS ────────────────────────────────────────
    lines = []
    for p in pools:
        proj = p["project"].replace('"', '\\"')
        sym  = p["symbol"].replace('"', '\\"')
        chn  = p["chain"].replace('"', '\\"')
        url  = p["url"].replace('"', '\\"')
        lines.append(
            f'  {{project:"{proj}",symbol:"{sym}",chain:"{chn}",'
            f'apy:{p["apy"]},apy30d:{p["apy30d"]},tvlM:{p["tvlM"]},url:"{url}"}}'
        )
    pools_js = "const LIVE_POOLS=[\n" + ",\n".join(lines) + "\n];"
    html, n1 = re.subn(r"const LIVE_POOLS=\[[\s\S]*?\];", pools_js, html)

    # ── 2. MARKET_DATA fallback ──────────────────────────────
    market_body = (
        f'  tbill_1y:{market["tbill_1y"]}, tbond_10y:{market["tbond_10y"]}, tbill_3m:{market["tbill_3m"]},\n'
        f'  hi_yield_savings:{market["hi_yield_savings"]}, sofr:{market.get("sofr", 4.10)}, sp500_hist_10y:{market["sp500_hist_10y"]},\n'
        f'  selic_meta:{market["selic_meta"]}, cdi_annual:{market["cdi_annual"]},\n'
        f'  ipca_12m:{market["ipca_12m"]}, usd_brl:{market["usd_brl"]},\n'
        f'  selic_usd_hist:{market["selic_usd_hist"]}, selic_real_brl:{market["selic_real_brl"]},\n'
        f'  updated_at:"{market["updated_at"]}"'
    )
    html, n2 = re.subn(
        r"(const MARKET_DATA = window\.__MARKET_DATA__ \|\| \{)[\s\S]*?(\};)",
        f"\\1\n{market_body}\n\\2",
        html,
    )

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    p_status = f"✅ ({len(pools)} pools)" if n1 else "⚠️  padrão não encontrado"
    m_status = "✅" if n2 else "⚠️  padrão não encontrado"
    print(f"   💾 HTML — LIVE_POOLS: {p_status}  |  MARKET_DATA: {m_status}")


def run():
    print("\n🚀 Formadores de Mercado — Refresh de Dados")
    print("=" * 52)

    # ── 1. Pools DeFi ──────────────────────────────────────
    pools = fetch_defi_pools()
    if pools:
        with open(POOLS_JSON, "w") as f:
            json.dump(pools, f, indent=2)
        print(f"   💾 Salvo: {POOLS_JSON}")
    else:
        print("   ⚠️  Usando pools.json existente (API indisponível)")
        with open(POOLS_JSON) as f:
            pools = json.load(f)

    # ── 2. Mercado Tradicional ─────────────────────────────
    fed_data = fetch_federal_reserve()
    bcb_data = fetch_bcb()
    market   = build_market_data(fed_data, bcb_data)
    with open(MARKET_JSON, "w") as f:
        json.dump(market, f, indent=2)
    print(f"   💾 Salvo: {MARKET_JSON}")

    # OUTPUT_DIR == BASE_DIR — JSONs já estão no lugar certo, cópia desnecessária

    # ── 3. Atualizar HTML dashboard ────────────────────────
    print("\n🌐 Atualizando dashboard HTML…")
    update_html_dashboard(pools, market)

    # ── 4. Resumo ──────────────────────────────────────────
    print("\n📊 Resumo dos dados coletados:")
    print(f"   DeFi pools:    {len(pools)} pools")
    print(f"   T-Bill 1 ano:  {market['tbill_1y']}%")
    print(f"   T-Bond 10 anos:{market['tbond_10y']}%")
    print(f"   SOFR:          {market['sofr']}%  →  Hi-Yield Savings: {market['hi_yield_savings']}%")
    print(f"   Selic:         {market['selic_meta']}%")
    print(f"   IPCA 12m:      {market['ipca_12m']}%")
    print(f"   Selic real BRL:{market['selic_real_brl']}%")
    print(f"   Selic adj. USD:{market['selic_usd_hist']}%")
    print(f"   USD/BRL:       {market['usd_brl']}")
    print(f"   Atualizado:    {market['updated_at'][:19]} UTC")

    # ── 5. Gerar PDF (apenas localmente, não no CI) ─────────
    if not os.environ.get("CI"):
        print("\n📄 Gerando PDF one-pager…")
        ret = subprocess.run([sys.executable, PDF_SCRIPT], cwd=BASE_DIR).returncode
        if ret == 0:
            print("   ✅ PDF atualizado com sucesso")
        else:
            print("   ❌ Erro ao gerar PDF")
    else:
        print("\n⏭️  PDF ignorado (ambiente CI)")

    print("\n✅ Refresh completo!\n")
    return pools, market


if __name__ == "__main__":
    run()
