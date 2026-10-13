# VLM-EGO4D-AWS-META-005：区域/官方对象权限已证，清单流读取超时

2026-10-13（北京时间）。状态 **SAFE_METADATA_STOP / ReadTimeoutError（阶段C）**。真实manifest桶区域发现PASS，正确区域的manifest HEAD与GET响应均200，**AUTH_OK仅限本次官方manifest对象请求证据**；GET正文未完整读完，不能做UID join或媒体HEAD。实际S3尝试3/7，未重试或继续后续任务。

## 本地及入口

独立公有checkout原工作树干净，安全同步main `137b6b0`，核唯一META-005 READY/无旧回报，重读AGENTS、看板、结果、合同、原META-004合同及实测收据、总览和已核官方固定源码约束。预排LIVE-MEDIA-002与LIVE-AB-001仅QUEUED，未执行。

复用用户此前明确指定的同一个下载目录，精确基础文件名存在，无需编号副本扫描，不进入旧Downloads/其它目录。正规文件/目录无链接或reparse，实际1,854,695B、≤16MiB，完整JSON可解析且dev结构PASS；只提顶层50个UID及有限正时长，读取前后原字节SHA内存核验一致。完整解析技术上读到QA字节，但题目/选项/答案/canary不用于排序、统计或输出，没有重做QA资格审计。原文件未改、移、复制或重新获取。

专用隔离boto3 venv和ego4d静态共享凭据提供器PRESENT。SDK只为签名内部加载，未手工访问或回显credentials/密钥，不使用default/环境其它账户、SSO/credential_process/IMDS/STS/自动刷新。环境、AWS配置、旧研究资产均不修改。

## 真实阶段结果

| 阶段 | 本次发送次数 | 实测响应/结论 |
|---|---:|---|
| A：manifest桶HeadBucket | 1 | 301；从可信S3 TLS响应区域头得到允许AWS商业区域，区域发现PASS，不跟随Location，也不将A视为AUTH_OK |
| B：该区域manifest HeadObject | 1 | 200；对象存在/本次访问权限PASS，ContentLength=4,653,141B，ETag可用于条件绑定 |
| C：同一manifest条件GetObject | 1 | 200；响应长度及ETag一致、无压缩，流读取途中ReadTimeoutError；完整GET失败，不解析partial CSV |
| D：候选媒体贡献桶HeadBucket | 0 | NOT_RUN，未取得完整清单/候选 |
| E：最多两个媒体HeadObject | 0 | NOT_RUN |

区域探测响应头只在RAM验证并按SDK本地AWS商业区列表核定；生成正确regional S3域与签名，不把301 Location当新源。多个regional client仅按需创建并串行执行，不并行。全阶段发送前严格核HTTPS主机、桶/key、method、当前阶段只能一次及总≤7，fsync持久聚合计数；每client total_max_attempts=1、connect_timeout=5、read_timeout=12、连接池1、禁代理继承、TLS保持。传输包装器在SDK重定向/重试前捕获A的区域头；B/C非预期响应则立即停止。

本轮没有再次发送、隐藏重试、LIST/STS或媒体GET/Range。清单GET是唯一允许研究数据正文；只流式读取到私有RAM，不落CSV文件或公共日志，不从partial内容选样。实际地区字符串、响应头/ETag/VersionId、URI/key及任何UID不披露。

## 计数、字节与已证/未证门

| 项目 | 本次真实结果 |
|---|---|
| 总S3 HTTP发起尝试 | 3 / 7 |
| HeadBucket / HeadObject / GetObject | 1 / 1 / 1 |
| manifest HEAD成功数 | 1；无对象HEAD失败 |
| manifest GET响应/完整成功/流读取失败 | 200 / 0 / 1（ReadTimeoutError） |
| manifest声明长度 | 4,653,141B，≤8,388,608B PASS |
| GET已读应用正文 | 2,555,904B，≤8,388,608B；小于声明长度，未完整取得 |
| 输入视频元数据数 | 50 |
| v2_1 UID精确命中/无歧义可HEAD候选 | NOT_RUN / UNKNOWN，不写成0匹配 |
| 媒体已知大小数、≤4GiB数量、合计≤8GiB | NOT_RUN / UNKNOWN |
| 媒体HEAD/GET/Range、媒体正文 | 0 / 0 / 0 / 0 |
| LIST / STS / 隐藏重试/额外发送拦截 | 全部0 |
| GPU/真实模型/解码/ffprobe | 全部0 |
| 单次现场耗时 | 约169.696秒，≤15分钟 |

AUTH_OK由指定官方对象HEAD200及GET200响应支持，不推广成所有贡献桶/所有数据权限、账号身份或媒体可用性保证。清单有可靠长度和条件绑定，但传输未完成；本轮唯一新阻塞是阶段C流读取超时，不是profile缺失、区域未知或403。

应用正文计数记录成功返回脚本的read字节。SDK/HTTP库在超时前可能已接收但未返回的缓冲字节、TLS开销和网卡wire总量没有精确计量，不能声称线上总字节等于2,555,904B或整个8GiB视频流控已认证。超时后不补读、不发Range、不换region/发行/镜像，不重新启动本ID重置计数。

## 科学边界与交接

真实凭据可用于该manifest访问、区域定位和官方对象大小已得到实物证据；仍无完整manifest、UID_PRESENT_IN_V2_1或任何视频HEAD大小，RELEASE_AND_CLOCK_BRIDGE_UNKNOWN保持。无法据本轮选出可GET媒体；不将官方批准至2026-10-26或GET200当作后续下载/GPU授权。未来若需要处理本次超时，应另行明确新任务请求/流读取超时边界，本轮不自行调整12秒超时或重试。

公有严格只交本匿名收据及结果末尾唯一父回报；0合成测试/工具安装/额外研究规划、0真实媒体/模型获取、0旧实验/Charades/ledger/锁/环境/PATH/AWS配置修改。私有脚本与无秘密聚合计数不上传，JSON/CSV、真实UID/QA、账号/密钥/Windows目录、实际region与响应Header原文不公开。

正常main push一次后立即停止，保留聊天等待验收；没有执行预排的两个QUEUED任务或继承旧媒体额度。NOVELTY=RETAIN0、Charades FINAL_MEDIA_STOP持续。
