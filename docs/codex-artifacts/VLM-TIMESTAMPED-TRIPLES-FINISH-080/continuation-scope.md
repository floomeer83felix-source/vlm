# 080明确续作范围与累计预算

2026-11-03（北京时间）｜ChatGPT研究负责人。

**APPROVED_CONTINUATION_OF_UNFINISHED_078_SCOPE / AWAIT_FRESH_080_START。** 依据用户已明确批准的[078整包授权](../VLM-TIMESTAMPED-TRIPLES-TRAIN-078/authorization-receipt.md)及长期“验收同回合给下一指令”，本次反馈079后由负责人明确安排080继续同一未完成工作；不冒称用户另说“批准080”，不自动新生科学额度，同范围不再次请示。079按实现错误部分关闭，不修写旧记录；080需本地新消息明确启动，不是后台续做。

| 范围 | 已耗/保守占用 | 080限额 |
|---|---|---|
| 网络body | 079应用34690881B，按全部声明Range上界36263866B保守计 | **≤769042502B**；跨父≤805306368B（原768MiB） |
| Range请求 | 079已STARTED6个，其中1失败 | **新≤93、累计≤99**；只恢复未完成成员一次+30未请求成员；这是对原96增加3的明确实现恢复，不增科学样本/字节额度 |
| 下载时间 | 07911.547秒 | ≤1788.45秒 |
| 已完成媒体 | 1个，15770653B；079无持久SHA总manifest | 只读size/CRC/新SHA重核和新reuse seal，**不得GET该成员**，不重解压 |
| 余下媒体 | 31个compressed565610565B | 同源/同generation/ETag，原解压aggregate640MiB/单80MiB范围累计；无自动重试/换源 |
| CPU准入/准备 | 07818.765秒+07942.391秒 | ≤538.83秒，不重复metadata/3556/22987/head或processor fixture；新增journal fixture计入 |
| 解码 | 0 | ≤1800秒/100000帧，32源各一次 |
| GPU | 0load/0秒/0root | 原一次load/3600秒/allocated16GiB/≤1428完整root，无单独特征重算 |
| 真实训练 | 0更新，旧synthetic fixture3.750秒 | 原4500更新、CPU≤1796.25秒，不增加seed/配置 |
| 预测/评分/review | 0780.203秒+0790.265秒 | ≤599.52秒，原3456/62208逻辑输出及完整独立oracle |
| 079专用old/prepared读账本 | settled1096206B/3515795B，unsettled0 | 余≤7292402B/12881386093B；078未知32MiB/12GiB仍另外保留上界，不当actual0 |
| 新weights全量hash | 078actual未知，原12GiB全额上界保留；0790 | **0**；沿用已认证缓存hash/current-stat桥，GPU前核stat连续 |
| 显式媒体读 | 079未读旧媒体payload做decode，network计量另列 | 总≤4GiB，包括首成员CRC/SHA重读及实际decode等，按实际/预留累计 |
| 根/文件/state | 078/079保留只读 | 三根合计≤8GiB/4096文件/state64MiB，free≥12GiB，不改旧根 |
| 父 | 079记录078最终1062.249976635秒；079最终以闭合为准 | 080≤12000秒，且078+079+080已执行父墙钟合计≤14400秒，排除用户等待间隔，不清零旧耗时 |

owned active≤8、一个科学worker、native采样256、Torch/BLAS4/interop1/codec1、CPU Job16GiB/GPU32GiB保持。逐阶段数据/方法/参数/门等按[080合同](./README.md)及引用的原078规范；本次只修追加进度通信、单成员恢复/持久seal及有界非科学修复。

请求上限96→99为明确的单次下载恢复安排，旧079原无retry约束和失败记录不倒填修改；不将它推广为无限retry或自动新任务许可。所有实际GET/Range预留和新旧失败byte计入原总量。只有未完成成员可按本合同重取一次，已完成媒体/已STARTED科学QA或训练步绝不重放。无新环境/付费/新模型/新源/手工标签/论文/后台或自动081。
