# VLM-BATCH-014：工具来源、完整性与隔离收据

2026-10-09。执行基线 main `afd21abd9da1d42a331e913eb81e4981a4bc6eed`。最终结果：`CPU_TOOL=BLOCKED`，唯一包GET发生socket timeout，未部署任何可执行文件，未运行ffprobe。不将来源预检或部分字节当作完整包验证。

## 来源与许可范围

[FFmpeg Windows 下载入口](https://ffmpeg.org/download.html#build-windows)推荐[Gyan.dev 构建](https://www.gyan.dev/ffmpeg/builds/)。FFmpeg项目直接提供源码；本次是第三方Gyan打包的静态x64 release essentials，版本固定9.0.2、GPLv3，不能称为FFmpeg项目直接签名发布的Windows二进制。

固定[包对象](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip)及[发布方checksum](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip.sha256)。冻结SHA-256：`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`。同站checksum一致只能说明发布方校验一致性，不构成独立数字签名或无恶意软件保证。

真实执行已核官网推荐链接、Gyan版本/许可文案，两条动态别名的HEAD Location锁定同一9.0.2对象，固定checksum逐字匹配，包HEAD大小/ZIP类型通过预算前置；没有跟随别名响应正文。GET明确使用`ProxyHandler({})`、默认TLS证书验证和拒绝自动跳转，不使用镜像、代理或latest包。

## 隔离与合成验证

固定根仅为`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe`；实际私人绝对路径不公开。Windows x64/Windows10+、已有祖先规范身份与reparse、已知云同步根、docs/原科研目录及metadata/media兄弟树重合排除、空闲至少1GiB已核。创建新工具根；不覆盖旧工具、不改PATH、Conda、Python、PyTorch、CUDA或旧研究账本。

合成验证保留失败记录：初轮15方法中14 PASS/1 FAIL，揭示已知Content-Length超过剩余累计预算时应在读正文前拒绝；增强预读预算后第二轮15 PASS。首次真实入口在任何网络或新目录创建前因缺失CPU-Tools父目录停止，核实零请求/零ledger；只修正新安装器同一固定树的父目录创建，并增加不覆盖反例。最终16方法全PASS（0 FAIL/ERROR/SKIP，suite 0.470秒），才启动正式网络。此修复没有改变位置或放宽安全边界。

测试只用虚构HTTP/ZIP、mock进程和临时文件，覆盖禁代理/TLS/URL/跳转/编码、长度缺失/欺骗、累计失败预算/持久化、固定SHA/版本、ZIP路径与大小写碰撞/特殊文件/加密/DLL/嵌套/zipbomb/ZIP64/CRC、唯一ffprobe和许可、目标不覆盖、版本异常和超时。

## 最终网络和本地收据

| 项目 | 实际结果 |
|---|---|
| 官网项目页面GET正文 | 27,484 B，COMPLETE |
| Gyan发布页面GET正文 | 52,159 B，COMPLETE |
| 固定checksum GET正文 | 64 B，COMPLETE，与冻结值一致 |
| 唯一工具ZIP GET已读正文 | 13,107,200 B，STOPPED：timeout |
| 全部工具GET正文 | 13,186,907 B / 157,286,400 B硬限 |
| GET / HEAD计数 | 4 / 3；其中工具ZIP GET尝试1、成功完整ZIP 0、重试0 |
| 最终私有文件占用 | 13,107,774 B：部分包13,107,200 B及账本574 B；共2文件 |
| 本地峰值收据 | 精确峰值UNKNOWN；失败发生在首次disk checkpoint之前，ledger初始0不能当峰值0。按部分包单调增长及小于1MiB的原子账本/写检查预留，保守文件字节上界14,155,776 B，低于536,870,912 B硬限；不包含文件系统目录元数据 |
| 完整包SHA / ZIP安全 / 全成员CRC | UNKNOWN / NOT_RUN / NOT_RUN |
| 提取 / ffprobe执行 / 版本 | 0 / 0 / UNKNOWN |
| Authenticode / exe SHA | UNKNOWN_NOT_CHECKED / 不存在可执行文件 |

包HEAD大小/Content-Type与总预算检查已通过后才发起包GET；本轮没有保存HEAD响应大小到最终ledger，因此不提供不可重核的精确HEAD数字。网页“约109MB”是发布方展示值，不是本轮完整包实测大小。

连接在一次持续直连传输中超时；账本将部分正文计入总量并标记STOPPED，部分文件仅留在固定私有工具根，没有改名为完整ZIP、提取或执行。本轮选择零重试，未更换代理/镜像/版本、未清空预算或覆盖文件。后续恢复必须由新的独立父任务先审查既有部分文件和累计额度，不能重跑已回报014或将部分文件当作完整包使用。

新安装器成功路径仅允许唯一ffprobe.exe及关联许可/README白名单、全CRC验证后一次10秒以内`-version`。这些真实阶段本轮未到达；合成测试PASS不证明真实ZIP结构、许可成员、二进制签名或健康检查已通过。

原研究目录、原CSV/ZIP、旧源码与历史结果均未修改；0 Charades请求、Range、视频下载、PTS、视觉解码、GPU、模型、外部联系或后台调度创建。公共仓库仅交本任务两报告、两新标准库代码和一条追加结果，不交包、exe、完整日志、许可全文或私人路径。
