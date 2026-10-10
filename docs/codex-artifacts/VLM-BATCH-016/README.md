# VLM-BATCH-016｜Charades媒体Range客户端禁代理与纯合成安全回归（代码修复，不准真实媒体）

**2026-10-10。** 这是[已验收BATCH-015工具部署](../VLM-BATCH-015/resume-integrity-install-and-science-decision.md)之后的**唯一新安全代码父任务**，仅当`docs/next-steps.md`明确`VLM-BATCH-016=READY`且用户主动在**原持续Codex聊天**发起时可执行。用户已批准将来条件式最多2段官方Charades 480p视频/媒体GET正文≤64MiB/本地媒体≤128MiB/仅CPU packet-PTS的V1科学试点，但**本BATCH-016仅改源码、测虚构网络和视频**。**本轮允许的真实媒体GET/HEAD、FFmpeg工具GET、ZIP访问、视频字节访问和CPU ffprobe调用全部为0；即使修复成功也不得运行V1**。原BATCH013、013-FIX、014、015已交付，不得重跑、更改旧报告或重新下载。

## 科学状态及修复对象

- BATCH015执行者报告固定发布方SHA`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`完整校验，通过受限ZIP/CRC且本机独立CPU `ffprobe -version`返回0、版本9.0.2。ChatGPT仅审查GitHub报告/源码，没有独立访问Windows重测。`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED`；**原媒体客户端安全仍HOLD**。
- 原`prototypes/charades_range_media_clock_pilot.py`的`RangeClient.__init__`当前使用`urllib.request.build_opener(NoRedirect())`。这个写法可自动安装默认`ProxyHandler`，继承Windows系统或环境中的HTTPS代理。原Charades媒体协议明确禁止代理/镜像/静默重定向。因此修改`RangeClient`且所有媒体协调器HEAD与Range请求必须**显式**同一禁代理opener，例如`urllib.request.build_opener(urllib.request.ProxyHandler({}),urllib.request.HTTPSHandler(context=ssl.create_default_context()),NoRedirect())`（注意Python handler正确性与不接受任意HTTP URL）；真实请求只能是固定原官方S3对象`https://ai2-public-datasets.s3-us-west-2.amazonaws.com/charades/Charades_v1_480.zip`，不因测试/参数增加其他源。
- `A_OFFICIAL_FRAME_LABEL`旧012限域验证；`B_TIME_BOUNDARY_QUALITY=HOLD`、`C_P1/P2_EVENT_TRUTH=HOLD`、`LONGVIDEO_AS_ONLY_DATA=FAIL`、`ORIGINAL_NOVELTY=RETAIN0`。禁代理单测PASS不能宣称真实206支持或视频时钟正确。

## 顺序执行的八项硬任务

