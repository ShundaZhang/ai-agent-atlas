# -*- coding: utf-8 -*-
"""Original teaching diagrams rendered as semantic HTML."""
from diagram_core import node, arrow, flow, frame, sequence
from content import SOURCES

def diagram(ident,lang):
    t=lambda en,zh: zh if lang=='zh' else en
    def n(en,zh,detail_en,detail_zh,tone='neutral'):return node(t(en,zh),t(detail_en,detail_zh),tone)
    def f(items):return flow([item for i,part in enumerate(items) for item in ((arrow(),part) if i else (part,))])
    title=caption=body=source=''
    if ident=='layers':
        title=t('One task, several different layers','一项任务，多个不同层次'); source='architecture'
        body='<div class="viz-path-list">'+n('User / application','用户 / 应用','Goal, acceptance and configured authority','目标、验收与已配置权限','protected')+arrow(direction='down')+n('Harness','Harness 运行时','State, context, routing, validation and stopping','状态、上下文、路由、验证及停止','protected')+arrow(direction='down')+'<div class="viz-two">'+n('Model','模型','Produces a response or proposed tool call','生成回答或建议工具调用')+n('Tools / environment','工具 / 环境','Return observed results and actual artifacts','返回观察结果及实际产物')+'</div></div>'
        caption=t('Conceptual composition, not an exact product implementation. The model and execution environment are distinct components.','概念组成图，不是某产品精确实现。模型与执行环境是不同组件。')
    elif ident=='decoder':
        title=t('A decoder-style generation step','Decoder 风格的一步生成');source='transformer'
        body=f([n('Prefix tokens','前缀 token','IDs → embeddings + positions','ID → 嵌入 + 位置'),n('Decoder blocks','Decoder 层','Causal attention + feed-forward transformations','因果注意力 + 前馈变换'),n('Logits → selection','Logits → 选择','Distribution over candidate next tokens','候选下一个 token 分布'),n('Append token','追加 token','Repeat with the updated prefix','更新前缀后继续')])
        caption=t('Teaching adaptation for autoregressive decoding. Causal masking restricts access to future positions; original Transformer architecture also has an encoder.','面向自回归解码的教学改编。因果掩码限制未来位置；原 Transformer 架构还包含 encoder。')
    elif ident=='training':
        title=t('Learning parameters is different from supplying context','学习参数与提供上下文不同');source='rlhf'
        body=f([n('Pretraining','预训练','Broad data and prediction objectives','广泛数据及预测目标'),n('Post-training','后训练','Demonstrations, preferences or rewards','示范、偏好或奖励'),n('Learned checkpoint','已训练版本','Parameters used during inference','推理使用的参数','protected')])+'<div class="viz-two">'+n('Inference input','推理输入','Task + documents + observations','任务 + 文档 + 观察')+n('Generated output','生成输出','Behavior conditioned on current inputs','受当前输入影响的行为')+'</div>'
        caption=t('An illustrative family of training stages. Changing a document in context does not by itself update model weights.','训练阶段的方法族示意。改变上下文文档本身不更新模型权重。')
    elif ident=='inference':
        title=t('Two execution phases and one reusable cache','两个执行阶段与一项可重用缓存');source='flash'
        body=f([n('Prefill','Prefill','Process the input prefix','处理输入前缀'),n('KV cache','KV cache','Retain earlier attention keys and values','保存此前注意力的 key / value','protected'),n('Decode','Decode','Compute / select the next token','计算 / 选择下一个 token'),n('Repeat','重复','Extend sequence and cache','扩展序列及缓存')])
        caption=t('A conceptual execution sketch. The KV cache supports sequence computation; it is not project memory. FlashAttention addresses attention IO rather than application memory.','执行概念示意。KV cache 支持序列计算，不是项目记忆；FlashAttention 关注注意力 IO，而非应用记忆。')
    elif ident=='prompt-contract':
        title=t('From a task request to a checkable result','从任务请求到可核验结果');source='chat-prompt'
        body='<div class="viz-two">'+n('Task specification','任务规格','Goal + evidence + output + constraints','目标 + 证据 + 输出 + 约束')+n('Acceptance condition','验收条件','What must an independent check observe?','独立检查应观察到什么？','protected')+'</div>'+arrow(direction='down')+f([n('Model / workflow','模型 / 工作流','Generate or act within the configured scope','在配置范围内生成或行动'),n('Candidate result','候选结果','Text, a structured object or an artifact','文本、结构化对象或产物'),n('Validator','验证器','Check source support and task properties','检查出处及任务属性','protected')])
        caption=t('Original task-contract example. A schema validates structure; independent checks validate the property the task requires.','原创任务契约示意。Schema 验证结构，独立检查验证任务要求的属性。')
    elif ident=='context':
        title=t('Several stores feed a bounded context','多种存储进入有限上下文');source='middle'
        body='<div class="viz-three">'+n('Instructions','指令','Goal and stable constraints','目标及稳定约束','protected')+n('Evidence / memory','证据 / 记忆','Selected records with provenance','带来源的所选记录')+n('Workspace / tools','工作区 / 工具','Current files and observations','当前文件及观察')+'</div>'+arrow(direction='down')+n('Context assembly','上下文组装','Select, budget and preserve authority distinctions','选择、预算并保留权限区别','protected')+arrow(direction='down')+n('Model input','模型输入','Useful evidence may still be omitted or misunderstood','有用证据仍可能遗漏或被误解')
        caption=t('Long-context research motivates measurement, not a claim about all current models. A longer window is not a substitute for source selection.','长上下文研究提示应实际测量，不代表所有当前模型的行为。更长窗口不能替代来源选择。')
    elif ident=='rag':
        title=t('Retrieve evidence before generating an answer','先检索证据，再生成回答');source='rag'
        body=f([n('Source corpus','来源语料','Versions, ownership and permissions','版本、所有权及权限'),n('Query + retrieval','查询 + 检索','Keyword / vector / hybrid candidates','关键词 / 向量 / 混合候选'),n('Access + selection','授权 + 选择','Filter, rerank and preserve source locations','过滤、重排及保留出处','protected'),n('Grounded answer','有依据的回答','Check the claims against the passages','按原段落核对主张')])
        caption=t('Engineering extension of the RAG idea. Authorization and grounding are separate checks, and neither is guaranteed by similarity search.','RAG 思路的工程扩展。授权与证据支持是不同检查，相似度搜索不保证二者。')
    elif ident=='agent-loop':
        title=t('A proposed action must survive real feedback','建议动作需要接受实际反馈');source='react'
        body=f([n('Observe','观察','Goal + partial environment state','目标 + 局部环境状态'),n('Propose','建议','Model or planner chooses a next step','模型或规划器选择下一步'),n('Gate / act','检查 / 行动','Runtime checks policy and executes','运行时检查策略并执行','protected'),n('Check / continue','检查 / 继续','Result → revised plan or stop','结果 → 调整计划或停止')])
        caption=t('Conceptual interaction loop. Tool observations are feedback, not automatic authority. Each cycle needs a completion or bounded-stop decision.','概念交互循环。工具观察是反馈，不自动产生权限。每轮需要完成或有限停止决策。')
    elif ident=='harness-boundary':
        title=t('Keep control separate from scoped compute','将控制与限定计算分开');source='sandbox'
        body='<div class="viz-two"><div class="viz-zone">'+node(t('TRUSTED CONTROL','可信控制'),'','protected')+n('Harness + application','Harness + 应用','User identity, task capability, durable state, audit and policy','用户身份、任务能力、持久状态、审计及策略','protected')+'</div><div class="viz-zone">'+node(t('EXECUTION ENVIRONMENT','执行环境'),'','outside')+n('Sandbox tools','沙箱工具','Scoped files, commands and limited external access','限定文件、命令及外部访问','outside')+'</div></div>'+arrow(t('Validated call → observed result','验证后调用 → 观察结果'))+n('Model calls','模型调用','Input assembly and proposals are mediated by the runtime','输入组装及建议由运行时协调')
        caption=t('A recommended separation of responsibilities, not a guarantee supplied by a container. Tools still require application authorization.','建议的职责划分，不是容器自动提供的保证。工具仍需要应用授权。')
    elif ident=='tool-sequence':
        title=t('One tool round trip','一轮工具调用');source='function'
        body=sequence(lang,[(t('Application / Harness','应用 / Harness'),t('Policy and execution','策略及执行'),'protected'),(t('Model','模型'),t('Proposes a call','建议调用'),'neutral'),(t('Tool','工具'),t('Real operation','真实操作'),'outside')],[(0,1,t('Task + tool schemas','任务 + 工具 schema')),(1,0,t('Call proposal with arguments','带参数的调用建议')),(0,0,t('Validate + authorize','验证 + 授权')),(0,2,t('Execute an allowed call','执行获准调用')),(2,0,t('Observed result or typed error','观察结果或类型化错误')),(0,1,t('Supply result, then continue or finish','提供结果，继续或完成'))])
        caption=t('The application, not a generated success sentence, determines whether an operation executed.','是否执行由应用确认，而非由生成的成功句确认。')
    elif ident=='codex-loop':
        title=t('A small code change with visible evidence','有可见证据的小代码修改');source='long-task'
        body=f([n('Inspect / reproduce','检查 / 复现','Repository and failing behavior','仓库及失败行为'),n('Patch','修改','Change the responsible behavior','修改负责的行为'),n('Run checks','运行检查','Relevant regression and normal behavior','相关回归及正常行为','protected'),n('Review','审查','Diff + actual result + limits','Diff + 实际结果 + 限制')])
        caption=t('Teaching workflow for a bounded patch. Repair failures based on observed feedback; a clean test result supports only its tested scope.','有界补丁教学流程。根据观察反馈修复失败；通过检查只支持被测范围。')
    elif ident=='chat-workflow':
        title=t('Use the learner’s attempt as feedback','用学习者的尝试形成反馈');source='chat-prompt'
        body=f([n('Source + question','来源 + 问题','Name assumptions and the topic','明确假设及主题'),n('Explanation','解释','One diagram and one small case','一张图及一个小案例'),n('Your attempt','自己尝试','Answer before reading the correction','先作答，再阅读纠正','protected'),n('Check + note','核对 + 笔记','Compare with authoritative evidence','与权威证据对照')])
        caption=t('Original study workflow that works with an ordinary conversation. It is not tied to account availability of a named feature.','普通对话即可使用的原创学习流程，不依赖特定功能的账号可用性。')
    elif ident=='evaluation':
        title=t('Separate outcomes, traces and aggregate metrics','区分结果、追踪及汇总指标');source='trace'
        body=f([n('Fixed task set','固定任务集','Inputs, expected effects and constraints','输入、预期效果及约束'),n('Candidate runs','候选运行','Same conditions, repeated where needed','相同条件，必要时重复'),n('Independent grading','独立评分','Assertions, evidence rubric and effect log','断言、证据准则及效果日志','protected'),n('Comparison','比较','Success, risk, latency and cost','成功、风险、延迟及成本')])
        caption=t('A trace explains the observed path; an outcome check assesses completion. Averages must not erase hard policy failures.','追踪解释观察到的路径，结果检查评估完成情况。平均值不能掩盖硬策略失败。')
    elif ident=='security':
        title=t('Do not let retrieved text expand a task’s authority','不让检索文本扩大任务权限');source='owasp'
        body=f([n('Outside document','外部文档','Evidence + possibly unwanted instructions','证据 + 可能存在的非预期指令','outside'),n('Generated proposal','生成建议','May request a tool action','可能请求工具动作'),n('Runtime policy','运行时策略','User + task + resource + action','用户 + 任务 + 资源 + 动作','protected'),n('Resource boundary','资源边界','Execute allowed calls; reject the rest','执行获准调用，拒绝其余','protected')])
        caption=t('Original authority-path illustration. Restrict actual tool effects even when model behavior is uncertain.','原创权限路径示意。即使模型行为不确定，也应限制实际工具效果。')
    else: raise ValueError(ident)
    src=SOURCES[source]
    return frame(lang,'viz-'+ident,title,body,caption,src[2],src[1 if lang=='zh' else 0])
