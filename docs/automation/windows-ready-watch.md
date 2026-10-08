# Windows 低额度 READY 任务监控（每30分钟）

本方案**不创建新Codex聊天，也不在无新任务时调用Codex模型**。系统任务计划程序启动纯PowerShell+Git脚本，检查GitHub `main` 是否出现**唯一且尚未回报的READY任务**。只有检测到新任务，才写本地提示；用户随后在**现有Codex聊天**发送一条继续指令，Codex才真正执行该任务。

## 组件与限制

- GitHub任务板：[../next-steps.md](../next-steps.md)；结果记录：[../codex-results.md](../codex-results.md)；Codex行为规则：[../../AGENTS.md](../../AGENTS.md)。
- 低成本检查脚本：[`../../tools/watch-ready-task.ps1`](../../tools/watch-ready-task.ps1)（仅运行本机已有Git/PowerShell；不使用Codex额度）。
- 执行周期：由 Windows **任务计划程序（Task Scheduler）**每30分钟运行一次；此定时任务必须在用户本地Windows电脑建立，我们无法从GitHub远程安装。
- **无法自动发送一条消息到已打开的Codex桌面聊天。** 当前仅支持发现新READY并写本地提示。不要宣传为自动执行。Codex原生thread automation可以返回同一聊天，但每次30分钟检查仍可能用模型额度，无法保证本地Git检查“免费且唤醒现有聊天”。
- ChatGPT已经设置约每小时尝试审核新Codex结果并写新计划的任务；两者周期不对齐，最多需要等待下一轮检查。自动更新发生后必须看GitHub commit才能确认。

## 一、首次在Windows运行并验证（不需要GPU）

先让Codex在**原来的同一个聊天框中**确认**GitHub文档仓库独立checkout**的路径。它可能不同于非Git的本地RTX3090实验目录。这里的例子仅是示意：

```powershell
$DocsRepo = "D:\Research\vlm-docs"
& "$DocsRepo\tools\watch-ready-task.ps1" -DocsRepo $DocsRepo -DryRun
```

`-DryRun`不会修改本地任务通知状态，但会执行必要的只读远端Git获取（`git fetch origin main`更新本地远端跟踪元数据，**不切换当前分支、不覆盖文件、不推送**）。输出说明：

- `NEW_READY_TASK <任务ID>`：存在未交付的唯一READY任务；不会自动启动Codex。
- `NO_NEW_TASK`：没有未交付READY任务。
- `ALREADY_NOTIFIED`：本机此前已为这一任务发过一次提示。
- 出错时退出码2且不授权执行：远端不是目标仓库、无法访问、多个READY、任务文件格式异常或状态损坏。

正式运行时省略 `-DryRun`。首次检测到新任务会在本机用户目录内写两个小型文件：

```text
%LOCALAPPDATA%\VLMResearch\TaskWatch\pending-task.txt
%LOCALAPPDATA%\VLMResearch\TaskWatch\last-notified.json
```

这只是私人本地提示与去重状态，不上传GitHub，不涉及GPU/视频/模型。已经提醒过的同一任务ID不会重复提醒；当任务结果文件出现对应 `### <任务ID> ...` 标题时，检测器视为已有回报，不再提示。删除缓存或改动READY状态可能重置提醒，**不意味着允许重复实验**，所以Codex仍必须重新核对结果/账本。

## 二、设置30分钟 Windows 计划任务（手动一次）

1. Windows 搜索并打开**任务计划程序** → “创建任务”；名称 `VLM Ready Watch`。普通用户权限即可；选 **“仅当用户登录时运行”**，不要设置为最高权限。
2. “触发器” → 新建 → 每天一次 → **重复任务间隔30分钟，持续时间：无限期**（若Windows版本菜单不同，选择最长可用持续时间并续期）。
3. “操作” → 启动程序 → 程序：`powershell.exe`；参数（替换两处路径为真实文档checkout路径）：
   ```text
   -NoProfile -NonInteractive -ExecutionPolicy RemoteSigned -File "D:\Research\vlm-docs\tools\watch-ready-task.ps1" -DocsRepo "D:\Research\vlm-docs"
   ```
4. “条件”中根据偏好选择 AC电源策略；电脑关机/休眠或GitHub不可访问时无法检查。允许任务在电脑联网时运行。
5. 在任务计划程序右键运行一次，使用 `%LOCALAPPDATA%\VLMResearch\TaskWatch\pending-task.txt` 确认结果；若没有新任务，正常不会出现新提示文件。错误查看任务历史/PowerShell退出码，不要强行重试或放行GPU。

**不要**让这段脚本以管理员权限运行，也不要将本地实验工作区设成 `-DocsRepo`。

## 三、用户怎样继续使用原Codex聊天

检测到新READY时，本机 `pending-task.txt` 会出现任务ID。随后在已经使用的同一个Codex聊天中发送：

> 继续下一轮：安全刷新独立GitHub文档仓库main，重新读取AGENTS.md、docs/next-steps.md、docs/codex-results.md；只执行尚未完成的唯一READY任务，并按任务说明上传脱敏报告后停止。不创建新聊天。

Codex必须重新验证远端任务的READY状态和对应结果是否已经存在；不能仅凭本地通知文件执行，更不能重新运行已开始的GPU前向。

## 四、想实现“自动执行，不需要我发送消息”怎么办？

此要求与“保持**现有桌面Codex聊天**、**无新任务完全不耗Codex额度**”目前不能同时得到保证：

- **省额度优先（当前方案）**：Windows纯Git每30分钟检查 → 仅新任务写本地通知 → 用户在同一个Codex聊天发一句继续；无新任务不消耗Codex额度。
- **全自动优先**：使用Codex桌面版的**thread automation**，定时回到同一个聊天检查并执行；但每次唤醒通常仍可能消耗模型额度，且自动审批/文件/网络权限、机器开机、应用运行等需实际配置和实测。尤其不能擅自授权GPU实验或敏感数据下载。
- **CLI独立执行**：可以由系统任务计划程序在检测到新任务后调用某个非交互Codex CLI执行命令，但不保证接入**当前桌面聊天线程**，且权限/失败恢复/额度、重复执行危险更高；未经专门设计和明确授权，本仓库没有提供此实现。

## 五、安全边界与维护

- 监控脚本只做 `git fetch`、`git show`、本地私有提示文件；它不写GitHub、不执行任务、不创建Issue、不启动Codex/GPU。
- 唯一可信READY状态为**最新远端main**；脚本只按`next-steps.md`表格中的第三列状态判断，并核对`codex-results.md`中是否有对应任务标题。文档格式一旦变化，应重新测试脚本后再启用计划任务。
- `last-notified.json`用于防重复提示，不是实验账本，不足以取代Codex任务/模型调用的write-ahead持久记录。
- 启用后先观察一次 `-DryRun` 和一次正式运行的结果，确认没有误报再让它长期运行。
- 当前唯一READY任务及GPU运行许可**以最新仓库任务书为准**。项目维持“一个Codex聊天、一个READY任务、一个完成提交”的协作约定。