**1. 公共文档 checkout和安全入口**：先安全fast-forward GitHub main，重读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[原BATCH013任务](../VLM-BATCH-013/README.md)、原`prototypes/charades_range_media_clock_pilot.py`和`test_charades_range_media_clock_pilot.py`。必须只有016 READY，且结果中未有任何`### VLM-BATCH-016`父结果。checkout脏/冲突/重复结果即STOP，无任何网络/源文件修改。
**2. 静态威胁模型**：逐一审查媒体脚本里会触发urllib的全部真实路径，包括官网anchor的任何页面GET、固定S3 ZIP的HEAD和Range、重定向处理、Content-Range/ETag、内容编码、预算/账本、工具查找。报告已发现的默认代理继承路径与其它同类漏点。禁止把“最终域名相同”当作“未走代理”证明。不得读取或公开Windows用户代理配置值。
**3. 最小安全代码修复**：仅编辑`prototypes/charades_range_media_clock_pilot.py`，增加唯一专用、显式禁代理且强TLS/禁跳转的urllib opener构建函数，全部真实媒体网络请求包括官网项目页的许可/anchor文档GET统一使用**同一安全客户端策略**，固定HTTPS官方域、URL/方法白名单，不复用可继承默认ProxyHandler的备用opener、`urlopen`/外部requests/浏览器。若官方项目页和S3媒体锚点是不同合法域，须分别精确列白名单并拒绝新增目标或静默跳域，不读未知响应正文。**禁止更改原保守预算、12次Range GET、媒体2段/64MiB/128MiB、下载独立路径、P1/P2样本冻结、功能计算/ffprobe命令/旧家族dataset准入。**
**4. 纯合成网络安全回归**：仅编辑原`prototypes/test_charades_range_media_clock_pilot.py`，为显式`ProxyHandler({})`、污染`HTTPS_PROXY/HTTP_PROXY/ALL_PROXY`环境、Windows系统`urllib.request.getproxies`被mock为异常、TLS默认证书核验/拒绝301,302,307,308、HTTP降级、官方锚点/固定媒体URL白名单、共享opener的HEAD及Range、失败无正文读取/预算不重置、已完成013不能重跑等补上反例。所有HTTP模拟`io.BytesIO`，媒体MP4和ffprobe输出均**合成/mock**，测试**不得**访问Gyan/AllenAI/Charades服务器/真实Windows视频。最终不少于**30个**纯合成`unittest`方法全PASS且0SKIP，且必须保留此前27项既有测试；新增测例如漏掉其它真实网络路径不能称全部修好。
**5. 非执行路径验证**：允许`python -B -m unittest prototypes/test_charades_range_media_clock_pilot.py`或等价的纯合成命令，仅CPU；也可不带`--execute`地调用媒体程序预检，但既有预检可能运行真实ffprobe `-version`，**本轮更严：禁止任何ffprobe执行，因此只准纯合成测试与静态审查**。`run_pilot(execute=True)`、自定义parent、任何服务HEAD/GET、任何视频/ZIP来源访问均禁。
**6. 原边界差异审查**：用`git diff`确认只修网络opener/精确客户端安全及对应合成用例，旧Charades元数据规则、原014/015工具代码、科研workspace与私有目录不改。任何测试需要放宽域、启用代理/重定向、源或预算才通过就STOP，报告`BLOCKED_SOURCE_POLICY`。
**7. 五处公开匿名交付**：严格只允许(1)`docs/codex-artifacts/VLM-BATCH-016/media-http-proxy-threat-and-fix.md`（漏洞路径/安全策略/合成证据）；(2)`docs/codex-artifacts/VLM-BATCH-016/code-only-test-and-science-gate.md`（>30测试收据、0HTTP/0媒体/0ffprobe、原仍HOLD）；(3)以上旧媒体脚本；(4)以上旧合成测试；(5)`docs/codex-results.md`尾部追加恰好一条`### VLM-BATCH-016 ...`。不能把原视频ID、subject、源映射、私有路径/系统代理、真实PTS、任何媒体ZIP、exe、已授权用户数据或个别动作例写进Git。
**8. 完成后裁决与STOP**：`MEDIA_CLIENT_PROXY_POLICY=CODE_LEVEL_VERIFIED / HOLD`；`REAL_MEDIA_RANGE_206=UNKNOWN`；`V1_MEDIA_ACCESS=NOT_RUN`；`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED_BY_BATCH015_REPORT`而非本次重新验证；B/C HOLD、GPU BLOCKED、创新retain0。只有静态+合成验证，不能升级为“真实媒体安全全部PASS”或自动创建017/启动013；完成仅允许一次正常push到main（不force、不PR、不到用户原研究树），随后保留原Codex聊天等待ChatGPT科学审核。

## 无需新增权限的范围与失败门

用户此前允许媒体≤2段的V1，但本批**主动采用更窄的代码修复范围，不消费那份媒体授权**。不能用本README绕过原013父任务已结案守卫。任何执行门不满足都STOP并仅报告；不下载Charades、Gyan或新的数据集、不启动真实ffprobe/视频容器/解码、CUDA/Conda/GPU/模型/视频帧/人脸/音频、也不修改Windows系统代理或PATH。
