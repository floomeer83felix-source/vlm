# 079部分验收与080追加日志修复后完成原实验

2026-11-03（北京时间）｜ChatGPT研究负责人。

**079按部分交付验收关闭：startup/复用/缓存身份/36帧processor PASS、1媒体成员完成，科学门INCOMPLETE。唯一READY：[080完成同一已批准实验](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-FINISH-080/README.md)。** 不因基础实现错误把已批准媒体/GPU/4500步重新申请；不增加源/科学配置/媒体总字节/GPU/真实更新。原D/070关闭、069暂停。

## 079实际完成、失败和范围

[48dd29c](https://github.com/floomeer83felix-source/vlm/commit/48dd29cb7946433bf6fb4092fce52a05e193e4a4)，父ae08419，精确九处及results唯一八行append。负责人**2747项公开检查**通过：源码LF SHA256 `064041861cfd802808e014bbd8fc7101e4868f5919bd45c853a69969dae745a0`、六科学函数本机重新parse的AST与078相同、9/162/42表全分母/科学NA、metadata/资源/请求/byte账本及剩余算术。报告中的Win端函数digest序列化本身不冒称跨运行时逐个复现，本次独立直接比较两份源码AST等价。不访问私有Windowspayload/输出，不重放Qwen/头/视频或真实训练。

079在26.735秒startup、0.547秒reuse、14.656秒registration、0.453秒manifest后通过前置门，共42.391秒/当轮581.23。复用原07822987历史metadata核验，新3556项选择/标签/关系绑定PASS；32源20/4/8、138问题、1152符号答案/2304关系不变。12个model-file当前stat/旧076catalog身份及小源码hashPASS，new全weights hash0，仍只是缓存hash/stat连续性。首次真实CPU processor-only36帧fixture PASS：grid[18,14,14]、pixels[3528,1536]、882tokens及native拆分一致，未load权重/forward。

进程封装修正已起作用：Job active上限8/readback正确，实际峰3、native峰16；所有六Job最后active0。13条观察PID记录中python6/conhost6/cmd1，Job总process16，3个快进程未观察到身份；不作完整树认证。该过程与077线程门、078 active3>2是不同阶段，不能说原限制又触发。

媒体请求6 STARTED/5 CLOSED/1 FAILED；应用body34690881B，全部已声明Range长度保守上界36263866B，网络11.547秒。第一个成员compressed15816410B，uncompressed15770653B，local ZIP64/method12/flags0/BZIP2 EOF/size/CRC通过并flush落盘；但其SHA只在内存，**全局manifest未闭合，不能说媒体有完整历史SHA seal**。第二成员body部分读取，另30未请求。第6请求BODY阶段`os.replace(network-state.tmp,network-state.json)`抛PermissionError/WinError5，exit1/no kill/no supervisor-budget-stop；精确占用者/并发原因UNKNOWN。不能把可能的监督器读取锁说成已证明原因，不能归为远端版本/样本/科学门失败。

所有解码/RGB/模型load/GPU/root/features/真实配置/4500更新/评分均0；3456 B0和62208头逻辑输出全未知、科学门INCOMPLETE，非负结果。最后5项核验只核已结束Job active0，完整科学oracle未运行。显式旧metadata1096206B/prepared3515795B全部settled、未结算0；078中断旧unknown保守上界仍保留。host/native/物理IO、wire prefetch实际与连续配额/快进程观测有缺口，full_resource_contract_certified=false。

## 已完成的负责人修复与验证

旧worker反复替换被监督器观察的状态文件；080改用[只追加progress组件](../../prototypes/timestamped_triples_080_progress.py)：单writer独占新journal，seq/job-id/前hash/本hash链、每行fsync；读者按偏移只接收完整校验行，半行保留上个deadline，完整损坏直接FAIL，缺失文件只用固定bootstrap/global deadline，不默认刷新IDLE。Windows reader使用显式FILE_SHARE_READ/WRITE/DELETE，不重命名/替换/截断/删除被观察文件。写入或fsync失败后writer标failed，禁止再append。

组件LF SHA256 `0b12bfed5a2f74f4856ca841967d648fbd29fd3337e96d0a37ba7b0cf1d44140`。已实际通过**213项本地可移植检查**，含reader持续持有时200次append、模拟replace始终PermissionError而不调用replace、半行/补全、损坏/跨job/乱序/重复key拒绝、独占writer、非finite deadline和fsync失败后不得再写。无真实网络/媒体/模型/GPU；**Windows共享API分支尚未实机验证**，须080在首次HTTP前并入一次fixture，不单开审计父包。

080先只读重核第一个已完成MP4的size/CRC并计算本次SHA，结合079完成ledger与原目录绑定，写新独立reuse seal；不冒称补回079旧SHA或redownload。剩余31完整compressed总565610565B。旧079body以全部声明Range上界36263866B收费，不拿应用读数当wire实际；原805306368B总额保守剩余**769042502B**。第二成员prefix/partial未持久，不能断点续传；080明确允许对这个未完成成员一次完整重新获取（其header/fields也重新验证），然后30未请求成员各一次。

这需要新≤93个Range、合计6+93=**99**，原96请求上限仅增加3，专用于一个中断成员的恢复/头验证；科学媒体字节仍≤原768MiB，不给已完成成员GET、不引入源/科学额度/自动无限retry。其余GPU3600秒16GiB/1428root、4500真实CPU更新仍未使用，原科学函数/参数/seed/门保持。新CPU准入≤538.83秒、network≤1788.45秒、训练≤1796.25秒、预测review≤599.52秒；old/prepared余量和根/父跨078+079+080累计见[续作表](../codex-artifacts/VLM-TIMESTAMPED-TRIPLES-FINISH-080/continuation-scope.md)。

每成员数据/CRC/SHA/版本seal立即fsync，禁止等32个完成才留内容hash。允许在080内**一次非科学基础设施修复**，保留v1失败/源码/seals/已耗资源，只恢复未消费阶段、不修改科学图/GT/评分/门、不重放模型/优化步、不超93新请求或允许额外失败HTTP重取。不得将报告渲染/监控小错自动拆成另一个空科学父包。遇到必要科学输入不确定/校验失败/预算超限仍停止。

080本地新消息后一次连续完成余下媒体、实际RGB、完整基线兼特征和A/I/S六seed4500更新及独立评估；同已批准科学范围不再请示。数据仍是官方train开发留出，物理来源/可见性/预训练重叠未知，不声称新机制/外部确认或写论文。完成后按原门保留/关闭，不补seed/换头；九处push后STOP，不自动081。
