# VLM-BATCH-017：V1访问与预算阻塞收据

2026-10-10。基线main `9e7bd45`，独立docs checkout安全fast-forward，启动时唯一READY=017且无017结果，013—016历史已回报。本轮最终执行状态：`BLOCKED_SYNTHETIC_GATE_FAILED`。唯一一次017真实入口在内置合成门停止；之后仅离线修正测试夹具并核验，不重启execute、不改变服务器策略、不补跑历史任务。

## 前置代码修复

父任务门移到所有工具、元数据/目录和网络操作之前。仅接受017，冻结017 README规范文本SHA以及013/014/015/016公开回报段落SHA，绑定已阅读的具体授权/状态/数值；单READY与无结果同时要求。不再使用“64/128/ffprobe”关键词授予权限，不接受其它父任务。默认模式即使授权通过也不调用工具、读元数据或联网。

Ledger新增actual body与不可退charged字段；所有官网/许可文本及媒体Range共享64MiB总限额与GET≤12。每次read≤64KiB，先原子写入reserve并flush/fsync，再read，返回后记录actual；短读直接STOP，超时/EOF保留全部预扣。ledger持久化失败则读取前停止，残留账本/.next或媒体根不得删除后重启。HEAD最多一次并持久记录，要求固定源、identity、正长度、带引号非弱ETag；Range再核总长/范围/长度/同ETag。

只允许015固定独立bin中的ffprobe，核其已有私有部署收据和exe SHA，拒绝PATH不同优先工具/Conda/全局回退；元数据和媒体隔离预检在版本调用前，CPU工具树加入媒体根重合排除。016安全opener/TLS/固定官方URL/NoRedirect保持原函数不变；原样本冻结、ZIP计算、时钟与ffprobe packet命令不改，64MiB/128MiB/12次/两例不扩权。

## 执行次序与透明失败记录

| 次序 | 真实事实 |
|---|---|
| 首轮外部合成 | 56方法：55 PASS/1 FAIL/0 ERROR/SKIP，suite3.981秒；旧mock Range客户端漏掉新增reserve，修其夹具，不弱化断言 |
| 第二轮外部合成 | 56 PASS，0 FAIL/ERROR/SKIP，suite4.837秒；原40个方法全部保留，新16方法 |
| 静态合同检查 | 017冻结合同与历史绑定PASS；科学/ZIP/016代理函数、来源与硬限不变；当时尚无真实HTTP/工具调用 |
| 唯一execute机会 | 显式017父任务，程序返回BLOCKED/SYNTHETIC_GATE_FAILED；没有进入主流程fixed_preflight/find_ffprobe/version或网络阶段 |
| 离线诊断 | 在临时合成LOCALAPPDATA与合成原工作区变量下复现56方法：55 PASS/1 ERROR/0 FAIL/SKIP，错误为旧Conda拒绝测试的AuditError；没有再运行execute |
| 离线夹具修复及最终核验 | 为该旧路径mock补充祖先检查mock，拒绝Conda断言保留。普通上下文56 PASS（suite6.629秒）；合成原工作区上下文56 PASS（suite10.190秒），均0 FAIL/ERROR/SKIP |

唯一execute内置套件继承了执行用原工作区环境变量；旧Path.resolve mock与新增祖先身份检查不兼容。此前普通环境外部PASS没有覆盖这一差异。主流程因此在安全门停止，而不是服务器拒绝或预算不足。生产身份/Conda安全检查未放宽，修复的是合成夹具。

该次内置套件的旧路径mock没有隔绝祖先stat，故不能宣称其完全没有只读身份元数据访问；没有工具内容读取或真实版本调用，也没有主流程原ZIP/CSV SHA读取。诊断及最终上下文套件使用合成路径并补齐mock。只用最终合成PASS不能抹去一次execute已失败，也不能把017重新当未执行任务。

## 本轮真实资源

| 指标 | 实际值或状态 |
|---|---|
| 官网项目页/许可GET | 0 / 0 |
| S3媒体HEAD / Range GET | 0 / 0 |
| Gyan/工具GET | 0 |
| 研究HTTP实际正文 / 已计费预留 | 0 B / 0 B；没有真实媒体ledger，不能把合成ledger当真实收据 |
| 实际版本调用 / packet-PTS调用 | 0 / 0 |
| 真实媒体保存数 / 媒体私有占用峰值 | 0 / 0 B；固定MediaPilot根和network-ledger均不存在，只读存在性复核 |
| 元数据SHA/物理隔离正式预检 | NOT_RUN，主流程未越过内置测试门 |
| 本机CPU工具正式预检 | NOT_RUN，本轮不重新认证015工具状态 |
| 源HEAD/强ETag/206/ZIP索引/两成员CRC | UNKNOWN / NOT_RUN |
| execute次数 / 追加机会 / 自动重试 | 1 / 0 / 0 |

GitHub授权的Git同步/交付通信不计作研究HTTP。合成临时目录、虚构ZIP/MP4/mock工具由unittest创建与回收，不是真实媒体预算消费。未写旧metadata/工具ZIP/014或015账本、原科研目录/Conda/PATH/CUDA/锁；未下载整包/镜像/STA、解码像素或运行模型/GPU。

## 阶段结论

离线修复代码及最终双上下文合成验证已完成；017真实机会已安全停止。不能据此判断官方服务器有无206，不能给本机正式SHA/隔离/工具预检PASS，不能声称已冻结真实两例或获得病例钟。只交本批五处，普通push后保留原聊天等待ChatGPT审查，不自动重启017或安排018。
