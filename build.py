# -*- coding: utf-8 -*-
"""Build a bilingual AI and agent learning atlas with Python standard library."""
from pathlib import Path
from html import escape
from diagrams import diagram
from content import PAGES, NAV, SOURCES, chapter
from glossary import TERMS
ROOT = Path(__file__).parent
SITE = 'AI & Agent Atlas'
REPO = 'ai-agent-atlas'
def pick(lang, en, zh): return zh if lang == 'zh' else en

def href(page, lang, anchor=''):
    return f'{page}{".zh" if lang == "zh" else ""}.html' + (f'#{anchor}' if anchor else '')

def cite(lang, *ids):
    return '<p class="references">' + pick(lang, 'Read the source: ', '对应资料：') + ' · '.join(f'<a href="{SOURCES[i][2]}" target="_blank" rel="noopener noreferrer">{SOURCES[i][1 if lang == "zh" else 0]} ↗</a>' for i in ids) + '</p>'

def para(*texts): return ''.join(f'<p>{t}</p>' for t in texts)

def table(headers, rows):
    return '<div class="table-wrap" tabindex="0"><table><thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'

def cards(items):
    return '<div class="cards">' + ''.join(f'<article class="card"><span class="eyebrow">{tag}</span><h3>{title}</h3><p>{text}</p></article>' for tag, title, text in items) + '</div>'

def callout(title, text): return f'<aside class="callout"><strong>{title}</strong><p>{text}</p></aside>'

def code(text): return '<pre><code>' + escape(text) + '</code></pre>'

def section(label, title, intro, content, ident):
    return f'<section class="chapter-section" id="{ident}"><span class="eyebrow">{label}</span><h2>{title}</h2><p class="lead">{intro}</p>{content}</section>'

def hero(lang, page, title, text, anchors=()):
    jumps = ''.join(f'<a href="#{ident}">{label}</a>' for ident, label in anchors)
    return f'<section class="page-intro"><div class="wrap"><span class="eyebrow">{NAV[lang][PAGES.index(page)]} / FIELD GUIDE</span><h1>{title}</h1><p>{text}</p><nav class="jump-links" aria-label="{pick(lang, "On this page", "本页目录")}">{jumps}</nav></div></section>'

def shell(lang, page, body):
    current = 'aria-current="page"'
    nav = ''.join(f'<a href="{href(p,lang)}" {current if p == page else ""}>{n}</a>' for p,n in zip(PAGES,NAV[lang]))
    langs = ''.join(f'<a data-atlas-lang="{l}" href="{href(page,l)}" {current if l == lang else ""}>{label}</a>' for l,label in [('en','EN'),('zh','中文')])
    title = SITE if page == 'index' else f'{NAV[lang][PAGES.index(page)]} · {SITE}'
    desc = pick(lang, 'Learn AI, LLMs, agents and harness engineering with ChatGPT, Codex, diagrams and local exercises.', '通过 ChatGPT、Codex、图解与本地练习学习 AI、LLM、Agent 及 Harness 工程。')
    scripts = '<script src="labs.js" defer></script>' if page == 'labs' else '<script src="glossary.js" defer></script>' if page == 'glossary' else ''
    prevnext = ''
    if page != 'index':
        idx=PAGES.index(page)
        prevnext = '<nav class="chapter-pager" aria-label="' + pick(lang,'Chapters','章节') + '">'
        prevnext += f'<a href="{href(PAGES[idx-1],lang)}">← {NAV[lang][idx-1]}</a>'
        if idx < len(PAGES)-1: prevnext += f'<a href="{href(PAGES[idx+1],lang)}">{NAV[lang][idx+1]} →</a>'
        prevnext += '</nav>'
    return f'''<!doctype html>
<html lang="{'zh-CN' if lang == 'zh' else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#182638"><meta name="description" content="{desc}"><title>{escape(title)} · ShundaZhang</title><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="style.css"><link rel="stylesheet" href="diagrams.css"><script src="language.js"></script>{scripts}</head>
<body><div class="topbar"><div class="wrap"><a href="https://shundazhang.github.io/">← {pick(lang,'Personal home','个人主页')}</a><nav class="languages" aria-label="{pick(lang,'Language selection','语言选择')}">{langs}</nav></div></div><a class="skip" href="#main">{pick(lang,'Skip to content','跳至正文')}</a><header><div class="wrap brand-row"><a class="brand" href="{href('index',lang)}"><span class="brand-mark">A/</span><span>{pick(lang,'AI / LLM / AGENT','AI 与 Agent')}<small>LEARNING ATLAS</small></span></a><a class="repo-link" href="https://github.com/ShundaZhang/{REPO}">GitHub ↗</a></div><nav class="chapter-nav wrap" aria-label="{pick(lang,'Main navigation','主导航')}">{nav}</nav></header><main id="main">{body}{'<div class="reading wrap">'+prevnext+'</div>' if prevnext else ''}</main><footer><div class="wrap"><div><strong>{pick(lang,SITE,'AI 与 Agent 知识地图')}</strong><p>{pick(lang,'Concepts, systems and verifiable practice','概念、系统与可核验实践')}</p></div><p>{pick(lang,'Reviewed 30 Sep 2026 · EN / 中文','复核于 2026 年 9 月 30 日 · EN / 中文')}</p></div></footer></body></html>'''

