# 期刊公开审阅稿Word/PDF生成：唯一受控出版交付，不是086科研实验

2026-11-04｜ChatGPT负责人制定。用户本轮明确要求从投稿格式、科学复现论证、独立验证三方面完善稿件。本合同仅对前两方面**已经写入main的公开论文文本**生成新的审阅版Word/PDF并逐页校验；第三方面新数据/模型实验仅有预注册计划，`NOT_RUN / NOT_AUTHORIZED`。

**父任务ID：VLM-JOURNAL-PUBLIC-RENDER-2026-11-04；唯一READY；PUBLIC_DOCS_ONLY / NO_GPU / NO_PRIVATE_DATA / NO_MODEL / NO_NEW_EXPERIMENT。**

## 1. 安全启动

1. 在用户当前Codex聊天接收**一条用户新消息**，在独立公共Github文档checkout按AGENTS安全同步main。清洁工作区才fast-forward；不得reset/rebase/force push。重新读取`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本合同及最新科学总览，确认只有本父READY且results尚未有本父记录；否则STOP。
2. 唯一允许的输入只在公共仓库：
   - `docs/papers/frozen-role-order-study/revision-2026-11-03/manuscript-submission-review-2026-11-04.md`
   - 该目录已有`figures/paired-seeds.png`、`figures/conditional-intervals.png`
   - 公开原稿`manuscript.docx`（仅当作pandoc样式参照，不承继内容）及公开校验稿`tables.json`。
   - `submission-audit-2026-11-04.md`、`independent-validation-preregistration-2026-11-04.md`与脚本`build_submission_review_2026_11_04.py`。
3. 严禁打开Windows实验私有工作区、模型、媒体、标签、特征或答案，严禁网络下载、训练、推理、GPU、驱动调查和自动投稿。仅允许Github公共文档同步/普通push。若本机没有已装pandoc/python-docx/LibreOffice或缺图，安全标`BLOCKED_TOOLING`；不能临时下载安装或查询私有目录。

## 2. 建造和科学内容硬闸

1. 首先完全公开只读核对：新稿标题中文≤20汉字、摘要200–300字、英文≥100词、[1]–[11]正式文献顺序和正文引号内引用，图1/图2，表1/表2；与公开原`tables.json`的5划分、六seed数组和现有条件区间的数值完全一致。**不用新的bootstrap，也不从原CSV之外扩展/重算科学结果**。负向验证−1.52pp、项目门FAIL、来源非独立、Qwen模型冻结、旧085 DATA_GATE HOLD必须保持其现有论证边界。源有矛盾直接`BLOCKED_SCIENTIFIC_MISMATCH`，**不后改数字**。
2. 用已提交`build_submission_review_2026_11_04.py --public-review-only`生成新版可编辑`docx`及`pdf`。这是**审阅版**，不是已按目标期刊官方模板精确套版，也不是匿名审稿证实的最终文件。
3. 验证Word中**两张可编辑表格**、图1/图2可见、数学公式保留为原生Word数学对象（如因pandoc版本不支持，明确记录限制，不能替成截图声称完整）、11条正式参考文献、实际图表分母和摘要中文/英文一致。无意的原旧参考文献/段落不得残留。
4. 将Word/PDF转成逐页图像，每一页目视检查文字重叠、越界、CJK缺字、表格截断、参考文献丢失、分栏错位；注意摘要和两图两表。若布局不达标，可最多一次**仅格式实现**修复公开builder，保留首次失败证据与修复说明；不可改正文科学结果、模型/数据、种子或文献内容。无法达标就BLOCKED而不是虚报完成。
5. 保持原`manuscript.docx`/`manuscript.pdf`及`manuscript.md`原2026-11-03版本不动；新版输出以`manuscript-submission-review-2026-11-04`前缀区分。原书稿是9页旧稿，不得写成新版本页数。

## 3. 资源、交付及停线

- 本父总wall≤3600s、科学CPU≤300s、RAM≤4GiB、工具调用本轮一次；禁止GPU。每步真实耗时/文件大小/执行版本公开记录；系统无法完全计量的宿主资源标UNKNOWN，不伪造硬保证。
- 允许提交**四处新增**：①`docs/papers/frozen-role-order-study/revision-2026-11-03/manuscript-submission-review-2026-11-04.docx`、②同名`.pdf`、③`docs/papers/frozen-role-order-study/revision-2026-11-03/build-submission-review-receipt.json`、④`docs/codex-artifacts/VLM-JOURNAL-PUBLIC-RENDER-2026-11-04/render-audit.md`，加⑤`docs/codex-results.md`唯一完整父项append。最多⑥原公开`build_submission_review_2026_11_04.py`在一次代码兼容修复时修改；不得更改AGENTS、规划文档、原旧论文或其他历史输入。输出文件总体预算≤8MiB。
- 若论文没有足够的严格独立验证，第三档状态必须继续`NOT_RUN`。禁止在新版摘要/讨论中新增“独立基准已证明”“接受率提高至50%”之类声称。期刊真实作者/单位/通讯/基金/分类号仍待作者填写，不能伪造。
- 只在上述白名单暂存`git diff --cached --name-only`，一次普通push main，随后STOP，**不自动延伸新的科研任务、外部提交或任何独立媒体实验**。失败也在允许的`render-audit.md`＋results一次append如实报告，Word/PDF未产生不可伪造链接。
