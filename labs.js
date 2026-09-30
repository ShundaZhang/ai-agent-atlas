(() => {
  'use strict';
  const zh = document.documentElement.lang.startsWith('zh');
  const t = (en, cn) => zh ? cn : en;
  const el = id => document.getElementById(id);
  const state = (lab, text, pass = 'info') => {
    el(`${lab}-state`).textContent = text;
    el(`${lab}-state`).dataset.pass = String(pass);
  };
  const output = (lab, text) => { el(`${lab}-output`).textContent = text; };
  const table = (lab, headers, rows) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-wrap'; wrapper.tabIndex = 0;
    const tab = document.createElement('table');
    const head = document.createElement('thead'), tr = document.createElement('tr');
    headers.forEach(text => { const th = document.createElement('th'); th.scope = 'col'; th.textContent = text; tr.append(th); });
    head.append(tr); tab.append(head);
    const body = document.createElement('tbody');
    rows.forEach(row => { const line = document.createElement('tr'); row.forEach(text => { const td = document.createElement('td'); td.textContent = String(text); line.append(td); }); body.append(line); });
    tab.append(body); wrapper.append(tab); el(`${lab}-details`).replaceChildren(wrapper);
  };
  const budget = () => {
    const limit = Number(el('budget-limit').value), strategy = el('budget-strategy').value;
    const selected = strategy === 'dump' ? [[t('Current excerpt','当前原文'),3000],[t('Stale draft','过时草案'),4000],[t('Logs','日志'),5000]]
      : strategy === 'select' ? [[t('Current excerpt','当前原文'),3000]] : [[t('Summary without exact clause','缺少精确条款的摘要'),1000]];
    const rows = [[t('Instructions','指令'),1000],...selected,[t('Output reserve','输出预留'),1000]];
    const used = rows.reduce((a,r)=>a+r[1],0), fit = used <= limit, evidence = strategy !== 'summary';
    state('budget', !fit ? t('Capacity exceeded — choose relevant evidence','容量超限 — 应选择相关证据') : !evidence ? t('Fits, but the exact evidence is missing','放得下，但缺少精确证据') : t('Fits with the current source excerpt','放得下，且包含当前原文'), fit && evidence);
    output('budget',`${t('Required','所需')}: ${used.toLocaleString()} / ${limit.toLocaleString()} ${t('teaching units','教学单位')}\n${t('Remaining','剩余')}: ${(limit-used).toLocaleString()}\n${t('Capacity','容量')}: ${fit?'PASS':'FAIL'}\n${t('Current clause present','包含当前条款')}: ${evidence?'YES':'NO'}\n${t('Passing this plan does not guarantee a correct generated answer.','计划通过不保证生成回答正确。')}`);
    table('budget',[t('Item','项目'),t('Units','单位')],rows);
  };
  const trace = () => {
    const scenario=el('trace-scenario').value,limit=Number(el('trace-limit').value);
    const read={kind:'tool',name:'read_invoices',args:{tenant:'A'}};
    const script=scenario==='denied'?[{kind:'tool',name:'read_invoices',args:{tenant:'B'}}]
      :scenario==='loop'?Array.from({length:8},()=>read)
      :[read,{kind:'tool',name:'sum_values',args:{values:[40,60]}},{kind:'final',value:scenario==='wrong'?99:100}];
    let observed=null,computed=null,stop='planner_exhausted';
    const events=[];
    const event=(step,phase,en,cn)=>events.push([step,phase,t(en,cn)]);
    for(let i=0;i<script.length;i++){
      const step=i+1,call=script[i];
      if(step>limit){stop='step_budget';event(limit,'STOP','No new proposal or tool after the step limit','步数限制后不提出新建议、不执行新工具');break;}
      event(step,'PROPOSE',JSON.stringify(call),JSON.stringify(call));
      if(call.kind==='final'){
        event(step,'VERIFY',`candidate=${call.value}; computed=${computed}`,`候选=${call.value}；已计算=${computed}`);
        stop=computed!==null&&call.value===computed&&computed===100?'completed':'verification_failed';
        event(step,'STOP',stop,stop);break;
      }
      event(step,'VALIDATE','Scripted call matches its fixed schema','脚本化调用符合固定 schema');
      if(call.name==='read_invoices'){
        if(call.args.tenant!=='A'){event(step,'AUTHORIZE','DENY: tenant A task only','拒绝：任务仅限租户 A');stop='policy_denied';event(step,'STOP','No tool executed, no foreign data returned','未执行工具，未返回其他租户数据');break;}
        event(step,'AUTHORIZE','ALLOW: tenant A read','允许：读取租户 A');event(step,'EXECUTE','read_invoices','read_invoices');
        if(scenario==='timeout'){event(step,'OBSERVE','simulated_timeout','模拟超时');stop='tool_timeout';event(step,'STOP','No result; no automatic retry','无结果，不自动重试');break;}
        observed=[40,60];event(step,'OBSERVE',JSON.stringify({values:observed}),JSON.stringify({values:observed}));
      }else{
        if(!observed||JSON.stringify(call.args.values)!==JSON.stringify(observed)){stop='policy_denied';break;}
        event(step,'AUTHORIZE','ALLOW: sum observed fixture','允许：求和已观察示例');event(step,'EXECUTE','sum_values','sum_values');
        computed=observed.reduce((a,b)=>a+b,0);event(step,'OBSERVE',JSON.stringify({total:computed}),JSON.stringify({total:computed}));
      }
    }
    const explanations={completed:t('Verified final with actual simulated computation evidence','最终结果与实际模拟计算证据一致'),verification_failed:t('Wrong or unsupported final is not completion','错误或无依据最终答案不算完成'),policy_denied:t('Denied before accessing the foreign resource','访问其他资源前拒绝'),tool_timeout:t('Stopped on a simulated tool timeout','模拟工具超时后停止'),step_budget:t('Stopped at the configured planner-step budget','在配置规划步数上限停止')};
    state('trace',`${stop} · ${explanations[stop]||stop}`,stop==='completed');
    output('trace',`${t('Observed fixture','已观察示例')}: ${observed?JSON.stringify(observed):t('none','无')}\n${t('Computed result','已计算结果')}: ${computed===null?t('none','无'):computed}\n${t('This is a scripted runtime trace, not a model reasoning trace.','这是脚本化运行时追踪，不是模型推理追踪。')}`);
    table('trace',[t('Step','步骤'),t('Event','事件'),t('Observed detail','观察详情')],events);
  };
  const candidates=[
    {name:'A',scores:[.9,.9,.5,.8,.85,.6],violations:[false,false,false,false,false,false],costs:[1,1,1,1,1,1],blocked:[]},
    {name:'B',scores:[.9,.92,.88,.95,.9,.6],violations:[false,false,true,false,false,false],costs:[2,2,2,2,2,2],blocked:[]},
    {name:'C',scores:[.9,.9,.85,.9,.5,0],violations:[false,false,false,false,false,false],costs:[3,3,3,3,3,1],blocked:[5]}
  ];
  const evaluation=()=>{
    const strict=el('eval-policy').value==='strict';
    const metrics=candidates.map(c=>{
      const accepted=c.scores.map((s,i)=>s>=.8&&!c.blocked.includes(i)&&(!strict||!c.violations[i]));
      const count=accepted.filter(Boolean).length,cost=c.costs.reduce((a,b)=>a+b,0);
      return {c,count,cost,per:count?cost/count:Infinity,accepted};
    });
    table('eval',[t('Candidate','候选'),t('Accepted / attempts','可接受 / 尝试'),t('Unauthorized effects','未获准效果'),t('Blocked','阻塞'),t('Total cost','总成本'),t('Cost / accepted','每项可接受成本')],metrics.map(m=>[m.c.name,`${m.count} / 6`,m.c.violations.filter(Boolean).length,m.c.blocked.length,m.cost,m.per.toFixed(2)]));
    const best=metrics.reduce((a,b)=>a.per<=b.per?a:b);
    state('eval',t(`Lowest cost per accepted task: ${best.c.name} · ${best.per.toFixed(2)} units`,`每项可接受任务成本最低：${best.c.name} · ${best.per.toFixed(2)} 单位`),strict);
    output('eval',t('All 6 cases remain in each denominator, including blocked and low-quality cases.\n','每个分母保留全部 6 项，包括阻塞和低质量案例。\n')+(strict?t('B: 5 quality passes → 4 accepted tasks after the policy check.','B：质量通过 5 项 → 策略检查后可接受 4 项。'):t('B: 5 quality passes include 1 unauthorized effect. Quality-only acceptance hides that violation.','B：质量通过 5 项包含 1 项未获准效果，仅质量验收掩盖此违反。'))+'\n'+t('Synthetic single-run data: no uncertainty or real product ranking can be inferred.','单次示例数据：不能推断不确定性或真实产品排名。'));
  };
  const actions={'budget-check':budget,'trace-run':trace,'eval-run':evaluation};
  document.addEventListener('click',event=>{const action=event.target.closest('[data-action]')?.dataset.action;if(actions[action])actions[action]();});
  document.querySelectorAll('.lab-box select').forEach(select=>select.addEventListener('change',()=>{
    const lab=select.closest('.lab-box').dataset.lab;
    state(lab,t('Selection changed — run again','选择已更改 — 请重新运行'));
    output(lab,'');el(`${lab}-details`).replaceChildren();
  }));
})();
