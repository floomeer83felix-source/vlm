# VLM-BATCH-015｜固定 Gyan 9.0.2 部分 ZIP 的同源 HTTP 206 断点续传与独立 ffprobe 就绪核验

**2026-10-10。用户已明确选择“继续安全断点续传方向”，并授权在 GitHub 制定新的有限任务。仅当 `docs/next-steps.md` 中 VLM-BATCH-015 为唯一 READY，且用户在**原 Codex 聊天框**主动下达执行指令时运行。**
已结束的 `VLM-BATCH-014`（[6bec3ab](https://github.com/floomeer83felix-source/vlm/commit/6bec3ab3e7e41571b8878e30c36b26ca710fd060)）不得重跑或重写。此前工具安装授权仍仅适用固定独立 CPU 工具树；此次**新批准的是在原额度内有条件续传同一工具包**，不是追加150MiB额度，更**不是**额外媒体下载授权。

## 0. 当前真实证据的边界与不可重置预算

前一批公开的执行者收据（不是ChatGPT独立读取Windows）：
- 固定Gyan来源：`https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-9.0.2-essentials_build.zip`，发布方同站SHA-256 `60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`。这是发布者SHA，并非官方FFmpeg直接签名；不能从同站校验文本通过推出部分文件正确。
- 原所有工具GET正文累计 **13,186,907 B**；旧包GET已读 **13,107,200 B** 后socket timeout；4 GET/3 HEAD，完整包成功0、重试0、`ffprobe`未安装；私有部分包+ledger报告共13,107,774B，精确峰值未知。总工具GET上限 **157,286,400 B**，尚余严格上限 **144,099,493 B**；不能另开新额度、漏记1-byte 206探测/失败/校验文本等正文。ZIP加上未来任何新GET只有在总预算内才能完整。新媒体预算独立，**当前媒体GET必须为0**。
- 固定原私有根仅：`%LOCALAPPDATA%\VLM-Research-Isolated\CPU-Tools\ffprobe\`；预期**已存在**`incoming/ffmpeg-9.0.2.zip.part`（13,107,200B）及`local-audit/tool-ledger.json`（报告574B）。原始文件的**SHA256未在公开收据冻结**，原第一次工具HEAD的ETag、精确Content-Length也**未持久化证明**。因此绝不能声称“本地part和远端同一ETag已验证”。下列步骤必须在原Windows上重新、独立核实；如果无法达到强ETag/范围/最终发布方SHA三层证据就STOP。
- FFmpeg官方只提供源码并指向[Gyan.dev Windows二进制构建](https://ffmpeg.org/download.html#build-windows)；Gyan[发布页](https://www.gyan.dev/ffmpeg/builds/)截至2026-10-10仍展示9.0.2 release essentials ZIP约109MB及同站校验链接，但该展示**不是实际HTTP HEAD大小/Range支持证明**。

## 硬边界与资源

- **只在上述已经存在的CPU工具树做追加式续传和经校验的最小提取**，绝不改原科研工作区/原Conda/CUDA/PATH、系统注册表/驱动、Charades metadata/video目录、Git checkout外其他路径、云同步目录。原part与原ledger不可覆盖/删除/改写历史字节；仅通过追加已认证的远端后缀改变原part（见步骤5）。旧ledger始终**只读**，新续传ledger以原账本为父在同一个`local-audit/`下**独立、独占创建**，持久记录累积账本、来源HEAD/strong ETag/Range/预留字节、实际收到及失败。不得更换目录逃避冲突。
- **全部014+015工具GET正文合计≤150MiB (157,286,400B)**；新轮独立GET在前项账本通过审查后可用的额度不超过**144,099,493B**，包含206探测、续传正文及失败已读字节，**0自动重试**。新轮真实包GET至多**2次**（1次≤4KiB的强ETag匹配及部分文件内容探测，1次`Range: bytes=13107200-(N-1)`后缀续传）。HEAD上限2次，不需要重新GET官方网页/checksum；若监管需要额外GET则STOP而不是扩大请求数。HTTP/ZIP CRC等校验不应额外联网。
- 原项目工具**本地磁盘全部文件合计≤512MiB (536,870,912B)**，CPU Tools同盘空闲≥1GiB；复制/硬链接/单成员提取的瞬时峰值应提前按上界计入，超过STOP。不能下载全新包、换latest、第三方镜像、走代理、安装7zip/choco/winget/pip、超时后私下重复GET。
- 唯一调用外部exe为本轮白名单提取后的固定`bin/ffprobe.exe -version`（最多1次、≤10秒）；禁止读取视频、Charades、真实PTS、图像、音频、GPU、模型运行。013媒体客户端代理安全HOLD；本轮不编辑、不执行原媒体脚本。

## 十项执行协议（可失败的真实一次性续接，不是重复前批）

**1. 任务与历史真值门**：安全fast-forward独立Git文档checkout；读`AGENTS.md`、`docs/next-steps.md`、`docs/codex-results.md`、本README、[014两报告](../VLM-BATCH-014/tool-source-integrity-and-isolation.md)、[014安装器](../../../prototypes/isolated_ffprobe_installer.py)。确认唯一READY=015、此前014已有最终结果且**015无既有结果**、Git工作树洁净，否则STOP。任何事实与原收据不符不得把收据当实地核验。
**2. 先本地原part与原ledger只读审计**：固定路径物理身份/no reparse/no cloud/原环境重合、x64、空闲≥1GiB；原part必须普通单文件且恰好13,107,200 B、以`PK\x03\x04`开头，私有原ledger必须真实存在且能解析、`body_bytes=13,186,907`、`get_attempts=4`、`head_attempts=3`、`successful_zip_gets=0`，events总字节相符、PACKAGE最后STOPPED且read13,107,200B；新部分文件hash可**只存本地**。若ledger缺项/损坏/同时存在其它旧续传账本/part与ledger冲突、工具已经安装或额外旧资产，**STOP，0HTTP**。不得改旧ledger或“初始化新账本为0”。
**3. 纯合成前置测试**：先构造新的独立`prototypes/isolated_ffprobe_resumer.py`和合成测试，stdlib且默认`--preflight`；`--resume`必须核唯一015父任务和旧014历史，不通过不能访问网络。合成tests覆盖代理污染禁用、无跳转/TLS、206/200/416、Content-Range/length/ETag/If-Range、弱ETag拒绝、part本地改写/不匹配、旧ledger不重写/余额继承、crash前预记预算、chunk超限、range偏移、partial文件预检、同源对象变更、sha最终不符绝不安装、ZIP/CRC/白名单/ZIP64/许可、exe已存在拒绝、`-version`失败和0 Charades请求。至少**18个**纯合成unittest一次全PASS**之后**才能发真实HEAD/GET；只在synthetic阶段修新代码，不靠真实网络错误临时扩权/切源。
**4. 同一固定对象的HEAD资格**：显式`urllib.request.ProxyHandler({})`+TLS默认证书核验+NoRedirect，唯一URL为上文已冻结的Gyan9.0.2 ZIP。最多2 HEAD（必要时复核稳定性），**不下载网页内容**；必须精确HTTPS URL、不允许301/302跨站/无声跳转、`Content-Length=N>13,107,200`且≤150MiB预算可涵盖、类型与ZIP一致、**强且带引号、非`W/`的ETag**在两次独立HEAD中一致（若仅1次HEAD也必须随206响应确认不变）。没有ETag/弱ETag、变化、长度矛盾、不可辨识来源→`BLOCKED_REMOTE_IDENTITY`并停止，无探测GET。**前一批未保存ETag**，所以该新强ETag只能证明*本次HEAD/后续206对象稳定*，不能追溯保证第一次13MB属于同对象；此缺口只能通过**最终完整ZIP与冻结发布方SHA256完全一致**补足，绝不在未核完整ZIP时“修好部分包”。
**5. 严格小量206探测，再一次后缀Range续传**：先以**独立计费的≤4KiB GET**请求原part某个已冻结边界字节（建议`13107199-13107199`）并逐字比对；响应必须真实`206`、精确`Content-Range: bytes s-e/N`、同强ETag、`Content-Encoding=identity`、`Content-Length`精确且读取不超额；返回`200`整包**不读取正文立即STOP**。接下来先算`N-13107200`是否小于等于旧额度剩余扣除探测正文及保留误差；预留/持久化再发**唯一一次**`Range: bytes=13107200-(N-1)`，加`If-Range: <strong ETag>`；仍需实际206，HTTP200/416、源转移、ETag/长度变化即停止不读响应体。新ledger要从旧`body_bytes`和事件和GET次数**继承只增不减**；每个后续读取chunk，**在read之前原子持久预留全chunk上限**（或等价断电保守计费）后再读取/写入part，单块≤64KiB，防止超额与丢失账本。不得因socket read timeout再尝试第2次后缀GET，不改包URL或私自延长次数；保留原part/审计/新ledger供下一决定，不自动清理。
**6. 网络后完整SHA最终验真**：若且仅若完整后缀已按HEAD的N长度取得，核part完整SHA256恰为冻结发布方`60f467265b1e312373dbcd92200c2618a74850f98d3d078e94296bb3fa2047ba`，文件总N、ZIP签名均符合；**完整SHA失败→`BLOCKED_INTEGRITY`、绝对不执行/提取/更换内容/请求新ZIP**。同时才认证原13,107,200B与补全字节最终组成同一发布者文件。公告中不能提供私有part指纹/真实用户路径。
**7. 仅原协议白名单部署**：SHA成功之后用014已审的`safe_tool_members`/标准库`zipfile`核路径/单一目标/GPL许可证、ZIP中央目录CRC`testzip`和展开大小，总用量预留；只允许独占创建`bin/ffprobe.exe`及所需许可文件，禁止`extractall`、覆盖其它旧文件、触碰旧项目或安装系统软件。如ZIP布局/多exe/依赖DLL/签名无法支持，`BLOCKED_ARCHIVE`并保存完整ZIP不运行。私有原part和历史账本在本轮不得删除；如额外硬链接/复制将超过512MiB则STOP。
**8. CPU版本只读**：最多一次运行固定根下的`ffprobe.exe -version`，限时10秒，不传视频/模型URL，要求返回0和9.0.2版本（不据此宣称供应链数字签名）。生成exe文件SHA、版本留在私有审计，公共报告仅输出版本/是否对应固定发布方SHA。**绝不调用媒体`-show_packets`**。
**9. 双账本与脱敏风险审计**：原014账本/旧part在恢复前只读冻结摘要；新续传账本载明父统计数、请求/预留/已读、HEAD ETag（只在私有本机，不公开可逆地址/指纹）、原part起始长度、最终ZIP SHA检验、磁盘峰值，允许公开的是旧固定消耗、**本轮新GET累计**、两轮合计及`GET`次数和STOP类别。普通报告不得包含Windows用户名、原视频ID、原本机具体路径、代理设置、会话密钥、精确媒体时长，任何工具ZIP/EXE均不得上传。若崩溃、ledger未完整持久化或计量不可信就`BLOCKED_ACCOUNTING`并停止；不得从0重新开始，更不得重做015。
**10. 独立裁决**：`TOOL_RANGE_SUPPORT=VERIFIED_206 / BLOCKED / UNKNOWN`；`CPU_TOOL=AVAILABLE_PUBLISHER_HASH_VERIFIED / BLOCKED`；媒体端`PROXY_HOLD`、`V1_MEDIA_ACCESS=NOT_RUN`、B/C科学真值HOLD、创新retain0/GPU BLOCKED。不因有ffprobe即自动启动媒体013或任何视频V1；成功push即STOP并等待ChatGPT审查。若任何条件失败，不允许第三次GET/镜像/重试、新工具或媒体，报告原因即可。

## 仅5处GitHub交付，严格匿名化

1. `docs/codex-artifacts/VLM-BATCH-015/local-part-ledger-and-remote-identity.md`：用户Windows上的part/014ledger是否真实吻合、原预算/本次HTTP HEAD/206/强ETag状态、累计资源、不可辨识处与安全阻塞。
2. `docs/codex-artifacts/VLM-BATCH-015/resume-integrity-install-and-science-decision.md`：完整SHA/ZIP CRC/最小ffprobe安装健康检查、代理门仍HOLD/科学真值不变、只有类别化异常与真实最小资源摘要。
3. `prototypes/isolated_ffprobe_resumer.py`：纯stdlib硬编码9.0.2与旧私有根、继续读取旧ledger但绝不重置、全预算上限/强ETag+206/If-Range、先合成后真传输，默认本地只读预检、真正执行必须`--resume`并核015唯一READY/014历史结果；只调用ffprobe -version，不能抓媒体。
4. `prototypes/test_isolated_ffprobe_resumer.py`：≥18项纯合成unittest，假HTTP/ZIP/路径与断电记账，0网络/真实用户媒体。
5. `docs/codex-results.md`末尾仅追加**一条**`### VLM-BATCH-015 ...`，10项的DONE/STOP/UNKNOWN、之前与本轮正文/本地最大实际字节、Range状态、ffprobe健康检查、0 Charades请求/0GPU。

**严禁**提交ZIP/EXE/原本地ledger/视频/来源身份/秘密，或更改014旧脚本/旧合成用例/老报告/`docs/next-steps.md`/`docs/research-overview.md`、原研究环境/conda/PATH/用户文件/旧CSV/视频。公共Git docs干净、安全fast-forward后单次普通push；冲突STOP不force push。任何源端协议、计费或ZIP不符→STOP并交BLOCKED收据，不能为了取得一个工具不断追加无边界批次。此任务只发生在用户**原持续Codex聊天**中；ChatGPT目前没有读取其Windows本地part/ledger，也未验证Gyan的实时ETag/206，不得把READY当已完成。
