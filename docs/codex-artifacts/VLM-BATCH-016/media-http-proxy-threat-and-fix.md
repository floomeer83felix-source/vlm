# VLM-BATCH-016：媒体HTTP代理威胁与代码修复

2026-10-10。基线main `c6a3149`；独立docs checkout干净并安全fast-forward，唯一READY=016、无既有016回报。仅源码/合成验证，未访问任何真实研究HTTP端点、工具或数据隔离树。

## 原风险与完整请求路径

旧`RangeClient.__init__`调用`urllib.request.build_opener(NoRedirect())`。没有显式ProxyHandler时urllib会补充默认代理处理器，可能调用getproxies并读取环境/Windows系统代理。因此固定URL、最终域名一致、TLS与禁止重定向不能单独证明没有Python代理继承。本轮没有读取实际代理配置值。

| 路径 | 原调用与修复后覆盖 |
|---|---|
| 官网项目页GET | `RangeClient.text(PAGE,…)`，用于官方480p媒体锚点；统一安全opener与fixed_request |
| 许可文本GET | `RangeClient.text(LICENSE,…)`；同一安全opener与fixed_request，原许可SHA校验不变 |
| 固定媒体ZIP HEAD | `run_pilot`中的`client.opener.open(…)`；继续使用同一实例，增加fixed_request的HEAD精确来源门 |
| 全部媒体Range GET | `RangeClient.get`；尾部、ZIP64记录、central、本地头及两成员内容均经此方法，同一安全opener与fixed_request |

官网文本仅精确允许`https://prior.allenai.org/projects/charades`和`https://prior.allenai.org/projects/data/charades/license.txt`的GET；媒体仅精确允许`https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip`的HEAD及有明确起止Range/If-Range的GET。HTTP降级、其它域/路径/查询参数、错误方法和媒体整包GET构造均拒绝；没有新增目标、镜像、备用opener或urlopen路径。

## 最小修复与证据

新增唯一`build_media_opener()`，显式`ProxyHandler({})`，`ssl.create_default_context()`并检查check_hostname/CERT_REQUIRED，HTTPSHandler使用该context，NoRedirect禁止跳转。对当前Python缺失的308处理别名显式复用302处理器，最终仍在redirect_request中拒绝且不读响应正文。新增`fixed_request()`统一精确URL/方法和identity请求编码；所有三个网络open调用点均使用其构造请求，不改变原预算/时钟/选择流程。

静态AST审查确认协调器内只有一个build_opener构造、一个Request构造（集中在fixed_request）、无urlopen备用入口；RangeClient和run_pilot均使用共享opener。合成测试污染大小写HTTP_PROXY/HTTPS_PROXY及ALL_PROXY，并把getproxies、getproxies_registry、getproxies_environment mock为异常，构造安全客户端时三者均未调用；没有读取Windows真实代理值。TLS默认验证和不安全context拒绝、301/302/307/308拒绝、合法四路径共享实例、非法URL/方法/响应读前停止均有反例。

既有206精确Content-Range/长度/ETag、identity、错误最终URL、200停止与失败累计记账保留。这里的代码级禁代理结论仅针对本协调器受控请求路径，不是实时服务器、系统网络路由或TLS对端证据。

## 未扩大修复边界及残余门

AST比较原全部常量完全一致；原函数/类仅NoRedirect、RangeClient与run_pilot有上述网络入口差异，其余均未变。64MiB网络/128MiB媒体本地/GET上限12/两例选择、旧源SHA、隔离路径、ZIP/CRC逻辑、ffprobe参数和时钟公式未改。原27项测试方法的AST也完全保留，新增13项。

工具查找和默认预检流程仍会先调用一次ffprobe版本，再在execute分支检查父任务；本轮没有调用该真实入口。历史父任务守卫仍检查单READY、已回报及README关键字，并不等价于解析完整许可语义，不能将本次代码任务READY视为媒体执行批准。原媒体账本仍采用读取后累计add，本轮没有移植015工具续传器的读前保守预留或升级断电计费保证；后续媒体验证任务须独立审查执行门和记账边界。这些均如实保留，未借代理修复放宽或改写原协议。

`MEDIA_CLIENT_PROXY_POLICY=CODE_LEVEL_VERIFIED`；真实媒体206/时钟/取样安全仍UNKNOWN或HOLD。无真实服务器请求/视频访问/ffprobe/GPU/模型，未修改旧工具包、私有账本、Conda或原研究环境。
