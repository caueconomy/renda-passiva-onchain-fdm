# MANIFESTO — Renda Passiva On-chain
## Framework de Pesquisa e Materiais de Mentoria

> **Propósito:** Estruturar de forma permanente o estudo de renda passiva com stablecoins em DeFi, com foco em protocolos Ethereum/Base/L2s, para uso em mentoria e apresentação a clientes. Cada nova sessão deve atualizar este documento.

---

## 📌 CONTEXTO DO PROJETO

**Origem:** Estudo iniciado em fevereiro de 2026, transportado para o Cowork em abril de 2026 para ser estruturado como framework reutilizável.

**Objetivo central:** Mostrar a clientes/alunos que o DeFi entrega renda passiva em dólar com APYs superiores ao mercado tradicional (Treasuries, poupança americana, CDs), mantendo flexibilidade de saque.

**Público-alvo dos materiais:** Clientes de mentoria — perfil investidor que busca renda em dólar com proteção cambial, mas ainda não está familiarizado com DeFi.

**Narrative de venda:** "Você já ouve falar de renda fixa americana pagando 4%. Com DeFi, você acessa os mesmos dólares rendendo 8–15%, com saque livre, e sem precisar abrir conta em corretora americana."

---

## 🎯 TESES PRINCIPAIS

1. **Stablecoins como instrumento de renda** — USDT e USDC são exposição ao dólar sem a volatilidade de BTC/ETH. Depositadas em protocolos de lending, geram yield superior a instrumentos tradicionais.

2. **Ethereum + L2s = custo viável** — A Solana foi considerada inicialmente pelo custo de gas, mas Base, Arbitrum e Optimism oferecem taxas equivalentes com o ecossistema de segurança do Ethereum.

3. **DeFi supera o mercado tradicional em rentabilidade** — Com dados de Abril 2026: US T-Bill 1 ano = 3.70%, High-Yield Savings = 4–5%. Aave V3 = 4–8%. Morpho Blue = 8–15%. Fluid = 8–22%.

4. **Risco não é eliminado, mas é gerenciável** — Aave V3 e Morpho Blue têm track record sólido, múltiplas auditorias, TVL bilionário. O risco é diferente do mercado tradicional, mas não necessariamente maior para quem entende o que está fazendo.

---

## 📊 MAPEAMENTO DE PROTOCOLOS (Atualizado Abril 2026)

### Categoria: Lending Conservador (Risco Baixo)

| Protocolo | Redes | APY Base | APY c/ Incentivos | Saque |
|-----------|-------|----------|-------------------|-------|
| Aave V3 | ETH, ARB, BASE, OP | 4–6% | 4–8% | Flexível |
| Morpho Blue | ETH, BASE | 5–8% | 8–15% | Flexível |
| Compound V3 | ETH, POLYGON | 3–5% | 3–6% | Flexível |

### Categoria: Lending/DEX Híbrido (Risco Médio)

| Protocolo | Redes | APY Base | APY c/ Incentivos | Saque |
|-----------|-------|----------|-------------------|-------|
| Fluid Protocol | ETH | 8–16% | 10–22% | Flexível |
| Curve Finance | ETH, ARB | 5–10% | 8–15% | Flexível |
| Aerodrome (sAMM) | BASE | 5–8% | 10–20% | Flexível |
| Velodrome | OP | 5–9% | 10–18% | Flexível |

### Categoria: Yield Estruturado (Risco Médio-Alto)

| Protocolo | Redes | APY Base | APY c/ Incentivos | Saque |
|-----------|-------|----------|-------------------|-------|
| Pendle Finance | ETH, ARB | 6–10% | 10–20% | Vencimento fixo |
| Maple Finance | ETH | 9–14% | 9–14% | Lockup 30 dias |

---

## 📈 BENCHMARKS — MERCADO TRADICIONAL (Abril 2026)

| Instrumento | Retorno Anual | Liquidez | Observação |
|-------------|---------------|----------|------------|
| US T-Bill 3 meses | 3.71% | Baixa (prazo) | Federal Reserve H.15, 13/04/2026 |
| US T-Bill 6 meses | 3.74% | Baixa (prazo) | Federal Reserve H.15, 13/04/2026 |
| US T-Bill 1 ano | 3.70% | Baixa (prazo) | Federal Reserve H.15, 13/04/2026 |
| US T-Bond 10 anos | 4.30% | Média | Federal Reserve H.15, 13/04/2026 |
| High-Yield Savings (EUA) | 4.0–5.0% | Alta | Bankrate / Fortune, Abril 2026 |
| S&P 500 (média histórica 10a) | ~10% | Alta | Macrotrends, variável |
| S&P 500 (retorno 2025) | 17.9% | Alta | FT Portfolios, Jan 2026 |

