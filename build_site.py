# -*- coding: utf-8 -*-
"""Build docs/index.html by inlining apis.json so the site works on GitHub Pages and file://."""
import json, pathlib

root = pathlib.Path(__file__).parent
data = json.loads((root / "apis.json").read_text(encoding="utf-8"))
docs = root / "docs"
docs.mkdir(exist_ok=True)

html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Free APIs 中文精选 - 真正可用的免费 API 大全</title>
<meta name="description" content="精选国内外真正可用的免费 API，标注是否需要注册 Key，开发者必备收藏">
<style>
  :root {
    --bg: #f6f8f7; --card: #ffffff; --text: #1f2328; --muted: #656d76;
    --accent: #0e9f6e; --accent-soft: #e7f6f0; --border: #e3e6ea; --radius: 14px;
    --warn: #b7791f; --warn-soft: #fdf3e3;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
         background: var(--bg); color: var(--text); line-height: 1.6; }
  .wrap { max-width: 1080px; margin: 0 auto; padding: 0 20px; }
  header.hero { text-align: center; padding: 64px 20px 36px; }
  header.hero h1 { font-size: 2.4rem; letter-spacing: -0.5px; }
  header.hero p.sub { color: var(--muted); margin-top: 12px; font-size: 1.05rem; }
  .stats { margin-top: 18px; display: flex; gap: 24px; justify-content: center; flex-wrap: wrap; }
  .stat { background: var(--card); border: 1px solid var(--border); border-radius: 999px;
          padding: 6px 18px; font-size: 0.9rem; color: var(--muted); }
  .stat b { color: var(--accent); }
  .toolbar { position: sticky; top: 0; z-index: 10; background: rgba(246,248,247,0.92);
             backdrop-filter: blur(8px); padding: 14px 0 10px; border-bottom: 1px solid var(--border); }
  .search { width: 100%; padding: 12px 18px; border: 1px solid var(--border); border-radius: 999px;
            font-size: 1rem; background: var(--card); outline: none; transition: border-color .15s; }
  .search:focus { border-color: var(--accent); }
  .chips { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
  .chip { padding: 5px 14px; border-radius: 999px; border: 1px solid var(--border);
          background: var(--card); cursor: pointer; font-size: 0.88rem; color: var(--muted);
          transition: all .15s; user-select: none; }
  .chip:hover { border-color: var(--accent); color: var(--accent); }
  .chip.active { background: var(--accent); border-color: var(--accent); color: #fff; }
  main { padding: 28px 0 60px; }
  .cat-title { display: flex; align-items: baseline; gap: 10px; margin: 30px 0 14px; }
  .cat-title h2 { font-size: 1.25rem; }
  .cat-title span { color: var(--muted); font-size: 0.85rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 14px; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius);
          padding: 18px 20px; transition: transform .15s, box-shadow .15s; display: flex; flex-direction: column; }
  .card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(31,35,40,0.08); }
  .card .head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
  .card h3 { font-size: 1.02rem; }
  .badge { flex-shrink: 0; font-size: 0.72rem; border-radius: 6px; padding: 2px 8px; font-weight: 600; }
  .badge.no { background: var(--accent-soft); color: var(--accent); }
  .badge.key { background: var(--warn-soft); color: var(--warn); }
  .card p.desc { color: var(--muted); font-size: 0.88rem; margin: 8px 0 0; flex: 1; }
  .card .note { margin-top: 8px; font-size: 0.8rem; color: var(--warn); }
  .card .example { margin-top: 10px; background: #f0f2f5; border-radius: 8px; padding: 8px 10px;
                   font-family: "SF Mono", Consolas, monospace; font-size: 0.75rem; color: #444;
                   overflow-x: auto; white-space: nowrap; }
  .card .foot { margin-top: 12px; display: flex; gap: 8px; }
  .btn { padding: 7px 14px; border-radius: 8px; border: 1px solid var(--border); font-size: 0.82rem;
         background: var(--card); color: var(--accent); text-decoration: none; cursor: pointer;
         transition: all .15s; }
  .btn:hover { border-color: var(--accent); }
  footer { text-align: center; padding: 36px 20px 48px; color: var(--muted); font-size: 0.88rem; }
  footer a { color: var(--accent); text-decoration: none; }
  .empty { text-align: center; color: var(--muted); padding: 60px 0; }
  .toast { position: fixed; left: 50%; bottom: 32px; transform: translateX(-50%);
           background: #1f2328; color: #fff; padding: 10px 22px; border-radius: 999px;
           font-size: 0.9rem; opacity: 0; transition: opacity .25s; pointer-events: none; z-index: 99; }
  .toast.show { opacity: 1; }
  @media (max-width: 600px) { header.hero h1 { font-size: 1.8rem; } }
