# VLM-BATCH-005：研究可行性决策任务包

**唯一可执行条件**：只有当 `docs/next-steps.md` 标记 VLM-BATCH-005 为 READY 时才能执行。保留原 Codex 聊天框。完成整个任务包后停止，等待 ChatGPT 审查，不自动推进 GPU 或下一个任务。

## 输入与科学边界

读取 main 最新 `AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`；参考 VLM-002、VLM-BATCH-003、VLM-BATCH-004 三批已经上传的审计和 toy 结果。若已有 VLM-BATCH-005 回报，停止，避免重复。

G1 仍 HOLD：VES-Bench 的许可、实际必要证据区间、真实媒体版本和 PTS；三候选的至少40个保守独立来源、12帧配对条件、真实视觉 token 预算均未证实。本任务不得以公开文件存在、toy 测试通过、论文描述代替真实数据核验。

## A：公开数据访问渠道核查

输出 `docs/codex-artifacts/VLM-BATCH-005/official-access-route.md`。优先仅查看 TRACE/VES-Bench 的官方项目页、仓库说明及公开数据访问说明；限制为最多6项小型官方页面，总计不超过1MiB。记录可验证的官方咨询/数据访问渠道链接、许可文本是否明确、版本信息，注明引用URL和日期。没有官方路径就记 UNKNOWN 并停止搜索。不得发送邮件、GitHub Issue、申请表或外部联系消息，不请求下载视频、答案和完整标注；不要猜测个人联系信息。沿用上一轮现成的中英询问草案，不重复改写。

## B：修补纯合成合同中的遗漏不变量

在**独立公开GitHub文档checkout**中，只允许修改：
- `prototypes/toy_g1_contract.py`
- `prototypes/test_toy_g1_contract.py`

当前toy已验证12帧与锚点等条件，但尚未要求 **至少3个互不重叠参考时间区间**。为此新增严格区间校验、拒绝重叠/无序/无效端点的错误码与负例；保留原10项回归，必要时将原toy有效场景调整为3个不重叠区间。新增同粗时间bin但细时钟不一致、未知真实token预算不可判公平性、参考区间内锚点覆盖、保护来源UNKNOWN不可放行的测试。不要为了通过删掉失败断言。只使用标准库和完全虚构的toy数据，在已有Python环境执行 `python -B -m unittest discover -s prototypes -p "test_toy_g1_contract.py" -v`。记录实际执行数、PASS/FAIL/SKIP和修改范围；失败如实报告。本任务不开发真实视频adapter、不运行任何模型、不导入本地私有研究代码。

## C：可证伪研究分叉决策

输出 `docs/codex-artifacts/VLM-BATCH-005/research-path-decision.md`，一至两页：

- 路线1：若能取得明确许可、无答案必要参考区间、同版本真实PTS及≥40个保守独立来源，则继续申请固定12帧D1/D2诊断的数据门复核；现在G1 HOLD。
- 路线2：若这些条件无法满足，建议停止“已覆盖必要gold区间”的假设，另行预注册不依赖参考真值的观测鲁棒性问题。写出可证伪假设及至少三种强替代解释（例如帧时间分布、画质、视觉token预算或检索偏差），不以历史准确率或toy通过宣称创新。
- 明确需要用户决定的下一步（是否主动咨询官方数据访问路径、是否调整研究命题），并给出停止同类反复静态调查的条件。

## 资源和提交范围

**0 GPU/模型QA/训练/评分调用，0视频解码、受限媒体或整套数据下载，0对外联系，0原研究工作区/conda/CUDA/锁/历史账本修改。** 只允许公开小文件、toy合成测试，不允许再次重跑旧实验。

一次安全提交只包含：上述 A/C 两份新 Markdown、B 两个 toy Python 文件、以及在 `docs/codex-results.md` **追加一条** `### VLM-BATCH-005 ...` 的A/B/C合并结果。提交前检查脱敏及stage路径；Git冲突停止，不强推；不改 `docs/next-steps.md`、`docs/research-overview.md`、`AGENTS.md`。任务包结束停止，用户保留同一 Codex 聊天框。

**验收只证明本批任务执行，不升级G1，也不授权真实GPU实验。**