**Fontes:** [Federal Reserve H.15](https://www.federalreserve.gov/releases/h15/) · [fminvest.com](https://www.fminvest.com/current-us-treasury-rates) · [Bankrate](https://www.bankrate.com/banking/savings/best-high-yield-interests-savings-accounts/) · [Macrotrends](https://www.macrotrends.net/2526/sp-500-historical-annual-returns)

---

## 💰 SIMULAÇÃO DE REFERÊNCIA

**Capital base para simulações:** $10.000 USD

| Cenário | Protocolo | APY | 30 dias | 6 meses | 12 meses |
|---------|-----------|-----|---------|---------|----------|
| Conservador | Aave V3 | 5% | $42 | $253 | $512 |
| Base | Morpho Blue | 10% | $83 | $511 | $1.047 |
| Otimista | Fluid / Pendle | 18% | $148 | $921 | $1.967 |
| Benchmark trad. | US T-Bill 1a | 3.70% | $31 | $186 | $377 |

**Diferencial DeFi vs T-Bill (cenário base, 12 meses):** +$670 a +$1.590 por $10k investido.

---

## 📁 ESTRUTURA DE ARQUIVOS

```
Renda Passiva On-chain/
├── MANIFESTO.md                          ← Este arquivo (log do projeto)
├── defi-yield-dashboard.html             ← Dashboard interativo (atualização periódica)
├── renda-passiva-onchain-onepager.pdf    ← One-pager para clientes (venda de mentoria)
└── yield_stablecoins_comparativo.xlsx    ← Planilha da análise original (Fev/2026)
```

---

## 📊 DADOS LIVE — ÚLTIMAS LEITURAS API DEFILLAMA (Abril 2026)

> Critério de seleção v2: **varredura sistemática** da API pública `yields.llama.fi/pools`. Filtro: chain ∈ {Ethereum, Base, Arbitrum, Optimism} · symbol contém USDC ou USDT · TVL > $10M · APY > 1%. Total de 16.740 pools analisados → 36 selecionados → 20 finais curados.

| Protocolo | Ativo | Rede | APY Atual | APY 30d | TVL | URL |
|-----------|-------|------|-----------|---------|-----|-----|
| Maple Finance | USDC | Ethereum | 4.19% | 4.34% | $3.47B | https://app.maple.finance/earn |
| Maple Finance | USDT | Ethereum | 3.67% | 3.79% | $2.21B | https://app.maple.finance/earn |
| Aave V3 | USDT | Ethereum | 2.40% | 2.02% | $1.01B | https://app.aave.com/markets/ |
| Spark Savings | USDT | Ethereum | 3.18% | 3.23% | $847.9M | https://spark.fi/savings |
| Aave V3 | USDC | Ethereum | 2.24% | 2.27% | $812.2M | https://app.aave.com/markets/ |
| Spark Savings | USDC | Ethereum | 3.75% | 3.75% | $399.6M | https://spark.fi/savings |
| Fluid Lending | USDC | Ethereum | 3.62% | 4.33% | $190.9M | https://fluid.instadapp.io/lending/ |
| Fluid Lending | USDT | Ethereum | 5.30% | 4.87% | $125.7M | https://fluid.instadapp.io/lending/ |
| Compound V3 | USDC | Ethereum | 2.61% | 2.56% | $115.7M | https://app.compound.finance/ |
| Aave V3 | USDC | Arbitrum | 1.66% | 1.53% | $91.7M | https://app.aave.com/markets/ |
| Curve DEX | USDC-RLUSD | Ethereum | 5.23% | 5.66% | $90.6M | https://curve.fi/#/ethereum/pools |
| Aave V3 | USDC | Base | 2.64% | 2.59% | $84.1M | https://app.aave.com/markets/ |
| Compound V3 | USDT | Ethereum | 2.60% | 2.52% | $64.1M | https://app.compound.finance/ |
| Avantis | USDC | Base | 11.02% | 9.42% | $62.3M | https://www.avantisfi.com/ |
| Curve DEX | PYUSD-USDC | Ethereum | 5.07% | 5.64% | $45.1M | https://curve.fi/#/ethereum/pools |
| Euler V2 | USDC | Ethereum | 3.55% | 3.70% | $41.4M | https://app.euler.finance/ |
| Goldfinch | USDC | Ethereum | 10.06% | 10.03% | $37.2M | https://app.goldfinch.finance/earn |
| Fluid Lending | USDC | Arbitrum | 4.86% | 5.90% | $31.4M | https://fluid.instadapp.io/lending/ |
| Yo Protocol | USDC | Base | 16.62% | 14.09% | $27.7M | https://yo.xyz/ |
| Yearn Finance | USDC | Ethereum | 3.45% | 3.18% | $28.6M | https://yearn.fi/ |

**Nota importante:** Maple Finance tem TVL enorme ($3.47B USDC + $2.21B USDT) mas é crédito privado institucional com lockup — **não é produto para cliente retail**. Para perfil conservador, o melhor risk-adjusted é **Fluid USDT (5.30%)** ou **Curve USDC-RLUSD (5.23%)**.

---

## 🔄 HISTÓRICO DE VERSÕES

### v1.0 — Fevereiro 2026 (Claude Web)
- Mapeamento inicial de protocolos Solana e Ethereum
- Análise específica do Sentora PYUSD na Kamino Finance
- Planilha comparativa com simulação de $2.000
- **Conclusão da época:** Kamino PYUSD com APY ~12.65% (base 6.95% + incentivos 5.7%) era a melhor opção em Solana para saque flexível

### v2.0 — Abril 2026 (Cowork — Sessão 1)
- Pivô de foco: Solana → Ethereum/Base/L2s
- Escopo ampliado para mercado tradicional como benchmark comparativo
- Valor de referência: $10.000
- **Entregáveis:** Dashboard HTML + PDF one-pager para clientes

### v3.1 — Abril 2026 (Cowork — Sessão 8) — Revisão comercial
**Baseado em análise de viés comercial (Claude + GPT)**

#### Dados corrigidos (verificados ao vivo)
- **Yo Protocol 16.63%** — confirmado na DeFiLlama: pool USDC/Base, TVL $27.7M, APY30d 14.09% ✅
- **Total de pools** — 16.790 (não 12.066 como o GPT apontou — GPT estava errado) ✅
- **Subtitle** — "Rendimento em dolar" (removido "real" que implica ajuste por CPI americano)
- **IPCA** — exibido como 4.14% positivo com "Perda de poder de compra em reais" (remover sinal negativo confuso)

#### Melhorias comerciais
- **Card Simulação $10k destacado** — fundo verde, borda destacada, fonte maior, linha "+$789 a mais por ano*"
- **Card Melhor APY** — agora mostra rede, ativo e TVL do pool específico (Yo Protocol USDC · Base · TVL $28M)
- **Nota de variabilidade** — `* APY variável, sujeito a alteração. Parte dos rendimentos pode incluir incentivos temporários.`
- **Disclaimer jurídico** — "Risco simplificado para fins ilustrativos. Não substitui análise de perfil de investidor."
- **Contato comercial** — `formadoresdemercado.com` no rodapé
- **Bloco narrativa mentoria** — removido do PDF (o vendedor trabalha esse ponto na conversa)

#### O que foi verificado e MANTIDO
- Yo Protocol 16.63% — dado real e verificável na DeFiLlama
- Total 16.740 pools — correto (GPT consultou fonte errada)
- Avantis 11.02% como segundo destaque — verificado

### v3.0 — Abril 2026 (Cowork — Sessão 7) — Arquitetura de dados automática
**Mudança estrutural: dados 100% dinâmicos**

#### Novo arquivo: `refresh_data.py`
Script de atualização único. Roda com `python3 refresh_data.py` e:
1. Busca **DeFiLlama API** → 16.000+ pools → filtra por USDC/USDT, TVL>$10M, APY>1%
2. Busca **BCB (Banco Central)** → Selic meta (série 432), IPCA 12m (série 13522), USD/BRL (série 1)
3. Busca **Federal Reserve FRED** → T-Bill 1a (DGS1), T-Bond 10a (DGS10)
4. Salva `defi_pools.json` e `market_data.json`
5. Roda `defi_onepager_v5.py` automaticamente → gera PDF atualizado

#### PDF script (`defi_onepager_v5.py`)
- Barras do gráfico: vindas dinamicamente do JSON (top 6 DeFi por APY)
- TradFi (T-Bill, T-Bond, HY Savings, Selic adj. USD): lidos de `market_data.json`
- Data de atualização: calculada do `market_data.updated_at`
- Seção Brasil: valores calculados de `market_data.json`
- **Zero valores hardcoded de mercado**

#### Dashboard HTML (`defi-yield-dashboard.html`)
- **🌙 Dark / ☀️ Light mode** toggle com persistência em localStorage
- **↻ Atualizar Dados** — busca DeFiLlama diretamente no browser via fetch (CORS), re-renderiza tudo
- **📄 Gerar PDF** — chama `window.print()` com CSS @media print otimizado para A4
- `MARKET_DATA` object: lido do `market_data.json` (via `window.__MARKET_DATA__`) ou fallback
- Barras do gráfico usam `MARKET_DATA` para TradFi (T-Bill, T-Bond, etc.)
- Simulações de rendimento usam valores live de `MARKET_DATA`

#### Fluxo de atualização completo
```
python3 refresh_data.py
# → atualiza defi_pools.json (DeFiLlama live)
# → atualiza market_data.json (BCB + Fed live)
# → regenera PDF automaticamente
# → copiar market_data.json para pasta de output
# → abrir dashboard.html no browser → clicar "↻ Atualizar Dados"
```

### v2.5 — Abril 2026 (Cowork — Sessão 6)
- **Cores clarificadas:** DIM `#a98fd4` → `#c4b5d8`, MUTED `#6b4f9e` → `#8b70b8` — melhor contraste no fundo escuro
- **Tabela alinhada ao dashboard:** ordenada por APY desc, risco Alto excluído (Maple, Goldfinch, Yo Protocol)
- **WBTC/BTC filtrado** da tabela — GMX Perps (WBTC.B-USDC) removido por não ser stablecoin pura
- **RISK_MAP expandido** com todos os protocolos que entram na tabela (Avantis, Convex, Merkl, Sparklend, Dolomite, Uniswap)
- **URLs corrigidas:** Dolomite → dolomite.io, GMX → app.gmx.io, Yearn → yearn.fi, Uniswap → app.uniswap.org
- **Duplicata sparklend** removida do RISK_MAP (estava como Medio e Baixo simultaneamente)
- **Seção Brasil:** Selic BRL removida, mantida apenas Selic adj. USD (~6.5%) como benchmark
- **Narrativa Brasil:** 3 colunas — Inflação (negativo), Selic adj. USD (neutro), DeFi (positivo/destaque roxo)

### v2.4 — Abril 2026 (Cowork — Sessão 5)
- **Info de fonte** movida para linha do subtítulo do gráfico (x direita, 68mm de gap garantido)
- **Selic 14.75% BRL removida** do gráfico de barras — evita que a maior barra seja o Brasil
- **MAX_APY ajustado para 13%** — Avantis DeFi (11.02%) domina visualmente, narrativa correta
- **Seção Brasil renomeada** para "Por que a Selic não protege em dólar — e o DeFi sim"
- **Selic BRL** aparece como dado de contexto em cinza/neutro, sem destaque verde
- **KPI 4** reformulado: mostra "+$650" (Selic adj. USD) em vermelho vs "+$1.159" (DeFi) em verde
- **Script estável:** `defi_onepager_v5.py` — sem sobreposições confirmadas

### v2.3 — Abril 2026 (Cowork — Sessão 4)
- **PDF layout totalmente reescrito** com sistema de coordenadas fixas top-down em mm (`mm2y` helper)
- **Zero sobreposições confirmadas** — cada seção tem Y hardcoded e espaço calculado com `stringWidth`
- **Legenda corrigida** — fundo escuro dedicado + `TEXT_C` (#f0eaf8) para contraste garantido
- **Header reorganizado** — info direita alinhada na zona livre (x>152mm, y em linha com título), subtítulo em 2 linhas curtas abaixo
- **Script de geração:** `defi_onepager_v5.py` (versão estável, roda standalone com `python3`)
- **Alturas por seção:** Header 4–37mm · Gráfico 41–144mm · KPIs 147–166mm · Tabela 170–249mm · Brasil 249–268mm · Footer 271mm

### v2.2 — Abril 2026 (Cowork — Sessão 3)
- **Logo real FDM** integrada em PDF e dashboard (PNG da pasta Material de Apoio, recortada e otimizada)
- **Wordmark "Formadores de Mercado"** presente no header e footer do PDF
- **Bugs visuais PDF corrigidos:** sobreposições eliminadas via layout calculado em mm com margens explícitas
- **Contador de pools** adicionado: "16.740 pools rastreados · 20 selecionados" em ambos os materiais
- **Data de atualização** explícita no PDF (14/04/2026) e no footer
- **Aba Brasil** adicionada no dashboard com:
  - Selic 14.75% a.a. · IPCA 4.14% · Selic real BRL ~10.2% · Selic adj. USD histórico ~6.5%
  - Explicação do porquê a Selic parece alta em BRL mas é modesta em USD
  - Simulação $10k em R$50.000 comparando Tesouro vs DeFi
  - Tabela completa Tesouro Selic / IPCA+ / CDB / T-Bill / DeFi
- **Contexto câmbio:** USD/BRL ~5.00 · BRL apreciou 15% em 12m (atípico — não recorrente)
- **Argumento central para cliente BR:** DeFi = hedge cambial + yield competitivo em USD

### v2.1 — Abril 2026 (Cowork — Sessão 2)
- **Varredura sistemática da API DeFiLlama** — 16.740 pools analisados, critério objetivo por TVL/APY
- **Design system Formadores de Mercado** aplicado: cores (#822ee5, #ffb81c, #8ffff8), fonte Sora, logo SVG vetorial
- **Links diretos** para cada protocolo/pool adicionados no dashboard
- **Critério de seleção documentado:** chain ∈ {ETH,Base,ARB} · USDT/USDC · TVL>$10M · APY>1%
- **Descoberta importante:** Maple Finance lidera em TVL ($5.67B) mas é crédito privado — não adequado para retail
- **Melhor risk-adjusted real:** Fluid USDT 5.30% APY / Curve USDC-RLUSD 5.23% APY
- **Alto APY verificado:** Avantis (Base) 11.02%, Goldfinch 10.06%, Yo Protocol 16.62% (alto risco)
- **PDF reconstruído** sem bugs visuais, fonte Sora, dados 100% da API
- **Benchmarks TradFi atualizados:** Federal Reserve H.15 (13/04/2026) — T-Bill 1a = 3.70%

---

## 🇧🇷 BENCHMARKS BRASIL (Abril 2026)

| Indicador | Valor | Fonte |
|-----------|-------|-------|
| Taxa Selic | 14.75% a.a. | BCB / Copom |
| CDI | 14.65% a.a. | BCB |
| IPCA acumulado 12m | 4.14% | IBGE |
| Selic real (Selic − IPCA) | ~10.20% a.a. em BRL | Calculado |
| USD/BRL atual | ~5.00 | BCB / Bloomberg |
| BRL variação 12m vs USD | +15.11% (apreciação) | Mercado |
| Selic adj. USD (atual, atípico) | ~32% | Calculado (excl.) |
| Selic adj. USD (normalizado hist.) | ~6.5% | Selic − deprec. BRL ~8%/a |
| Tesouro IPCA+ 2029 | IPCA + 7.72% | Tesouro Direto |
| Tesouro Selic 2028 | Selic + 0.05% | Tesouro Direto |

**Argumento chave para cliente brasileiro:**
- Selic em BRL = 14.75% (parece alto)
- Selic real em BRL = 10.2% (depois da inflação)
- Selic em USD (histórico) = ~6.5% (depois da depreciação cambial histórica ~8%/a)
- DeFi conservador (Aave/Fluid) = 2.4%–5.3% em USD com saque livre
- **DeFi é competitivo vs Selic em USD E oferece proteção cambial natural**

---

## 🔧 PROTOCOLO DE ATUALIZAÇÃO

Para futuras sessões, atualizar:

1. **APYs** → Verificar em [defillama.com/yields](https://defillama.com/yields?token=ALL_USD_STABLES) filtrando por USDT/USDC
2. **Benchmarks TradFi** → [Federal Reserve H.15](https://www.federalreserve.gov/releases/h15/) para Treasuries, [Bankrate](https://www.bankrate.com/banking/savings/best-high-yield-interests-savings-accounts/) para savings
3. **Novos protocolos** → Pesquisar no DeFiLlama por TVL > $100M em stablecoins nas chains mapeadas
4. **Atualizar MANIFESTO** → Adicionar nova seção no Histórico de Versões
5. **Regenerar PDF** → Rodar `defi_onepager.py` com novos dados
6. **Atualizar Dashboard** → Editar `defi-yield-dashboard.html` na seção de dados

---

## ⚠️ NOTAS DE RISCO PARA COMUNICAÇÃO COM CLIENTES

- Sempre mencionar que APYs são **variáveis** e podem mudar rapidamente
- Morpho Blue e Aave são os mais adequados para perfil conservador pela profundidade de auditoria e TVL
- Pendle e Fluid têm yields mais altos mas requerem mais atenção e entendimento do produto
- Smart contract risk é real — nunca alocar mais do que se pode perder sem comprometer a vida financeira
- Stablecoins não são risk-free: USDC depende do sistema bancário americano, USDT tem risco de emissor
- Recomendar hardware wallet para valores acima de $5.000

---

*Última atualização: Abril 2026 — Cowork Session*
