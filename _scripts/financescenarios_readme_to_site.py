"""Turn the Finance Scenarios README's Functionality section into the landing page's, keeping the site's design.

    python _scripts/financescenarios_readme_to_site.py /path/to/FinanceScenarios/README.md _pages/financescenarios/financescenarios.md
"""
import re, sys
readme, page = sys.argv[1], sys.argv[2]
rd = open(readme).read()
fn = rd[rd.index('# Functionality'):rd.index('# Questions & Answers')]
fn = re.sub(r'___\n\n<b><div align="center">.*?</div></b>\n___\n\n', '', fn, flags=re.S)
fn = fn.replace('# Functionality', '## Functionality', 1)
charts = {'simulation': 'Simulated short rate, inflation and US equities', 'distribution': 'Distribution of the five-year US equity return',
          'portfolio': 'Simulated value of a 60/40 portfolio', 'regimes': 'US inflation in the baseline and under three stress regimes',
          'backtest': 'Historical value of the 60/40, All Weather and Permanent Portfolio mixes since 2000', 'solvency': 'Distribution of own funds after one year'}
LEAD = {'simulation': "Which draws the median of each variable with the bands that hold half and nine in ten of the scenarios:",
        'distribution': "Which shows where the five-year return lands across all 2,000 scenarios:",
        'portfolio': "Which shows the portfolio's value in money, with the same bands:",
        'regimes': "Which puts the four runs side by side:", 'backtest': "Which follows each mix month by month:",
        'solvency': "Which marks today's own funds and the 1-in-200 outcome:"}
fn = re.sub(r'<picture>.*?</picture>', lambda m: LEAD[re.search(r'readme/(\w+)-dark', m.group(0)).group(1)] + '\n\n' + '{% include ft-chart.html id="' + re.search(r'readme/(\w+)-dark', m.group(0)).group(1)
            + '" src="/assets/data/financescenarios-charts.json" label="' + charts[re.search(r'readme/(\w+)-dark', m.group(0)).group(1)] + '" %}', fn, flags=re.S)
icons = {'Settings profiles': 'fa-sliders-h', 'Factor sets': 'fa-layer-group', 'Stress regimes': 'fa-bolt', 'Portfolios': 'fa-chart-pie'}
fn = re.sub(r'<details>\n<summary><b>([A-Za-z ]+) \((\d+)\)</b>[^\n]*</summary>\n',
            lambda m: f'<details class="ft-details" markdown="1">\n<summary><i class="fas {icons[m.group(1)]}"></i> <b>{m.group(1)}</b> <span class="ft-details__meta">{m.group(2)}</span></summary>\n', fn)
fn = fn.replace('https://www.jeroenbouma.com/', '/')
fn = re.sub(r'\*\*Find ([^*\[]+?) \[here\]\((/[^)]+)\)', r'**Find [\1](\2)', fn)
fn = re.sub(r'the ([A-Za-z ]+?) \[here\]\((/[^)]+)\)', r'[the \1](\2)', fn)
fn = fn.replace('FinanceScenarios', 'Finance Scenarios').replace('### Simulating Scenarios', '### Simulating Scenarios {#simulating-scenarios}')
fn = re.sub(r'calibrated on \d{4}-\d{2}-\d{2}', 'calibrated on {{ site.data.financescenarios_run.date }}', fn)
fn = fn.replace('every chart is drawn from that same run', 'every chart is interactive and drawn from that same run')
fn = fn.replace("Every class also documents itself through Python's built-in help.",
                "Every class also documents itself through Python's built-in help, and the [documentation](/projects/financescenarios/docs) explains each model and its assumptions.")
s = open(page).read()
s = s[:s.index('## Functionality')] + fn.rstrip() + '\n\n' + s[s.index('## Notebooks'):]
open(page, 'w').write(s)
