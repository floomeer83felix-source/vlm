# Ego4D 许可申请与“现成标注→科研问题”准入清单

**记录：2026-10-09｜状态：USER WILLING TO REVIEW / NOT SUBMITTED / NOT LICENSED。** 用户已表示愿意亲自通过Ego4D官方渠道审阅并在认可条款后接受协议。这**不**是已签署许可、不代表ChatGPT/Codex可以替用户提交表单或使用数据；本文件不记录姓名、邮箱、住址、机构或AWS凭据。

## 1. 唯一优先入口与官方事实

- 官方[Start Here](https://ego4d-data.org/docs/start-here/)明确：获取数据或任何标注之前，须先审阅并接受数据许可；审核后约48小时通过邮箱收到AWS凭据（官网描述的通常时间，非保证）。许可可由个人或有正式权限的机构签署人签署。授权凭据约14天有效，超期可续期。
- 现行[个人/机构Ego4D许可表](https://ego4ddataset.com/ego4d-license/)：表单生成正式 data usage agreement，后续通过HelloSign邮件签署；页面提供[协议草案](http://ego4d.github.io/pdfs/Ego4D-Licenses-Draft.pdf)。**应以签署时正式最终条款为准，不以草案/研究总结代替法律审阅。**
- 不混用Ego-Exo4D的不同许可表。仓库[MIT许可证](https://github.com/facebookresearch/Ego4d)主要覆盖代码；**不能推导为视频/标注开放MIT**。
- 官方[Episodic Memory benchmark](https://ego4d-data.org/docs/benchmarks/episodic-memory/)定义MQ（活动的所有发生时间窗口）和NLQ（可见/可推断答案的时间窗口）；[annotation schemas](https://ego4d-data.org/docs/data/annotations-schemas/)含video_uid、clip_uid、clip/video相对时间、活动label和版本等字段。公共文档中的秒值和frame号**尚不能单独证明实际媒体PTS、版本与来源独立性**。
- 官方说明整个数据规模是TB量级，不允许把申请等同于批准下载，更不能启动full_scale全量下载。是否允许存储、计算、匿名汇总发表、衍生特征处理、校内共享等，**必须由用户读正式协议自行判断**。
- 2026年2—4月官方GitHub [issue列表](https://github.com/facebookresearch/Ego4d/issues)可见用户报告表单500/成功无邮件/审查迟迟未回等问题；它们是外部故障报告，**不证明用户也必遭同样问题**。若出现故障，只记录状态，用户自行决定通过官方支持渠道沟通，ChatGPT/Codex不得自动发Issue/邮件。

## 2. 用户自行处理的流程（唯一待执行动作）

1. 打开Ego4D [许可申请表](https://ego4ddataset.com/ego4d-license/)；选择Individual，或仅在本身是机构正式授权签署人时选Organization。
2. 个人审阅正式协议：研究/非商业范围、可否发布聚合评估结果、隐私保密、派生数据/权重与下载存储/删除、是否允许共享及机构/伦理审批。存在不确定条款时，先不签，咨询单位负责人员。
3. 仅在同意完整条款后，**用户本人**填写个人信息、收HelloSign邮件并签署；查看邮箱/垃圾邮件的签署及审批状态。
4. 返回聊天时**只报告一个脱敏状态**：`未提交/已提交待审批/已获批准/条款不接受/表单异常`；**不要**贴协议里个人资料、AWS keys、邮箱/地址、签署表单或私人标签。不能把“已提交”改写成“已批准”。
5. 获批准后由ChatGPT重新审查用户自报授权范围；**未经另行授权仍不得使用凭据/下载任何数据或变更本地环境**，待提出最小数据子集方案与存储路径后才申请批准。

## 3. 科研资源匹配门（授权后也必须单独完成）

**候选问题**：同一长视频中重复活动实例造成的时间实例混淆是否呈系统性偏差、而非单纯问句内容相关性差异？当前仅有可检验现象，不是新算法。需先做强先例去重（时间动作定位、密集活动实例消歧、long-tail event retrieval、NLQ/MQ/egocentric grounding）；若先例已给同可识别目标，标REPLICATION/NO-GO。

- **数据准入**：协议研究/发表权限→目标split与annotation revision→合法视频与标签匹配→clip/video同版时钟/真实PTS→保守独立来源组→预定分母/泄漏排除。
- **标注效力**：MQ活动起止区间可验证**已标注的正例实例、时间定位/混淆**；不可证明所有视频中未标注活动都不存在、感知器完全覆盖或全世界否定事实。NLQ标注为可回答时间窗口，不能偷换成负事实oracle。
- **独立评分**：使用正确答案/事件真值仅由终态评分器读取，不给模型选择策略/调参器；首次法定授权后的实际视频处理、CPU解码、GPU、公开衍生数据或人工标注**逐项另请用户批准**。
- **资源止损**：先用公开schema确定能否定义不泄露标签的输入和是否有足够源；若没有可验证的增量科学贡献或实际授权缺失，则STOP，而不再硬造连续10个文献/toy任务。

## 4. GitHub与Codex交接边界

更新[任务看板](./next-steps.md)与[总览](./research-overview.md)仅记录用户**愿意审阅签署**和唯一待执行的人类动作。**不建立新的READY Codex批次、不发邮件、不代签、不登录网站、不配置AWS、不下载标注或视频、不变更原Windows工作区**。旧BATCH-007已ACCEPTED且机制retain0，旧VLM-003/004仍BLOCKED。收到用户脱敏审批状态后才决定是否制定下一批安全、有实质新增证据的工作。