DESCRIPTIONS=[
('Fields, models, products and runtime layers','领域、模型、产品与运行时层次'),
('Tokens, embeddings, attention and next-token prediction','Token、嵌入、注意力与下一个 token 预测'),
('Pretraining, SFT, RLHF, DPO and LoRA','预训练、SFT、RLHF、DPO 与 LoRA'),
('Prefill, decoding, KV cache and reasoning budgets','Prefill、解码、KV cache 与推理预算'),
('Task contracts, examples and structured outputs','任务契约、示例及结构化输出'),
('Context windows, memory, retrieval and grounding','上下文窗口、记忆、检索及证据支持'),
('Actions, observations, planning and stopping','行动、观察、规划及停止'),
('Runtime contracts, state, recovery and architecture','运行时契约、状态、恢复及架构'),
('Tool schemas, MCP, skills and resource authorization','工具 schema、MCP、Skill 及资源授权'),
('Repository context, patches and verified changes','仓库上下文、补丁及可核验修改'),
('Study, source comparisons and reviewable artifacts','学习、来源比较及可审查产物'),
('Datasets, traces, graders and operational metrics','数据集、追踪、评分器及运行指标'),
('Injection, data boundaries, capabilities and effects','注入、数据边界、能力及实际效果'),
('Three projects and a reusable task notebook','三个项目及可复用任务笔记'),
('Context budgets, harness traces and eval tradeoffs','上下文预算、Harness 追踪及评估取舍'),
('40 searchable terms linked to their chapters','40 个可搜索术语及对应章节'),
('Papers, textbooks and current product documentation','论文、教材及当前产品文档'),
]

