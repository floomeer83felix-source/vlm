# 角色差分实证稿重构

2026-11-03用户同意按[可行性评估](../../../research-decisions/empirical-publication-feasibility-2026-11-03.md)恢复一次稿件重构。此次由负责人直接完成，不增加科研任务编号；旧稿与原实验记录保留，不新增训练、模型调用、原始数据或私有缓存读取。

- [正文Markdown](manuscript.md)
- [可编辑Word](manuscript.docx)
- [审阅PDF](manuscript.pdf)
- [补充材料与完整计数](supplement.md)
- [公开聚合表图数据](tables.json)
- [投稿前信息](submission-readiness.md)
- [重建脚本](build_document.py)

正文限定于固定冻结特征接口上的角色视图相对效应。063来源四格5.00%到17.67%、068新条目1.33%到12.33%及负向划分同时保留；项目20%门失败，不认新算法或独立来源泛化。后续强对照和多事件失败作为边界，不反向否定早期普通C已经能拟合训练的事实。

重建仅需公开仓库数据、Python的matplotlib和python-docx及pandoc。先运行build_document.py生成原生Word公式、两表和两图，再用文档渲染器导出PDF核查。中文排版使用Noto Serif CJK SC公开字体，字体文件不随仓库上传；用户可替换为当地学报要求的合法中文字体。页面与图表检查摘要见[revision-summary.json](revision-summary.json)。

历史069是已暂停的旧执行合同，本次新写作授权不恢复其执行READY，也不恢复083或实验配方。稿件完成后仅进入作者审阅和选刊，不自动投稿。
