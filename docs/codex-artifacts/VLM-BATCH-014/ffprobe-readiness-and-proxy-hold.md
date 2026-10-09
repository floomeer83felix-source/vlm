# VLM-BATCH-014：ffprobe就绪与媒体代理门

2026-10-09。最终执行收据：工具获取因直连socket timeout安全停止，没有部署ffprobe；未执行旧媒体任务。

## 独立工具门

`CPU_TOOL=BLOCKED`。仅请求固定Gyan9.0.2发布包，来源和发布方checksum预检已通过，唯一包GET在13,107,200 B部分正文后超时。总工具正文13,186,907 B，0完整包、0重试、0提取、0 ffprobe调用。完整包SHA、真实ZIP/CRC、版本、exe SHA与签名均UNKNOWN；没有可用CPU工具入口。[详细资源和隔离收据](tool-source-integrity-and-isolation.md)保留测试失败/修复和真实初始化停止的完整简史。

未来成功也只能认证发布方hash范围内的CPU工具和无媒体版本健康检查，不认证媒体服务或科学真值。当前只保留私有部分包与账本，后续安装恢复需新的限定任务，不自动再次GET、不重置累计额度、不覆盖原树。安装器默认只预检，存在工具根即拒绝，因此本轮源码不提供未经审查的断点恢复路径。

## 旧媒体客户端静态风险

只读AST审查[旧媒体协调器](../../../prototypes/charades_range_media_clock_pilot.py)第132行：`urllib.request.build_opener(NoRedirect())`，没有显式`ProxyHandler({})`。读取已有Python标准库实现表明build_opener会补充默认ProxyHandler；其缺省构造调用getproxies，因此可能继承环境或Windows系统代理。未读取实际代理值、未执行旧客户端、未请求媒体、未修改旧源码。

URL白名单、默认TLS和NoRedirect本身不能证明直连。旧客户端经同一opener取得的媒体Range和来源文本均受此风险影响；新安装器的禁代理合成测试只验证安装器，不替旧媒体代码背书。

`MEDIA_NETWORK_CLIENT_PROXY=HOLD`。建议下一独立父任务显式构造`ProxyHandler({})`、保留TLS/源白名单和拒绝跳转；先用被污染的代理环境/模拟Windows代理来源构造合成反例，证明getproxies不会被调用、请求不经过代理，再审查端到端预算与父任务防重复门。本轮不修旧代码、不自动重启013/013-FIX或放行媒体。

## 科研边界

`V1_MEDIA_ACCESS=NOT_RUN`；视频GET与媒体Range均0，0实际packet PTS、视频/动作人工核验。既有A评测兼容性限域结论不扩大，时间区间质量B和P1/P2事件真值C继续HOLD；创新RETAIN 0，Charades自然长域缺口不变，GPU BLOCKED。工具就绪不得被解释为已验证媒体时钟、原始端点正确或事件实例真值。

| 任务书步骤 | 最终状态 |
|---|---|
| 1 独立文档仓库、单READY、无重复回报 | DONE |
| 2 固定Windows路径、规范身份、权限与空间 | DONE |
| 3 官方推荐/第三方许可/固定checksum | DONE；完整二进制完整性UNKNOWN |
| 4 合成安全逻辑先测 | DONE；最终16 PASS，0 FAIL/ERROR/SKIP |
| 5 唯一固定工具包GET | BLOCKED_TIMEOUT；部分正文计入预算，无重试 |
| 6 真实ZIP/白名单/全CRC | UNKNOWN_NOT_RUN；没有完整包 |
| 7 仅一次版本健康检查 | BLOCKED_PRECONDITION；实际调用0 |
| 8 旧客户端代理问题静态审查 | DONE；MEDIA_NETWORK_CLIENT_PROXY=HOLD |
| 9 资源/脱敏审查 | DONE；实际正文和最终占用可重核，精确峰值UNKNOWN，保守上界公开 |
| 10 工具/媒体/科学分门决定 | DONE；CPU_TOOL BLOCKED、媒体NOT_RUN、B/C HOLD、RETAIN 0、GPU BLOCKED |

建议ChatGPT先审查下载超时及固定私有部分文件/累计预算的恢复边界，再决定是否建立下一工具父任务；媒体客户端代理修复仍需独立授权和合成回归，不因工具源网页或合成用例PASS解除媒体门。本轮报告不提出新研究算法或科学成功结论。