def overview(lang):
    t=lambda en,zh:pick(lang,en,zh)
    layers=[('01',t('MODEL','模型'),t('Learned parameters and conditional outputs','已有参数与条件输出')),('02',t('AGENT','智能体'),t('A goal pursued through actions and observations','通过行动及观察推进目标')),('03',t('HARNESS','运行时'),t('Context, execution, state and verification','上下文、执行、状态及验证')),('04',t('PRACTICE','实践'),t('ChatGPT, Codex and a local teaching runtime','ChatGPT、Codex 与本地教学运行时'))]
    graphic='<aside class="trust-map" aria-label="'+t('Four layers of the course','课程的四个层次')+'"><div class="map-label">THE SYSTEM AROUND THE MODEL</div>'+''.join(f'<div class="map-step"><span>{num}</span><div><strong>{title}</strong><small>{text}</small></div></div>' for num,title,text in layers)+'<div class="map-foot">'+t('One task → observable evidence of completion','一项任务 → 可观察的完成证据')+'</div></aside>'
    body='<section class="hero"><div class="wrap hero-grid"><div><span class="eyebrow">AI / LLM / AGENT / HARNESS</span><h1>'+t('Understand the model<br><em>Build the system</em>','理解模型<br><em>构建系统</em>')+'</h1><p>'+t('An independent learning map for engineers: from language-model mechanics to agents, runtime design and verifiable practice. Use ChatGPT to study and synthesize, Codex to work with code, and local exercises to inspect the machinery.','面向工程师的独立学习地图：从语言模型原理到 Agent、运行时设计及可核验实践。用 ChatGPT 学习与综合资料，用 Codex 处理代码，用本地练习观察运行机制。')+'</p><div class="hero-actions"><a class="button" href="'+href('concepts',lang)+'">'+t('Start with the concept map →','从概念地图开始 →')+'</a><a class="text-link" href="'+href('harness',lang)+'">'+t('Explore the Harness ↗','了解 Harness ↗')+'</a></div><div class="hero-meta">18 CHAPTERS / 14 DIAGRAMS / 3 LOCAL EXERCISES<br>'+t('ENGLISH & 中文 · CHATGPT + CODEX · PRIMARY SOURCES','中英双语 · ChatGPT + Codex · 一手资料')+'</div></div>'+graphic+'</div></section><div class="reading wrap">'
    route=[('01',t('See the whole stack','统览整个系统'),t('Concepts → LLM mechanics → Training → Inference. Explain which component changes when you add data, context or tools.','概念 → LLM 原理 → 训练 → 推理。能解释新增数据、上下文或工具时，改变的是哪个组件。')),('02',t('Use evidence well','学会使用证据'),t('Prompting → Context / RAG → ChatGPT. Produce a source-supported comparison, including a case where the evidence is missing.','提示 → 上下文 / RAG → ChatGPT。完成有出处的比较，并包含证据缺失时的行为。')),('03',t('Operate an agent','运行 Agent'),t('Agents → Harness → Tools / MCP → Codex. Reproduce a small code failure, patch it and inspect the verified result.','Agent → Harness → 工具 / MCP → Codex。复现小型代码失败、修改并检查核验结果。')),('04',t('Measure and improve','测量并改进'),t('Evaluation → Security → Practice / Labs. Read a trace, test a denied action and compare accepted results against cost.','评估 → 安全 → 实践 / 练习。阅读追踪、测试拒绝动作，并比较可接受结果与成本。'))]
    body+=section('01 / LEARNING ROUTE',t('Move from concepts to observable results','从概念走向可观察结果'),t('Assumed background: programming and basic systems knowledge. Linear algebra and probability help with the model chapters; no paid API is required for the local exercises.','预备知识：编程及基本系统知识；线性代数和概率有助于模型章节。本地练习无需付费 API。'),'<div class="sequence">'+''.join(f'<article><span>{n}</span><div><h3>{title}</h3><p>{text}</p></div></article>' for n,title,text in route)+'</div>','route')
    grid='<div class="topic-grid">'+''.join(f'<a class="topic-card" href="{href(page,lang)}"><span class="eyebrow">{i:02} / FIELD NOTES</span><h3>{NAV[lang][i]}</h3><p>{desc[1 if lang=="zh" else 0]}</p></a>' for i,(page,desc) in enumerate(zip(PAGES[1:],DESCRIPTIONS),1))+'</div>'
    body+=section('02 / CHAPTERS',t('Choose the layer you want to understand','选择你想理解的层次'),t('Read in sequence or enter at one practical question. These topics stand as an independent direction.','可以顺序阅读，也可从具体问题进入。本专题作为独立方向。'),grid,'chapters')
    body+=section('03 / START HERE',t('Four outputs worth keeping','值得保留的四个产出'),t('A learning site is most useful when it turns into your own experiments.','学习网站应帮助形成自己的实验。'),cards([('CHATGPT',t('A cited study note','有出处的学习笔记'),t('Explain one concept, attempt a question, and verify the correction against a source.','解释一个概念，尝试一道题，并按来源核验纠正。')),('CODEX',t('A reviewed code change','经过审查的代码修改'),t('State the failing property, inspect the diff, and keep the observed regression result.','明确失败属性、检查 diff、保存实际回归结果。')),('HARNESS',t('A trace you can explain','能逐步解释的追踪'),t('Download the scripted local runtime and identify what was proposed, authorized, executed and verified.','下载脚本化本地运行时，分清建议、授权、执行及验证。')),('EVAL',t('A repeatable acceptance set','可重复验收集'),t('Keep cases, denied actions and failure examples beside cost and latency measurements.','案例、拒绝动作及失败示例与成本 / 延迟一起保存。'))]),'outputs')
    body+=callout(t('Stable ideas, changing products','稳定概念与持续变化的产品'),t('Product guidance was checked on 30 Sep 2026. Availability, models and limits depend on your account and environment. The diagrams and deterministic labs are teaching models, not claims about private model internals.','产品指引复核于 2026 年 9 月 30 日。功能、模型及限制取决于账号和环境。图解及确定性练习是教学模型，不代表私有模型内部实现。'))
    return body+'</div>'

