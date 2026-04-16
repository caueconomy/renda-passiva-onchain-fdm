# Renda Passiva On-chain — Formadores de Mercado

Dashboard de yields DeFi em USDC/USDT com comparação contra mercado tradicional (T-Bill, Selic, IPCA).

**Acesso:** [fdm-renda-passiva.github.io](https://formadores-de-mercado.github.io/renda-passiva-onchain/) *(atualizar após publicar)*

---

## Atualizar os dados (time técnico)

Rodar o script abaixo atualiza os pools, dados de mercado e injeta tudo no dashboard:

```bash
cd "C:\Users\caueo\Desktop\Quant Strategies\Renda Passiva On-chain"
python refresh_data.py
```

Depois de rodar, fazer o commit e push para o GitHub atualizar a página online:

```bash
git add defi_pools.json market_data.json index.html
git commit -m "dados: refresh $(date +%d/%m/%Y)"
git push
```

A página online atualiza automaticamente em ~1 minuto após o push.

---

## Arquivos principais

| Arquivo | Descrição |
|---|---|
| `index.html` | Dashboard principal (abrir no browser) |
| `refresh_data.py` | Script Python — atualiza todos os dados |
| `defi_pools.json` | Pools selecionados (gerado pelo script) |
| `market_data.json` | Dados de mercado — T-Bill, Selic, IPCA (gerado pelo script) |
| `defi_onepager_v5.py` | Gerador do PDF one-pager (rodado automaticamente pelo refresh) |
| `logo-vertical.png` | Logo FDM horizontal (usada no PDF) |
| `logo-simbolo.png` | Símbolo FDM (usado no PDF e no dashboard) |

---

## Fontes de dados

- **DeFiLlama API** — APY e TVL dos pools DeFi (`yields.llama.fi/pools`)
- **Federal Reserve H.15** — T-Bill 1 ano, T-Bond 10 anos, SOFR
- **Banco Central do Brasil** — Selic, CDI, IPCA, USD/BRL

---

## Requisitos para rodar o script localmente

```bash
pip install requests reportlab
python refresh_data.py
```

Python 3.8+ requerido.
