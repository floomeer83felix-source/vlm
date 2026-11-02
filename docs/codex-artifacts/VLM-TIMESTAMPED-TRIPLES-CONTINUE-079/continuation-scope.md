# 079续作依据与累计预算

2026-11-02（北京时间）｜ChatGPT研究负责人。

**APPROVED_CONTINUATION_OF_UNFINISHED_078_SCOPE / AWAIT_FRESH_079_START。** 授权依据是用户在本会话对078完整合同明确回复“批准”，已登记[078授权回执](../VLM-TIMESTAMPED-TRIPLES-TRAIN-078/authorization-receipt.md)，批准登记main598292f。本次用户反馈078部分交付后，负责人按长期“验收同回合给下一指令”要求，明确将**同一尚未完成的科学工作**交079执行。这里不冒称用户另行说过“批准079”，也不以新父号自动生成科学额度；相同已批准范围不用再次请示。

078已闭合，数据32组已合格，但媒体请求/响应body、解码、GPU权重load/root、真实optimizer更新全部0。079继续原32源、六排列/六问、相同Qwen和341633参数A/I/S六seed，不加数据/模型/seed/实验条件或训练步数；原科学投入门不变。需要本地新消息明确079；不是后台自醒或执行者自行续做。

| 范围 | 078已耗/未知 | 079明确额度 |
|---|---|---|
| metadata/processor/软件准入CPU | 18.765秒（metadata+失败registration） | ≤581.23秒，metadata不重构，直接复用闭合输出 |
| 媒体正文/请求/时间 | 0B/0次/0秒 | 原≤768MiB/≤96精确Range/≤1800秒，不增源、不重试/整包 |
| 解码 | 0帧/0秒 | 原≤100000帧/1800秒，每源一次 |
| GPU/root/load | 0秒/0次/0次 | 原≤3600秒/allocated16GiB/≤1428完整root/一次load；无分离特征重算 |
| CPU训练 | fixture3.750秒，真实更新0 | ≤1796.25秒，全部4500真实更新；既有fixture不重跑 |
| 预测/评分/独立review | 停止核验0.203秒 | ≤599.79秒，原62208逻辑头项/25704实际eval上界及3456 B0逻辑项 |
| weights全量hash | 被中断，actual UNKNOWN，按完整12GiB上界预留 | **新hash读0**，仅076缓存hash+现stat/安装源码桥接；不是鲜验hash |
| 必要旧元数据/新prepared显式逻辑读 | 078中断计数UNKNOWN，旧cap分别32MiB/12GiB保留为上界 | 079独立≤8MiB/12GiB；跨父保守上界40MiB/24GiB，actual与reserved分开 |
| 新媒体显式逻辑读 | 0 | 原≤4GiB |
| root/文件/state | 078报告1959653B/51文件，最终以闭合清点为准 | 两根合计≤8GiB/4096文件、state合计64MiB；不写旧根 |
| 科学并发/原生线程/Job进程 | 科学真实训练0，registration active3>2已停 | 一个科学worker；owned active≤8，native采样256，Torch4/interop1、codec1 |
| 父与free | 078报告961.057秒，最终闭合另列 | 079从pre-sync≤12000秒、free≥12GiB；可核旧最终计时则再核合计14400秒，缺失保留UNKNOWN |

仅修改运行封装、身份/I/O复核方法及有界本地CPU读取账本；GPU、媒体和真实训练权限均来自已明确批准而未执行的078范围。规则修订不抹掉078 active3>2违规、fixture计量或I/O未知。不允许扩大科学范围、补跑任何已STARTED QA/训练、重建环境、追加手工标签、写论文或自动080。

完整[079合同](./README.md)给出阶段门/归档与九处交付。准入通过后同轮连续执行、同范围不再次请示；实际错误按完整分母交付并停止，不为换ID绕过未决科学STARTED。
