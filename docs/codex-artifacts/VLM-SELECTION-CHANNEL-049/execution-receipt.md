# 049完整开发执行回执

2026-10-27（北京时间）。**FULL_DEVELOPMENT_COMPARISON / STOP_CURRENT_HYPOTHESIS / NOVELTY=RETAIN0。**
本轮四源×6题、240逻辑格、216独特输入全部实际运行并独立评分。不是合成推理、CPU负载冒充模型或引用旧分数。本文件只公开匿名聚合与通用资源信息。

## Git与授权

独立文档checkout安全同步main=3ede2ab；AGENTS、唯一未回报049看板、results、overview和完整合同/§10及引用设计重新核对。用户已明确批准整包GPU范围，后又批准有限原标注恢复及必要一次CPU候选重建，仍沿用049，不恢复旧父任务或旧余额。
有限文件名定位未找到原标注；用户随后要求恢复。当前用户同盘回收站只读删除元数据379条/44972B，发现两条原路径对应记录；按最新删除时间选一份，纯字节SHA与旧冻结引用一致后不覆盖复制回原路径，未解析gold。回收站源数据/元数据均未改。原移动/删除命令被自动审批返回blocked by policy拒绝，完全未执行；安全复制成功。恢复是用户授权的单文件数据操作，不是新下载。
输入表从指定017/018精确源文件和正常模型配置恢复；无全盘/无关目录扫描、无旧预测/答案/评分正文读取。新私有根此前不存在，无链接/reparse祖先，free空间通过256MiB+2GiB门，新的7200秒父窗口在入口齐备时一次启动。

## 串行执行与信息隔离

1. CPU processor启动优先：本地正常依赖、隐藏CUDA、local-only/trust_remote_code=False，无全局file-audit猴补丁。两次自有灰色小探针全部原生回调/grid/token/roundtrip通过；CUDA未初始化，权重/forward/generate0。
2. 独立nongold投影器对混合原JSON物理打开1次/1854695B，词法跳过未保留值，包括未取字段的非有限字面值；保留字段非法则不放宽。gold字段解码0，不声称gold所在文件零open。六源合计220个已冻结nongold问题，最终资格100题；只按原ordinal/源序取S01–S04各6题，其他源不换入。初步自动清单、语义复核及最终冻结全部保留，均早于任何解码或模型输出。
3. 当前原媒体前后size/mtime/inode/device同runtime匹配、旧size/mtime相符，无链接。每源仅一次原48目标提取、每目标一次后向keyframe seek，不额外遍历/补帧/重试，不解音频。四个48帧规范化数组按原PIL BICUBIC整帧缩放192×288，合计31851008B≤32MiB；原尺寸帧/整视频/模型视觉tensor正文不保存。全媒体SHA不重新计算，不升级历史字节/物理来源/时钟资格。
4. 非阻塞原GPU文件锁和协作mutex取得后，只做一次起始telemetry，再在Qwen加载前复核一次；正确3090/UUID/bus核对通过，free22821/22512MiB，util11/3%。不等待空闲、不杀peer、不重query。
5. 一次SigLIP float32/eval/inference_mode，192图/24题干，batch≤8，24图batch/3文本batch。没有可信完整特征缓存，按授权全量提取一次；仅question文本，不含选项/gold/source ID。有限float32→CPU float64 L2/cosine，稳定分数降序/index升序Top12，再恢复时间顺序。
6. 所有逻辑条件的实际原生CPU输入一次正式制作并封存全部返回字段，真实callback/时码核对；按全局0-based题序mod10轮转条件，按首次出现独特输入顺序执行。相同输入只生成一次。GPUworker只读匿名nongold和新规范化数组/模型配置，无原标注路径或真实source UID。
7. Qwen3-VL-4B-Instruct本地登记目录、BF16/SDPA、eval/inference_mode、seed19、batch1、greedy/max_new_tokens64/fresh context，无warmup/额外forward、第二模型或训练。权重load/encode/generate均在私有fsync账本预扣，216次attempt=216return；每次新输出2tokens、均自然EOS、严格单字母有效。432个观察到的模型forward步骤均发生在216次generate内部，不是额外调用。
8. 实际模型Job/PID active0、队列/源码/nongold绑定核齐后，独立CPU scorer只打开原JSON一次≤4MiB，词法投影仅解码冻结24题gold与join字段，不解码其他gold值。不读取旧评分。标签/题目join均有效，完整N24/240槽保留。
9. 独立stdlib复核85断言通过，未导入被测聚合或重开gold；对派生正确性表重算D/I、来源权重、全条件分母和去重/计数。这是算术/收据独立复核，不是第二次独立原标签认证。

## 必要测试和事件

初轮19例30断言PASS；保守nongold语义处理代码有实质变化后，必要回归21例32断言PASS。覆盖真正同题跨源矩阵、有限性/零范数、稳定tie、Uniform去重仍保留逻辑格、失败分母、不同n_s来源等权、UNKNOWN及手算D=2/3、I=1/4、nongold/有限gold词法投影与共享不重复成本。没有历史suite或模型失败重答。
完整GPU执行之后，控制器打印尾部日志时遭GBK UnicodeEncodeError，外层打印进程exit1；此前已持久化的真实inference child exit0、active0与216返回均完整。保留错误，不重跑、不伪造为模型失败，评分根据实测退出/绑定门，而不是外层exit0判成功。
处理器调用需明确区分：2次自有灰色小探针；106次nongold长度资格处理（由已完成分支计数推导）；240次逻辑正式处理，共348次Qwen processor调用、正常配置实例3个。它们不是额外Qwen generate。106次资格处理另行披露，不归入“仅2次小探针”冒充零成本；正式UO/UR仍各做CPU处理后按完整输入指纹合并生成。

