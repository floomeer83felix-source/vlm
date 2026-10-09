# VLM-BATCH-013：未取得媒体的病例时钟决定

2026-10-09，main46bc361。**工具前置BLOCKED，0媒体／0Range GET**；详见[资源和隐私收据](./remote-range-and-privacy-receipt.md)。没有时钟观测，不能从CSV、同类事件或官方评测器标签反推两例媒体事实。

## 2. 病例冻结未执行

拟定规则：训练越界记录0≤s<L<e且δ∈(1,5]；按SHA256任务前缀＋video ID排序确定越界候选，对照整行严格合法，要求不同subject、length差≤5秒，再按同哈希排序。该规则仅在虚构输入上验证，候选ID／subject未从真实CSV取得，没有selection manifest。

本轮不在工具缺失时先挑真实两例，亦不将既有347／97,723当本试点可获取数。没有remote目录／时钟结果，更没有按结果改变选择或容差。若将来无法满足唯一身份及匹配，应STOP而非换测试源；本轮这一资格也仍UNKNOWN。

## 6—7. 容器与packet时钟：全部未观测

| 病例 | 公开类别 | 原因 |
|---|---|---|
| CASE_OVERFLOW | **CLOCK_UNKNOWN** | 既有ffprobe未定位、未选择／取得媒体，duration/PTS/timebase未测 |
| CASE_CONTROL | **CLOCK_UNKNOWN** | 同上；不能用CSV length填媒体时钟 |

容器format.duration、视频stream.duration、首末视频packet PTS/DTS/duration是不同对象，本轮均UNKNOWN；没有codec、B帧、VFR或CSV-end相对媒体末端的数据。没有精确时长、动作端点、视频ID、人物映射或私有时间戳可披露。

### 仅合成的方法合同，不是真实时钟验证

组件的ffprobe命令仅指定本地file协议、视频v:0、format/stream及packet字段；不含-show_frames、截图、转码／像素输出或网络输入。其合成对照使用timebase、名义单帧时间和1ms报告精度下限来冻结比较容差；没有实际media runtime调用。保守实现遇B帧／不一致帧率／缺packet时间等返回CLOCK_UNKNOWN，并不声称这些视频不可分析或最后packet就是最终显示帧。

字段一致性模拟只能校验数值流程；真实使用还需要：已验证工具／私有ledger／受控下载、同媒体版本与CSV来源桥接、video stream原点和packet覆盖完整性、容器与stream及packet-end分别解释。未满足这些条件，不能升级LENGTH_APPROX_MATCH或LENGTH_DIFFERS。

## 8. 外推边界

两例即便未来得到MATCH，也只提供病例与该480p版本的时钟线索；不判动作发生／完成，不外推19,625旧strict拒绝token、347 P1组、97,723 P2 pair。V1不含画面／音频观察、动作边界人工核验或模型，只能停在容器／packet层；V2必须另获明确授权。

本轮连两例也未取得，因此没有timebase／媒体长度新证据。不把工具阻塞误归因于数据许可、服务器不支持206或ZIP64结构，因为这些真实条件尚未测试；也不把合成ZIP/HTTP案例当真实官方服务收据。

## 10. 三门裁决和下一单点需求

| 门／研究层 | 当前状态 |
|---|---|
| A_OFFICIAL_FRAME_POLICY | 沿012的限域VERIFIED，本轮没有新增／修改该证据 |
| V1_MEDIA_ACCESS | **BLOCKED_EXISTING_FFPROBE_NOT_FOUND**；源锚点、206、成员、ledger及端到端协调器未核／未放行 |
| V1_CLOCK | **UNKNOWN**，两个CASE均无媒体观测 |
| B_TIME_BOUNDARY_QUALITY | **HOLD**，没有原始边界／同版时间语义证据 |
| C_EVENT_TRUTH | **HOLD**，不能生成ordinal／negative／自然语言真值 |
| LONGVIDEO／NOVELTY／GPU | **FAIL_AS_SOLE_DATASET／RETAIN0／BLOCKED** |

**停止本轮执行，不继续下载或扩大权限。** 下一最小缺失事实是可验证的既有、非原科研conda的ffprobe入口；当前仅知PATH及有限常见／已登记runtime候选未找到，不断言全机没有工具。由用户／ChatGPT另行决定工具定位或安装授权（本轮不安装），并对后续端到端受限协调器安排新的安全审查，不能把本未完成协调器直接当可运行试点。

若未来按需官方访问无法在64MiB与支持的ZIP结构内取得冻结两成员，STOP访问路径；不借本次授权获取13GB、换镜像或未冻结的影片。当前不申请V2、一揽子视频／GPU或自动安排014。

资源全为0实际媒体、GET正文、packet probe、画面／音频核验和GPU；仅本地source SHA读取、工具／路径检查、16项虚构标准库测试及脱敏交付。原metadata树、科研代码／环境／锁／账本及历史结果未改；规定5处普通push后停止并保留当前聊天。
