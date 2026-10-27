# 050负责人验收及051纠正版立项

2026-10-27（北京时间）｜ChatGPT研究负责人  
执行提交：[987aa3a](https://github.com/floomeer83felix-source/vlm/commit/987aa3a1dbaccc3bfc3672d6b622a0b15bac7138)。  
**ACCEPTED_BOUNDED_INPUT_FAILURE_REPORT / SCIENTIFIC_NOT_RUN / 050_CLOSED。**

## 1. 本次实际发生了什么

接收050的有界输入失败回执，关闭本父。新模型调用0，120个F48/P0–P3格全部NOT_RUN，V4也未形成。输入规范化在第一条到达canonical_question的原记录上以MISSING_OR_CONFLICTING_OPTIONS结束；没有完成24题的字段join。不能据此写全帧/投票无收益，也不能评H_F/H_V通过或失败。

原文件1,854,695B及冻结SHA一致，仅说明同字节入口。nongold投影一次物理打开混合JSON，gold值解码0；数组payload、processor、模型/GPU查询、标签评分均0。旧049自然结果没有在本轮重绑定或重评分；此前描述性结果保留，但其严格选项字段绑定仍待核。

## 2. 公开复核

刷新main及AGENTS/看板/results/总览/合同/两个原始报告，读取两源码、48行CSV和JSON。987aa3a的父为5fa1059，恰7处allowlist；results旧前缀逐字保留，仅追加一个050父记录。两源码SHA与收据一致，AST可解析：

- coverage_aggregation_050.py：9ca4602331cde45869906cc7bcc4114d5e4c2cc53d6c065aa30414880f87d253。
- test_coverage_aggregation_050.py：c1de8f4c233f76337d0b3893c98237dc2a4cfef621fb8ac0ae9c789f0b3b018b。

独立标准库核48行CSV：20行新模型来源×条件，每行N6且NOT_RUN6，总120；4行V4总24个未形成投票；旧基线和O4/O5行均UNKNOWN，所有correct留空。JSON的模型/processor/评分0计数、null效果/门槛、四源分母、成本/退出与CSV一致，不能把空值填0。

四个Job均实际active0且无kill：bind0.453s/exit1，初suite1.281s/exit1，回归0.172s/exit0，verify0.125s/exit0，总2.031s。峰commit17,506,304B，根17文件/7708B、父报告时1425.917s，在合同限内。初suite成本检查缺math导入、修复后16/16例36断言、独立23断言是执行者报告；负责人未在Windows重跑它们。实际原schema、私有退出/读取计数和原标签未由负责人独立重演，公开推理/评分路径本轮未运行，不认证已可用。

## 3. 找到的公开契约缺口

050只请求question/options/A–E，并只接受options列表/字典或A–E顶层键。当前公开作者数据卡的[Annotation Format](https://huggingface.co/datasets/HourVideo/HourVideo/blob/main/README.md)却列出mcq_test及answer_1…answer_5，并明确建议基于mcq_test评测。作者代码提供了更直接依据：

[hv_utils.py，固定提交1ac83c260c315545c571f78dea5bf913f36595a5](https://github.com/keshik6/HourVideo/blob/1ac83c260c315545c571f78dea5bf913f36595a5/hourvideo/hv_utils.py#L303)，blob0b243332edddb518f0db7ee06921817cf8c5a605，在question后拼接mcq_test形成测试题。官方GPT/Gemini入口使用该构造结果。这里只读取公开说明/代码，没有下载原数据或调用官方付费模型。

**负责人在050合同中漏列了官方展示格式，这是可避免的契约错误。** 执行者按原合同停机是正确行为。公开证据足以支持定向修正；但还不足以证明私有24题全部确实采用该字段，或第一条究竟是缺失旧字段还是多个旧字段冲突。051必须先实际核齐，不能从报错推造原schema。

## 4. 已完成的纠正及其边界

已实现[纯标准库mcq_test解析/绑定器](../../prototypes/hourvideo_mcq_schema_051.py)及[16个自有夹具测试](../../prototypes/test_hourvideo_mcq_schema_051.py)，负责人在当前CPU工作区实际运行全部通过。无任何HourVideo题/答案/私有路径或模型输入。

它从官方mcq_test显示的A–E标签提取有序选项，并与049冻结问题/五选项逐项比对。仅处理声明的显示标签、行结束符和首尾结构空白；不改大小写、标点、内部空白或顺序。返回给模型的仍是原冻结文本。无mcq_test、标签缺失/重复/错序、选项互换或正文改动均拒绝；不回填旧nongold，也不让answer_1…5覆盖展示标签。protected gold对象哨兵测试确认绑定函数不访问它。

这是格式实现验证，**不是私有字段join已通过**。051把实际24题核对、CPU原生输入、模型比较与评分放入同一完整父包，全部核对在权重前完成；不存在单独“再做一个schema检查任务”的安排。

## 5. 下一任务

下达[051完整纠正版](../codex-artifacts/VLM-COVERAGE-AGGREGATION-051/README.md)，为当前唯一READY，等待其明确本地启动。复用同四源48帧/同24题、F48/P0–P3/V4、模型/提示/帧规格、旧SO主参照与门槛，均不因本次失败改变。新generate≤120、GPU≤1200s；050未用额度不结转，051是新授权的一次完整执行，不重启050/049。

模型前原文件仅投影同24题question/mcq_test，词法跳过gold；模型实际退出后独立scorer再按同一展示绑定读24个原标签，重算旧自然输出并与049正确性表逐题对齐。发现不一致则报告UNKNOWN并由负责人另行追加更正，不覆盖旧记录。

当前可用研究资产与方法效果保持未知/既有状态；科学上既不能判全帧有效，也不能判无效，NOVELTY=RETAIN0。负责人本轮没有读取私有原标注、运行本地模型或扩大数据范围。