## 完整性、成本和预算

| 阶段 | Job监督wall秒 | Job user秒 | Job kernel秒 | peak commit B | active0 | child exit |
|---|---:|---:|---:|---:|---:|---:|
|bootstrap|30.781000000|4.281250000|3.765625000|1185579008|0|0|
|prepare|9.438000000|5.515625000|3.468750000|1185214464|0|0|
|initial-suite|0.296000000|0.125000000|0.093750000|125050880|0|0|
|suite|0.297000000|0.125000000|0.093750000|125423616|0|0|
|cache-R1|11.469000000|11.734375000|1.843750000|191954944|0|0|
|cache-R2|9.328000000|7.578125000|1.531250000|198189056|0|0|
|cache-R3|16.563000000|15.484375000|2.531250000|199438336|0|0|
|cache-R4|42.141000000|55.015625000|4.609375000|210202624|0|0|
|infer|70.438000000|37.484375000|19.062500000|18486960128|0|0|
|score|0.422000000|0.265625000|0.062500000|17203200|0|0|
|verify|0.125000000|0.046875000|0.015625000|14553088|0|0|

独立监督阶段outer合计191.298000000s，其中CPU阶段120.860000000s，四源候选共享准备79.501000000s只计一次。GPU整Job保守包络70.438000000/1800s，包含权重意图之前的CPU配置准备和退出余量；worker首权重意图到显式卸载61.781000000s不冒充PID退出精确值。整个GPU Job bound比合同定义更保守，已独立核active0。
SigLIP load/encode/CPU选择inclusive 3.281000000s；全正式CPU输入准备inclusive 2.453000000s（逐请求processor wall和2.265000001s是内含项）。Qwen load意图至首generate意图4.250000000s为标记间包络。generate wall和48.228000001s；同步首forward/prefill和35.404000002s，后续decode-forward和12.059999999s，均为generate内含带同步开销的wall，不相加到父包络、不称纯GPU kernel计时。
PyTorch peak allocated=9294470144B（8.656GiB）≤18GiB；最大Job commit=18486960128B≤32GiB。全部11个本轮Job收据实测active0，无超时/kill/OOM、无peer干预。自己的child先CREATE_SUSPENDED、入Job后resume，4 CPU affinity/线程配置，parent只减自身时钟，传递剩余阶段时长，不跨runtime减绝对perf_counter。私有监督器保留；公开角色模块不是对抗性隔离证明。
源视频Python接口read返回323587167B，读前保守预扣323704895B≤48GiB；无预扣退款。规范化缓存读取按4个一次文件payload 31851008B记账，np.load底层实际read返回/OS物理I/O未装计数器，明确UNKNOWN，不伪称精确测量；这不改变已知四文件payload/shape的输入范围门。旧指定调用索引87038B/6文件、545 STARTED记录，只提身份/状态。它们未保存完整input hash，本轮已知旧system模板不同并有018原runner谱系绑定；不宣称全库exactly-once。未读旧预测或答案。
新根关闭前快照67files/33498647B≤4096/256MiB；初始free=349767192576B，满足配额外2GiB。父从入口齐备首次运行起到本报告2789.523/7200s，包含实现/等待/语义复核/清理。目录快照不是卷级硬配额证明。
CPU/GPU阶段、内含组件与文件payload的度量层次在JSON分列；缺失的缓存底层字节精确值不填0。不存在用正常CPU负载冒充GPU模型调用的成本表。

## 身份与隐私

公开不含问题/选项/原标签/逐题预测、真正source UID/路径、媒体/数组/特征/权重、完整时码/选帧序列、原账本或任何输入/内容身份摘要。模型输出只用于严格解析评分和既定配对诊断，不作选择或停止规则调参。只公开本轮通用源码SHA及匿名聚合。
实验应用网络/下载0；旧任务重跑0；环境安装/永久修改、ACL/profile/凭据修改0；训练0；无全局文件audit猴补丁。恢复阶段原始文件复制与nongold原文件物理open被如实披露，没有以“答案未解析”为理由声称原文件零读取。

## 交付与STOP

两新模块、两报告、40行条件CSV、匿名JSON及codex-results一条父追加为原7处科研交付；另外3处规划文档只登记此前用户明确批准的同包范围/单文件恢复和执行事实，不替研究负责人签验收。
科学结果D=1/72、I=0，预注册STOP_CURRENT_HYPOTHESIS。所有实际调用完成，无未运行缺口；不以此宣称论文创新、正式榜分、独立确认或普遍阴性。负责人验收待定，一次普通安全push后停止，不自动050/扩样/二模型/修复/下载/训练。

源码`prototypes/selection_channel_049.py` SHA256 `e24bb6fa4ff1285900cbbbeeda4bccb0e1bbddd9f1a849693db722899f6272d1`。

源码`prototypes/test_selection_channel_049.py` SHA256 `72969b57a7545840f654415c37ef29b990eb7baefc0c02d652e9fc7bd14bbfdd`。

发布前Git fetch遭TLS握手失败，未重试。首次main同步已成功；只从该已知基线普通非强推一次，若远端前移或传输失败则保留本地并停止，不绕过。
