# 078完整媒体、GPU及训练范围授权回执

2026-11-02（北京时间）｜ChatGPT研究负责人登记。

**APPROVED_078_INTEGRATED_MEDIA_GPU_TRAIN_SCOPE / AWAIT_FRESH_078_START。** 用户在看到[078完整合同](./README.md)及本次新增范围后，明确回复：**“批准”**。授权绑定制定合同时main `259590c36b7c39e2c217158a68374c3c4a15ab08`、原README Git blob `2b2050a89d4ab814ba12c6011baf2ea3e6b4cf6d`。本回执仅确认该合同原范围已获批准，不改数据、算法、投入门或资源限额。

## 已批准的一次完整父包

- 固定32个Perception Test源媒体，保持原hash选择与20/4/8开发划分；由原离线metadata包及已验证078组件重新准入，按原六排列/六问构建真实RGB，不复活077。
- 媒体仅原官方archive固定generation/ETag的≤96个精确Range；网络正文≤768MiB、每member≤80MiB、累计≤1800秒；连接/header/body/无重试策略依合同。不下载整archive。
- 一次实际解码/采样，≤1800秒/100000帧；codec显式单线程，三段各12帧、统一36帧runtime输入。
- 同一本地冻结Qwen一次load/infer/unload，GPU累计≤3600秒、allocated≤16GiB、GPU Job RAM≤32GiB、最多1428新完整root前向；每次B0推理同时以只读hook取必要新特征，独立视觉/文字特征重算0。3480秒停止新调用、120秒闭合预留。
- A/I/S同341633参数、六seed、每配置250步，共4500次CPU真实更新，训练≤1800秒/RAM16GiB；不更新主干。最终预测/评分/独立核验≤600秒，保持原对照、软件守卫和事前门，不调参补seed。
- metadata/processor/软件准入CPU≤600秒；新独占根≤8GiB/4096文件、checkpoint≤64MiB、初始free≥12GiB、pre-sync父≤14400秒。旧metadata32MiB、media逻辑读4GiB、prepared及中间件读12GiB、同模型hash12GiB分别依合同计量。
- metadata单科学计算线程，Torch/BLAS intra≤4、interop1、codec1；原生辅助线程与compute分别报告，owned进程native采样停止阈值256、同时active≤2。原077 native4>1失败不倒填通过。

## 启动及边界

本地用户新消息明确078后，Codex安全同步main，重新读取AGENTS/看板/results/合同及本回执，核唯一尚未交付READY与输入/锁/预算。**同一已批准范围不再次请求媒体/GPU/训练授权；准入通过即同轮连续完成全部允许阶段，按原九处脱敏交付push main后STOP。** 没有本地ZIP路径只等待明确输入，不扫盘、不交空阻断包；实际失败按合同如实闭合，不能借授权自动重试/换样/超额。

本回执不是实验执行或科学收益证据：077仍为构建/训练NOT_RUN；负责人已做的078验证只有metadata本地构建。不能据授权声称RGB已制成、模型/训练已完成或核心创新成立。无新环境/模型安装、旧QA重放、手工标签、主干训练、论文、后台、自醒、自动079或额外数据范围。D/070关闭，069暂停；全部身份/输入账本/角色隔离/原门/失败分母和完整资源覆盖限制保持。
