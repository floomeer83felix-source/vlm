# 081同一已批准实验：分块恢复与累计扣账

2026-11-03（北京时间）｜ChatGPT研究负责人。

**APPROVED_CONTINUATION_OF_UNFINISHED_078_SCOPE / AWAIT_FRESH_081_START。** 原[078用户明确批准](../VLM-TIMESTAMPED-TRIPLES-TRAIN-078/authorization-receipt.md)的32源/GPU/真实训练仍未完成；本次反馈080后负责人明确安排081，同范围不再请示，不冒称用户另说“批准081”，不自动新生科学额度。080闭合，不改旧失败；本地新消息明确081后执行一次父包。

| 范围 | 截至080 | 081明确范围 |
|---|---|---|
| 完整媒体 | 5个member seal、78060287B raw；compressed78235421B | 5源只读hash/CRC/stat复用，不GET/BZIP2；27源compressed503191554B待取，不换样 |
| HTTP字节 | 累计Range保守占用134757960B | 新≤670548408B，跨父仍≤805306368B（原768MiB）；不以应用值降低旧收费 |
| 请求方法/数量 | 21已STARTED，原080总上限99 | 改4MiB持久body Range：133data+54metadata=187初始；额外body恢复≤16、metadata≤8；新≤211/总≤232，这是明确执行方法修订，不添加数据/训练范围 |
| 每Range恢复 | 旧大body丢prefix、无新retry | 最多初始+1次；只取durable prefix后剩余suffix，固定退避2秒，全局恢复数/byte/time始终计账；身份/CRC/local-I/O错误不当网络retry |
| 网络时间 | 07911.547+080244秒 | ≤1544.45秒剩余 |
| CPU准入 | 07818.765+07942.391+0802.312秒 | ≤536.51秒；只测新stream adapter，不重跑metadata/head/processor/journal成功fixture |
| 解码/GPU/实际更新 | 全0 | 原decode1800秒/100000帧，Qwen一次load/GPU3600秒/allocated16GiB/≤1428root，4500真实CPU更新≤1796.25秒，不增seed/配置 |
| 预测/评分/独立review | 前轮review累计0.827秒 | ≤599.16秒，3456B0/62208head逻辑、25704实际eval上界和原门保持 |
| 显式old/prepared/media读 | 0791096206/3515795、080787791/235446/15770653B | 剩≤6504611/12881150647/4279196643B，包含5媒体重核/part复核/decode；078未知旧上界仍保留 |
| 新weights全量hash | 078未知占旧12GiB上界，后续0 | 0，cached076graph/hash+current-stat/小源码桥，不鲜验内容hash |
| 根/文件/checkpoint | 078/079/080保留只读、统计到最终闭合 | 四根合计≤8GiB/4096文件/state64MiB，free≥12GiB；新compressed.part计入，不删旧artifact腾账 |
| 父 | 078/079最终1062.250/1267.284秒，080最终读闭合 | 081≤12000秒且四父实际已执行时间合计≤14400秒，排除用户等待，旧耗时不归零 |

新最坏HTTP charge：503191554+16×4194304+27×(30+65535+65535)+8×131070=574888678B，小于剩余670548408B。原byte预算足以支持这次有限恢复；232是请求总数cap，**不能**把232次当232个额外4MiB的许可。每次全Range长度在HTTP前fsync预留，actual与reserve/prefetch UNKNOWN分开。

owned active8、一个科学worker、native采样256、Torch/BLAS4/interop1/codec1、CPU Job16GiB/GPU32GiB均不变。每chunk最多2尝试，全局24额外请求；禁止无限retry、全源重复获取、source/GT/门变更或已STARTED科学输入重放。必要校验/预算失败仍停止，partial文件/prefix/失败和扣账保留。

完整[081合同](./README.md)连续执行下载、真实RGB、完整基线及特征、A/I/S六seed4500更新和独立评估；不是另一个只测网络的任务。最多一次非科学基础设施修复沿080规则，不新增HTTP额度或科学重放。九处push后STOP，无自动082/环境改变/论文。
