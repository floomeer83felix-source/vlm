# 078部分交付验收与原批准范围的079完成安排

2026-11-02（北京时间）｜ChatGPT研究负责人。

**078按部分交付验收关闭：metadata PASS，科学门INCOMPLETE；唯一READY为[079完成已批准实验](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-CONTINUE-079/README.md)。** 本次新消息触发负责人审查与新一轮安排，不是执行者自动续做。用户已明确批准078整包；同样32媒体/GPU/4500更新尚未开始，079明确延续该尚未完成的授权，科学额度不增加、已耗资源扣账，不再次申请同范围权限。D/070关闭、069暂停。

## 验收事实

[7d29576](https://github.com/floomeer83felix-source/vlm/commit/7d295766fa6a6d96e140da26ff196b64d0c82872)，父598292f，精确九处及results八行唯一追加。负责人**3888项公开/符号数学检查**通过：核原包预览计数、metadata选中/分拆总数、9/162/42行全分母和NA、资源停止/闭合及两组纯符号人工数组的scorer PASS/FAIL边界；未访问私有模型输出或重放媒体/头/Qwen。科学源码LF SHA256 `1a57c1588d0d00a10cfb0bd1db417cca8176f3a93207f48bd16dce5c9daacd6a`，metadata组件`c10f863190a6ccc3f4d961d173dade99c80f35453548e8d523704b9b232bbe34`。

078 metadata Job实际9.469秒/39,743,488B，exit0/active0，完整CRC/manifest/原JSON/ZIP64/有理数独立22987检查及32有序owner比对PASS。2135视频/13644动作：2678合格段、10565重复或空文本、401边界失败；1376候选/280eligible；32源/20-4-8、29文本/138问、192符号变体、1152答案/2304关系。媒体仅目录证据：压缩581426975B/解压579702574B，最大71166131/70872100B，metadata总帧28139；实际视频/PTS/可见性未验证。

一次synthetic head fixture核341633参数、forward/backward/打乱support通过，3.750秒，1人工forward/1backward、0optimizer。随后模型identity/processor注册Job在9.296秒处因**Accounting.active=3>2**停，peak865251328B、exit99/killed=true、最终active0。失败Job及其精确辅助进程身份未落完整进度，身份/子阶段UNKNOWN。不能断言第三进程是恶意、计算worker或确定的Python launcher；也不能把配置active2当实际满足。没有processor fixture完成、weight load/媒体请求/GPU/真实训练/预测/评分。

fixture v1将PID列表population错标为active，实际Accounting峰UNKNOWN；执行者在首次annotation前修计量并重封，fixture未重跑。后来的registration失败使用已修正Accounting计量，是独立实际停止，不能说它只是旧错误。所有四Job最终active0；metadata22987独立数据核验与最终3项停止闭合核验范围分开，完整科学oracle未运行。9/162/42表正确性NA，3456/62208逻辑输出全未知，不将未知评分0%。

已耗preparation18.765秒、训练fixture3.750秒、review0.203秒；父报告961.057秒、根51文件1959653B，checkpoint0。registration显式读计数随进程被杀丢失，模型hash实际字节/完成与其它角色实际读量UNKNOWN；不是0。old前置1MiB只是预留。宿主/Git/隐式native/物理IO/连续线程和周期磁盘配额覆盖仍有限，full_resource_contract_certified=false，不追认完全合规。

## 修正执行封装，不改变科学实验

079不重跑已合格metadata、既有head fixture或已消费QA。复用明确078私有输出并独立核固定选择/GT/关系身份。直接启动既有绝对Python exe，禁py/conda run/cmd/PowerShell套娃；科学worker仍一个，owned active上限改为8，逐阶段记实际PID/PPID/可执行basename及Accounting/PIDlist两口径和限制readback，原生线程256与Torch4/interop1/codec1保持。一次纯启动/小依赖预检在正式研究payload前完成，异常先保存实际进程证据，不再因无身份的3>2反复消耗科学任务。

不重做被中断的全权重hash。076已封存的model registration含完整hash/graph和每文件size/mtime；新增[079 identity组件](../../prototypes/timestamped_triples_079_identity.py)只核catalog graph、全文件集合和当前stat，再核小安装源码hash。若任何stat/graph不符则在模型前STOP，不能悄悄全量rehash。它是`CACHED_076_HASH_PLUS_UNCHANGED_STATS`，不是新的内容逐字节认证。078未知model-hash读量按旧完整12GiB保守预留，079新权重hash读0；框架未来实际load另列native覆盖。

新identity组件LF SHA256 `89567c6d5d31166be0e319cf4837292c828d2c593c8d4d6d843fd154df7edf6c`，本地6个纯合成接口情形通过：缓存graph/stat合法接收、graph/mtime/source/file-set/path异常拒绝；未读真实weights或测试Windows/processor。本测试只验证身份桥软件，不证明未来运行成功。

修正I/O账本为**读取前持久预留，完成后实际结算**，强杀也留上界。078未知读量不被当零；079新增小型旧元数据读8MiB、prepared12GiB明确单列，和078最大预留合并上界可达old40MiB/prepared24GiB/modelhash12GiB；这是有界本地CPU/I/O修复，不添加媒体/GPU/训练实验。实际媒体仍0，所以原768MiB/96请求和GPU3600秒16GiB/1428root及4500更新不变；prep≤581.23秒、CPU训练≤1796.25秒、预测核验≤599.79秒扣除已耗。根078+079合计≤8GiB/4096文件，079父≤12000秒，旧父单列，能读取最终闭合时再核合计14400秒，缺失则覆盖UNKNOWN，不伪认证。

## 下一步与科学边界

[079合同](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-CONTINUE-079/README.md)及[续作授权依据/预算](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-CONTINUE-079/continuation-scope.md)明确同一尚未执行科学工作，由本地新消息启动一次完成processor准入、媒体/实际RGB、完整B0兼取特征、A/I/S六seed4500更新和独立评估。原数据/架构/seed/损失/门/对照/分母不变，旧078不修跑、日志不回写；不再索取相同科学范围批准。

全32仍是官方train开发划分、Perception Test与TOC-Bench来源可能重叠，参与者/录制/预训练/可见性UNKNOWN；元数据通过不等于答题收益或核心创新。完成后按原门保留/关闭此配方，不堆seed/换头/改门；不写论文或自动080。负责人验收同回合给下一步。