def chapter_page(page,lang):
    t=lambda en,zh:pick(lang,en,zh)
    rows=chapter(page,lang)
    idx=PAGES.index(page)
    body=hero(lang,page,NAV[lang][idx]+'<br><em>'+t('Concepts into practice','从概念到实践')+'</em>',DESCRIPTIONS[idx-1][1 if lang=='zh' else 0],[(r[0],r[1]) for r in rows])+'<div class="reading wrap">'
    for i,(ident,title,intro,content,refs,viz) in enumerate(rows,1):
        body+=section(f'{i:02} / FIELD NOTES',title,intro,(diagram(viz,lang) if viz else '')+content+(cite(lang,*refs) if refs else ''),ident)
    body+=callout(t('Check your understanding','检查理解'),t('Explain one distinction from this chapter using a concrete task. Identify the input, the component that acts, and the independent evidence you would use to check the result.','用一个具体任务解释本章的一项区别，指出输入、行动组件及独立核验结果的证据。'))
    return body+'</div>'

def labs(lang):
    t=lambda en,zh:pick(lang,en,zh)
    body=hero(lang,'labs',t('Inspect the runtime<br><em>See the tradeoffs</em>','观察运行时<br><em>看清工程取舍</em>'),t('Three deterministic local exercises use synthetic inputs. They call no model, send no requests and store no exercise data.','三项确定性本地练习使用示例输入，不调用模型、不发送请求、不保存练习数据。'),[('budget',t('Context','上下文')),('trace',t('Harness trace','Harness 追踪')),('eval',t('Evaluation','评估'))])+'<div class="reading wrap">'
    def select(ident,label,options):return '<label for="'+ident+'">'+label+'<select id="'+ident+'">'+''.join(f'<option value="{v}">{text}</option>' for v,text in options)+'</select></label>'
    def box(ident,controls,action,title):return f'<div class="lab-box" data-lab="{ident}"><div class="scenario-options">{controls}</div><div class="lab-actions"><button type="button" data-action="{action}">{title}</button></div><p class="lab-state" data-pass="info" id="{ident}-state" role="status" aria-live="polite">'+t('Ready — choose an input','就绪 — 选择输入')+f'</p><div class="lab-output" id="{ident}-output"></div><div class="lab-matrix" id="{ident}-details"></div></div>'
    body+='<noscript><aside class="callout">'+t('JavaScript enables these exercises. All chapter notes and downloads remain available without it.','练习需要 JavaScript；章节及下载内容仍可使用。')+'</aside></noscript>'
    controls=select('budget-limit',t('Context capacity · teaching units','上下文容量 · 教学单位'),[('6000','6,000'),('9000','9,000'),('12000','12,000')])+select('budget-strategy',t('Selection strategy','选择策略'),[('dump',t('Paste all documents','粘贴全部文档')),('select',t('Select current evidence','选择当前证据')),('summary',t('Use a summary without raw evidence','仅摘要，没有原始证据'))])
    body+=section('01 / CONTEXT',t('A fitting context can still lack evidence','放得下的上下文仍可能缺乏证据'),t('Task: compare the current protocol requirements. Reserve 1,000 units for instructions and 1,000 for the output.','任务：比较当前协议需求。为指令和输出各预留 1,000 单位。'),box('budget',controls,'budget-check',t('Inspect the context plan','检查上下文计划'))+para(t('Synthetic material: current source excerpt 3,000 units, stale draft 4,000, logs 5,000, summary 1,000. The summary omits the exact clause. Selection needs 5,000 units; all documents need 14,000. These are invented accounting units, not tokens, actual attention or billing estimates.','示例资料：当前原文 3,000 单位，过时草案 4,000，日志 5,000，摘要 1,000。摘要遗漏精确条款。选择方案共需 5,000，全部资料共需 14,000。这是虚构计量单位，不是 token、真实注意力或费用估计。'))+cite(lang,'middle'),'budget')
    controls=select('trace-scenario',t('Scripted proposal sequence','脚本化建议序列'),[('success',t('Read → compute → verified final','读取 → 计算 → 核验最终结果')),('wrong',t('Read → compute → wrong final','读取 → 计算 → 错误最终结果')),('denied',t('Read another tenant','读取其他租户')),('timeout',t('Read tool times out','读取工具超时')),('loop',t('Repeated reads without a final','反复读取，没有最终结果'))])+select('trace-limit',t('Maximum planner steps','最大规划步数'),[('2','2'),('4','4')])
    body+=section('02 / HARNESS',t('Proposal, execution and completion are distinct events','建议、执行与完成是不同事件'),t('Task: sum tenant A’s public training invoices [40, 60]. The only allowed read is tenant A; final completion requires a validated computation result of 100.','任务：求和租户 A 公开训练账单 [40, 60]。只允许读取 A；完成要求已验证的计算结果为 100。'),box('trace',controls,'trace-run',t('Run the scripted harness','运行脚本化 Harness'))+para(t('The fake planner emits a fixed sequence. Tools read only in-memory fixtures. Inspect the event order and whether verification occurs; an unexecuted or wrong final answer must not be marked complete. A timeout is simulated and the loop budget counts planner steps.','模拟规划器输出固定序列，工具只读取内存示例。检查事件顺序及是否发生验证；未执行或错误最终答案不能标记完成。超时是模拟的，循环预算按规划步数计数。'))+cite(lang,'running','function'),'trace')
    controls=select('eval-policy',t('Acceptance policy','验收策略'),[('quality',t('Quality threshold only','仅质量阈值')),('strict',t('Quality + no unauthorized effect','质量 + 无未获准效果'))])
    body+=section('03 / EVALUATION',t('Compare cost per accepted task','比较每项可接受任务成本'),t('Three invented candidates run the same six tasks, each once. Candidate C is blocked on one task; that case stays in the denominator.','三个虚构候选各运行相同六个任务一次。C 有一项阻塞，仍保留在分母中。'),box('eval',controls,'eval-run',t('Compare the synthetic candidates','比较示例候选'))+para(t('A task passes the quality threshold at score ≥ 0.8. Strict acceptance also requires no unauthorized effect. Costs use arbitrary units, and blocked attempts still incur their listed cost. This tiny fixed dataset demonstrates metric definitions, not comparative product performance.','任务分数 ≥ 0.8 满足质量阈值；严格验收还要求无未获准效果。成本为任意单位，阻塞尝试仍计入列出的成本。小型固定数据只演示指标定义，不代表产品性能比较。'))+cite(lang,'eval'),'eval')
    body+=section('04 / LOCAL CODE',t('Read and run a minimal teaching Harness','阅读并运行最小教学 Harness'),t('A Python standard-library example with a scripted planner, not an LLM or an SDK.','Python 标准库示例，使用脚本化规划器，不是 LLM 或 SDK。'),'<p class="download"><a href="labs/toy_harness.py" download>'+t('Download toy_harness.py ↓','下载 toy_harness.py ↓')+'</a> · <a href="labs/test_toy_harness.py" download>'+t('Download its checks ↓','下载检查文件 ↓')+'</a></p>'+code('python3 toy_harness.py success --max-steps 4\npython3 toy_harness.py denied\npython3 -m unittest -v test_toy_harness.py')+para(t('Save both files into the same disposable directory. The program reads synthetic fixtures from memory and prints JSON events. It has no network, file writes, subprocesses or credentials. Its validation is deliberately narrow for this task; it is not a production sandbox or a security library.','将两个文件放在同一可丢弃目录。程序读取内存示例并打印 JSON 事件，不使用网络、写文件、子进程或凭据。验证为此任务刻意限定，不是生产沙箱或安全库。')),'download')
    return body+'</div>'

