# HourVideo 等待期：本地开发集资格检查与实验入口（2026-10-10）

本页是**已经落地的离线检查工具使用说明**，不是新一轮静态审查父任务。Ego4D协议根据用户提供的Dropbox Sign成功画面**已签署、官方数据凭据仍未证实到达**；Ego4D和HourVideo访问条件分开，不能相互替代。**当前READY=0，GPU=未授权本轮启动，媒体/模型下载=0，NOVELTY=RETAIN0**。

## 已从官方可公开页面确认

1. [HourVideo官方GitHub README](https://github.com/keshik6/HourVideo)：2025-03-06声明发放带答案的development标注；开发集作者计数50视频/1182道选择题/39.3小时，整库500个20–120分钟来自Ego4D。HourVideo benchmark数据**严禁进入训练corpora**；带答案标注包含作者canary，不得修改/移除。
2. [HourVideo官方HF数据卡](https://huggingface.co/datasets/HourVideo/HourVideo/blob/main/README.md)公开一个按`video_uid`分组的纸面示例结构：`video_metadata.duration_in_seconds`、`benchmark_dataset`、`qid`、`question`、`mcq_test`、`correct_answer_label`。其旧段落仍注明`dev_v1.0.json`无答案、`samples_v1.0.json`有答案，不能凭它推断后来发布的`dev_v1.0_annotations.json`的**实际行级字段/有效答案数/每视频至少两题**已核实。
3. [HourVideo官方HF gated入口](https://huggingface.co/datasets/HourVideo/HourVideo/tree/main)可以公开看到文件目录但访问数据文件需用户登录同意共享联系信息等条款。HF卡片的Apache-2.0标记不能覆盖上游Ego4D视频许可或HourVideo特定基准使用限制。**本项目没有在本轮通过HF gate、打开题目/答案文件或取得原视频。**

## 已备好的可执行工具

[离线Python检查脚本](../tools/hourvideo_dev_preflight.py)只用Python标准库，默认不联网、不开GPU、不访问视频、不安装依赖、不读取任何未显式指定的路径。设计为**用户日后另行同意HF条款并合法获得开发集文件后**，验证标注纸面字段、时长、答案标签、同视频至少两道可评分问题、12个不同视频以及其中至少四段≥30min的**标注层候选数量**。不会上传受保护题目、答案、视频ID、个体时间戳；公开标准输出只显示聚合数字。该脚本并不验证视频实际存在、许可、Ego4D同版本、帧/PTS或独立性，不能将`ANNOTATION_ONLY_CANDIDATE`提升成实验GO。真实文件的字段若与公开示例不同，必须先修订适配器，不推断缺失正确标签。

如果你要在**独立公有文档checkout**中运行工具自身的**完全虚构合成数据自检**（不使用真实数据）：

```powershell
python -B tools/hourvideo_dev_preflight.py --self-test
```

**在用户本人完成HourVideo gate并明确允许本机受限标注读取以后**，才能对私有本地文件执行以下命令；所有数据源路径和选择结果都必须位于**独立私有目录**而非Git/GitHub，保护canary、题目/标准答案和video UID：

```powershell
python -B tools/hourvideo_dev_preflight.py --annotations "X:\\PRIVATE_DATA\\dev_v1.0_annotations.json" --private-selection "X:\\PRIVATE_RUN\\hourvideo-selection-private.json" --public-report "X:\\PRIVATE_RUN\\hourvideo-aggregate-only.json"
```

上述路径只是虚构占位符，不意味着本机存在该文件；父目录须已存在，工具不会覆盖现有结果。**不要**把真实`dev_v1.0_annotations.json`、任何真实示例/题目/答案/选择UID、签署协议、Ego4D AWS凭据或HF Token提交到公有仓库。合成自检输出并不证明真实标注已取得或格式兼容。

## 直接影响实验的决策

- 合法标注读后只有`ANNOTATION_ONLY_CANDIDATE`：下一步仍须核具体Ego4D官方批准+凭据、每个候选UID的同版真实可用视频以及本地3090锁/环境；与原先REAL-PILOT-001`SAFE_STOP`是**不同数据来源的新审批**，旧48次预算不可直接复活。
- 若字段不符、无正确答案或不足12视频/24题：`ANNOTATION_PREFLIGHT_BLOCKED`，先不要下载Ego4D视频。只在**开发集**做模型比较，test无GT的500视频不当本地正确率数据。
- 对HourVideo基准，严格**只评估、不训练或蒸馏/反馈调参泄露标准答案**。模型回答应以`mcq_test`作为可见选项；`correct_answer_label`只能在独立评分侧访问，选帧检索器看不到它。
- 时间评测不等于问答评测：QA正确率可用标签评分，但不能从正确答案声称已验证事件真值、原始PTS或精确定位。

**下一件需要用户自行完成的事**：前往[官方HF HourVideo页面](https://huggingface.co/datasets/HourVideo/HourVideo)阅读并按意愿接受该数据集的访问条件。Ego4D邮件审核/访问凭据可同时等待；无需发送账号、数据或任何凭据给ChatGPT。收到HF可访问的确认后告知即可。
