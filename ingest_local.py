import urllib.request, re, os, json
BASE = 'D:/scholar/genai_w10/wiki'
os.makedirs(BASE, exist_ok=True)
SOURCES = {
    'react':        'https://arxiv.org/abs/2210.03629',
    'reflexion':    'https://arxiv.org/abs/2303.11366',
    'toolformer':   'https://arxiv.org/abs/2302.04761',
    'genagents':    'https://arxiv.org/abs/2304.03442',
    'crag':         'https://arxiv.org/abs/2401.15884',
}
records = []
for name, url in SOURCES.items():
    html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read().decode('utf-8','ignore')
    title = re.search(r'<meta name="citation_title" content="(.*?)"', html).group(1)
    authors = re.findall(r'<meta name="citation_author" content="(.*?)"', html)[:3]
    date = re.search(r'<meta name="citation_date" content="(.*?)"', html)
    absm = re.search(r'<meta name="citation_abstract" content="(.*?)"', html, re.S)
    abstract = re.sub(r'\s+', ' ', absm.group(1)).strip() if absm else ''
    with open(f'{BASE}/{name}.md', 'w', encoding='utf-8') as f:
        f.write(f'# {title}\n\n- 來源：{url}\n- 作者：{", ".join(authors)}\n- 日期：{date.group(1) if date else ""}\n\n## Abstract\n{abstract}\n')
    records.append({'name': name, 'title': title, 'url': url})
    print('[ingest ok]', name, title[:60])
with open(f'{BASE}/index.md', 'w', encoding='utf-8') as f:
    f.write('# AI Agents LLM Wiki — 目錄\n\n')
    for r in records:
        f.write(f"- [{r['title']}]({r['url']})（wiki/{r['name']}.md）\n")
print('files:', sorted(os.listdir(BASE)))