def glossary(lang):
    t=lambda en,zh:pick(lang,en,zh)
    body=hero(lang,'glossary',t('Name the component<br><em>Find its boundary</em>','叫对组件名称<br><em>看清职责边界</em>'),t('Search 40 terms by name or explanation. Each term links to the chapter that develops it.','按名称或解释搜索 40 个术语，每项链接到进一步介绍的章节。'))+'<div class="reading wrap">'
    body+='<section class="chapter-section"><label class="lab-field" for="term-search">'+t('Search terms','搜索术语')+'<input type="search" id="term-search" placeholder="'+t('e.g. Harness, KV cache, memory','例如 Harness、KV cache、记忆')+'"></label><p id="term-count" role="status" aria-live="polite">'+t('40 terms','40 个术语')+'</p><div class="tool-grid">'
    for name,page,en,zh in TERMS:
        body+=f'<article class="tool-card term-card"><span class="eyebrow">{NAV[lang][PAGES.index(page)]}</span><h3>{name}</h3><p>{t(en,zh)}</p><a href="{href(page,lang)}">'+t('Read the chapter →','阅读对应章节 →')+'</a></article>'
    return body+'</div></section></div>'

def sources(lang):
    t=lambda en,zh:pick(lang,en,zh)
    body=hero(lang,'sources',t('Read the theory<br><em>Check the current interface</em>','阅读理论<br><em>核对当前接口</em>'),t('Primary papers, author-maintained textbooks and official product guides. Historical research and current documentation have different roles.','原始论文、作者维护的教材及官方产品指南。历史研究与当前文档承担不同职责。'))+'<div class="reading wrap">'
    groups=[('theory',t('Model theory and experiments','模型理论及实验'),['d2l','pytorch','transformer','scaling','chinchilla','rlhf','lora','dpo','flash','rag','middle','react','gaia']),('model',t('Model inputs, tools and outputs','模型输入、工具及输出'),['prompt','reasoning','embedding','retrieval','function','structured']),('runtime',t('Runtime, evaluation and security','运行时、评估及安全'),['runtimes','architecture','running','sandbox','sandbox-security','eval','trace','mcp','mcp-auth','aml','owasp']),('product',t('ChatGPT and Codex practice','ChatGPT 与 Codex 实践'),['quickstart','chat-prompt','projects','agents-md','skills','codex-mcp','app-server','codex-sandbox','long-task'])]
    for i,(ident,title,ids) in enumerate(groups,1):
        grid='<div class="source-grid">'+''.join(f'<a class="source-card" href="{SOURCES[k][2]}" target="_blank" rel="noopener noreferrer"><span class="eyebrow">{SOURCES[k][3]}</span><h3>{SOURCES[k][1 if lang=="zh" else 0]} ↗</h3></a>' for k in ids)+'</div>'
        body+=section(f'{i:02} / PRIMARY SOURCES',title,t('Use the chapter explanation as a reading map, then inspect the original source.','将章节作为导读，再检查原始来源。'),grid,ident)
    body+=callout(t('How to read the dates','怎样理解日期'),t('Paper dates identify historical experiments, not the internals of current commercial models. Living product pages can change after the review date. No external material is mirrored; all course explanations, diagrams and labs are original.','论文日期代表历史实验，不代表当前商业模型内部实现。动态产品文档可在复核日后更新。本站不镜像外部资料，课程解释、图解及练习为原创。'))
    return body+'</div>'

if __name__=='__main__':
    for lang in ('en','zh'):
        for page in PAGES:
            body=overview(lang) if page=='index' else labs(lang) if page=='labs' else glossary(lang) if page=='glossary' else sources(lang) if page=='sources' else chapter_page(page,lang)
            (ROOT/href(page,lang)).write_text(shell(lang,page,body),encoding='utf-8')
    print(f'Built {2*len(PAGES)} pages, {len(TERMS)} terms, {len(SOURCES)} sources')
