# VLM-BATCH-016：纯合成回归与科学门

2026-10-10。仅代码修复，不执行媒体试点。交付两报告、媒体协调器和合成测试修改、Codex结果一次追加；计划、总体总结、013/014/015历史报告及工具代码不改。

## 可审查测试收据

现有conda pytorch中的Python只运行`-B -m unittest discover -s prototypes -p test_charades_range_media_clock_pilot.py -v`，不安装或更新库，不import PyTorch/CUDA。原27个方法保留，新增13个，总40项。

| 次序 | 真实合成suite结果 |
|---|---|
| 首轮 | 40方法：38 PASS、1 FAIL、1 ERROR、0 SKIP；suite3.605秒 |
| 修复 | ERROR是当前Python未提供308处理别名；补显式拒绝。FAIL是新增空响应头夹具的`headers or default`误补默认头；改为仅None才用默认头，保留拒绝断言 |
| 最终一轮 | 40 PASS、0 FAIL/ERROR/SKIP；suite3.724秒，不含Python启动 |

所有方法的setUp对未mock的OpenerDirector.open、urlopen、socket.create_connection和subprocess.run设置异常防护；测试只用io.BytesIO、虚构ZIP/MP4字节、mock ffprobe输出和合成临时目录。原协调器mock流程也保留，不启动真实execute或无参数预检命令。假的代理地址/人物/成员/时长仅用于反例，不是用户资产。

新增覆盖：环境代理污染及Windows代理发现函数不调用、TLS验证/不安全context、301/302/307/308读前拒绝、精确HTTPS源/方法与禁整包GET、四路径共享opener、200/416/源跳转、文本跳转/编码/缺失长度/超额/未知源、失败已读预算不重置、已完成013即便仍READY也拒绝、静态无备用网络入口。原27项继续覆盖206/范围/ETag、跨失败预算、12请求/磁盘限额、ZIP64/路径/CRC/zipbomb/两例、工具与时钟mock及隐私。

## 八项任务裁决

| 步骤 | 结果 |
|---|---|
| 1 入口与历史 | DONE：main c6a3149安全同步，唯一016 READY且无结果；读AGENTS/任务书/结果/013合同/原媒体代码与测试 |
| 2 静态威胁 | DONE：项目页、许可GET、S3 HEAD和所有Range共享默认代理风险；不读真实代理设置 |
| 3 最小修复 | DONE：唯一禁代理/TLS/NoRedirect构造，四路径统一精确请求门；无新增URL或预算放宽 |
| 4 合成回归 | DONE：最终40 PASS，原27方法AST不改，新增13方法 |
| 5 非执行约束 | DONE：仅静态与受防护合成测试，0真实ffprobe/研究HTTP/媒体；未运行真实preflight/execute |
| 6 差异审查 | DONE：原常量、非网络函数/类、样本选择、隔离、时钟、ffprobe命令和旧账本规则不变 |
| 7 五处交付 | DONE：两脱敏报告、两允许源码修改、一条结果追加；不交真实日志/映射/数据/工具 |
| 8 裁决与停止 | CODE_LEVEL_VERIFIED；真实媒体UNKNOWN/NOT_RUN，科学门HOLD；正常push后停止 |

研究HTTP计数均0：项目/许可GET、媒体HEAD/Range GET、Gyan工具GET；正文0 B、真实媒体文件0、真实ffprobe调用0、PTS/视觉解码/人工核验/GPU/模型均0。GitHub文档同步与交付Git通信属于用户授权的仓库交接，不作为研究HTTP探测。未读取或修改工具隔离资产/旧工具账本/原CSV或ZIP/原科研目录/Conda/PATH/系统代理；合成临时对象由测试标准库创建并回收，不是受保护资产。

## 门状态与下一轮边界

`MEDIA_CLIENT_PROXY_POLICY=CODE_LEVEL_VERIFIED`；`REAL_MEDIA_RANGE_206=UNKNOWN`；`V1_MEDIA_ACCESS=NOT_RUN`；`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED_BY_BATCH015_REPORT`，本轮未重核工具。A沿012限域结论；B时间质量/C事件实例真值HOLD、自然长视频单独数据适用性FAIL、创新RETAIN 0、GPU BLOCKED。

这次验证只关闭Python代理继承的代码层漏洞，不验证真实S3206、媒体ZIP实际结构、媒体时钟或事件真值。默认预检会调用ffprobe、父任务许可门是关键字检查、媒体账本读后记账等既有边界见[静态威胁报告](media-http-proxy-threat-and-fix.md)。是否安排独立真实媒体父任务由ChatGPT审查；本轮不创建下一READY、不自动启动旧013或任何真实请求，保留同一聊天。