</style>
</head>
<body>
<header class="hero">
  <h1>🔌 Free APIs 中文精选</h1>
  <p class="sub">精选国内外真正可用的免费 API · 标注是否需要注册 Key · 开发者必备收藏</p>
  <div class="stats">
    <div class="stat"><b id="statApis">0</b> 个 API</div>
    <div class="stat"><b id="statFree">0</b> 个无需 Key</div>
    <div class="stat">CC0 协议 · 随意使用</div>
  </div>
</header>

<div class="toolbar">
  <div class="wrap">
    <input class="search" id="search" type="search" placeholder="🔍 搜索 API，如：天气、翻译、二维码…">
    <div class="chips" id="chips"></div>
  </div>
</div>

<main class="wrap" id="main"></main>

<div class="toast" id="toast">已复制到剪贴板 ✅</div>

<footer>
  <p>用 ❤️ 维护 · <a href="https://github.com/AnonymousLeeJJ/free-apis-zh" target="_blank" rel="noopener">GitHub 仓库</a> · 欢迎 Star ⭐ 与投稿</p>
</footer>

<script id="apis-data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('apis-data').textContent);
const { categories, apis } = DATA;
const state = { q: '', cat: 'all' };

document.getElementById('statApis').textContent = apis.length;
document.getElementById('statFree').textContent = apis.filter(a => a.auth === 'no').length;

const chipsEl = document.getElementById('chips');
const mainEl = document.getElementById('main');
const toast = document.getElementById('toast');

function renderChips() {
  const all = [{ id: 'all', name: '全部', icon: '✨' }, ...categories,
               { id: 'nokey', name: '无需 Key', icon: '🆓' }];
  chipsEl.innerHTML = all.map(c =>
    `<span class="chip ${state.cat === c.id ? 'active' : ''}" data-id="${c.id}">${c.icon || ''} ${c.name}</span>`
  ).join('');
  chipsEl.querySelectorAll('.chip').forEach(el =>
    el.addEventListener('click', () => { state.cat = el.dataset.id; renderChips(); renderList(); }));
}

function matches(a) {
  if (state.cat === 'nokey' && a.auth !== 'no') return false;
  if (state.cat !== 'all' && state.cat !== 'nokey' && a.category !== state.cat) return false;
  if (!state.q) return true;
  const q = state.q.toLowerCase();
  return (a.name + a.description + (a.example || '')).toLowerCase().includes(q);
}

function copyText(text) {
  if (navigator.clipboard) { navigator.clipboard.writeText(text).catch(() => {}); }
  else { const ta = document.createElement('textarea'); ta.value = text;
    document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); }
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 1500);
}

function renderList() {
  const groups = categories
    .map(c => ({ cat: c, items: apis.filter(a => a.category === c.id && matches(a)) }))
    .filter(g => g.items.length);
  if (!groups.length) {
    mainEl.innerHTML = '<div class="empty">没有找到匹配的 API，换个关键词试试 🧐</div>';
    return;
  }
  mainEl.innerHTML = groups.map(g => `
    <div class="cat-title"><h2>${g.cat.icon} ${g.cat.name}</h2><span>${g.items.length} 个</span></div>
    <div class="grid">${g.items.map(a => `
      <div class="card">
        <div class="head"><h3>${a.name}</h3>
          <span class="badge ${a.auth}">${a.auth === 'no' ? '无需 Key' : '需注册 Key'}</span></div>
        <p class="desc">${a.description}</p>
        ${a.note ? `<div class="note">💡 ${a.note}</div>` : ''}
        ${a.example ? `<div class="example">${a.example}</div>` : ''}
        <div class="foot">
          <a class="btn" href="${a.url}" target="_blank" rel="noopener">📖 文档 / 官网</a>
          ${a.example ? `<button class="btn copy" data-url="${a.example.replace(/"/g, '&quot;')}">📋 复制示例</button>` : ''}
        </div>
      </div>`).join('')}
    </div>`).join('');
  mainEl.querySelectorAll('button.copy').forEach(el =>
    el.addEventListener('click', () => copyText(el.dataset.url)));
}

document.getElementById('search').addEventListener('input', e => { state.q = e.target.value.trim(); renderList(); });
renderChips();
renderList();
</script>
</body>
</html>
"""

html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))
(docs / "index.html").write_text(html, encoding="utf-8")
print("OK ->", docs / "index.html", f"({len(data['apis'])} apis)")
