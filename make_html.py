#!/usr/bin/env python3
"""Generate a styled HTML page from the collocates CSV results."""

import pandas as pd

CSV_FILE = "collocates_王小波.csv"
HTML_FILE = "collocates_王小波.html"


def main() -> None:
    df = pd.read_csv(CSV_FILE)
    df = df.sort_values("p_value")

    rows = []
    for _, r in df.iterrows():
        p = r["p_value"]
        p_str = f"{p:.2e}" if p < 0.001 else f"{p:.4f}"
        sig = "★★★" if p < 1e-4 else "★★" if p < 1e-3 else "★" if p < 0.01 else ""
        rows.append(
            f"<tr>"
            f"<td class='word'>{r['collocate']}</td>"
            f"<td>{int(r['obs_local'])}</td>"
            f"<td>{r['exp_local']:.2f}</td>"
            f"<td>{r['ratio_local']:.1f}×</td>"
            f"<td>{int(r['obs_global'])}</td>"
            f"<td>{p_str}</td>"
            f"<td class='sig'>{sig}</td>"
            f"</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="zh-Hans">
<head>
<meta charset="utf-8">
<title>「王小波」的显著搭配词 — 《黄金时代》</title>
<style>
  :root {{
    --bg: #faf9f6; --card: #ffffff; --ink: #2b2b2b; --muted: #8a8a8a;
    --accent: #b03a2e; --line: #e8e4dc;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; padding: 2rem 1rem; background: var(--bg); color: var(--ink);
    font-family: "Noto Serif SC", "Songti SC", "SimSun", serif;
    line-height: 1.6;
  }}
  .container {{ max-width: 860px; margin: 0 auto; }}
  header {{ text-align: center; margin-bottom: 2rem; }}
  h1 {{ font-size: 1.6rem; margin: 0 0 .4rem; letter-spacing: .05em; }}
  h1 .target {{ color: var(--accent); }}
  .subtitle {{ color: var(--muted); font-size: .95rem; }}
  .stats {{
    display: flex; justify-content: center; gap: 2rem; margin: 1.2rem 0;
    flex-wrap: wrap;
  }}
  .stat {{ text-align: center; }}
  .stat .num {{ font-size: 1.5rem; font-weight: 600; color: var(--accent); }}
  .stat .label {{ font-size: .8rem; color: var(--muted); }}
  .card {{
    background: var(--card); border: 1px solid var(--line); border-radius: 10px;
    padding: 1rem 1.4rem; box-shadow: 0 1px 4px rgba(0,0,0,.04);
  }}
  table {{ width: 100%; border-collapse: collapse; font-size: .95rem; }}
  th {{
    text-align: left; padding: .5rem .6rem; border-bottom: 2px solid var(--line);
    font-weight: 600; font-size: .85rem; color: var(--muted);
    position: sticky; top: 0; background: var(--card);
  }}
  td {{ padding: .45rem .6rem; border-bottom: 1px solid var(--line); }}
  tr:hover td {{ background: #f5f1ea; }}
  td.word {{ font-weight: 600; }}
  td.sig {{ color: var(--accent); letter-spacing: .1em; }}
  .note {{ color: var(--muted); font-size: .8rem; margin-top: 1rem; text-align: center; }}
  input#search {{
    width: 100%; padding: .55rem .9rem; margin-bottom: 1rem;
    border: 1px solid var(--line); border-radius: 6px; font-size: 1rem;
    font-family: inherit; background: var(--card);
  }}
  input#search:focus {{ outline: none; border-color: var(--accent); }}
</style>
</head>
<body>
<div class="container">
  <header>
    <h1>「<span class="target">王小波</span>」的显著搭配词</h1>
    <div class="subtitle">《黄金时代》· 王小波 — 搭配词分析（window 法，左右各 5 词，p ≤ 0.05）</div>
    <div class="stats">
      <div class="stat"><div class="num">{len(df)}</div><div class="label">显著搭配词</div></div>
      <div class="stat"><div class="num">{int(df['obs_local'].sum())}</div><div class="label">共现总次数</div></div>
      <div class="stat"><div class="num">{df['collocate'].iloc[0]}</div><div class="label">最显著搭配词</div></div>
    </div>
  </header>
  <div class="card">
    <input id="search" type="text" placeholder="搜索搭配词…">
    <table>
      <thead>
        <tr>
          <th>搭配词</th><th>局部共现</th><th>期望频数</th>
          <th>比率</th><th>全局频次</th><th>p 值</th><th>显著性</th>
        </tr>
      </thead>
      <tbody id="rows">
        {''.join(rows)}
      </tbody>
    </table>
  </div>
  <p class="note">★ p &lt; 0.01 · ★★ p &lt; 0.001 · ★★★ p &lt; 0.0001 — 由 qhchina.find_collocates 计算</p>
</div>
<script>
  document.getElementById('search').addEventListener('input', e => {{
    const q = e.target.value.trim();
    document.querySelectorAll('#rows tr').forEach(tr => {{
      tr.style.display = tr.textContent.includes(q) ? '' : 'none';
    }});
  }});
</script>
</body>
</html>"""

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved {HTML_FILE} with {len(df)} collocates")


if __name__ == "__main__":
    main()