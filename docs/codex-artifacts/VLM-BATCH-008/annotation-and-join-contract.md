# VLM-BATCH-008：标注与join合同（任务3—4）

2026-10-09，main eb2c53f。schema文档审查完成，不等于逐行验证通过。DIRECTLY_SEEN为网页明确陈述；INFERRED为需核验的合同设计；UNKNOWN为资料没有建立的事实。本轮未打开任何标注包或实际标注行。

## 3. 原Charades公开字段与评测语义

依据[官方README](https://prior.allenai.org/projects/data/charades/README.txt)，v1 train/test CSV以逗号分列、含逗号的值可带引号，多值以分号隔开；类表、对象／动词类及映射文件、classification/localization评测文件名称均直接可见。

| 字段／对象 | 证据层级 | 合同与限制 |
|---|---|---|
| id | DIRECTLY_SEEN | 每视频唯一ID；真实唯一性／字节别名未验，不能证明不同人或事件 |
| subject | DIRECTLY_SEEN | 数据集subject唯一标识；不是公开上传者／session／家庭ID映射，更不是原真实身份 |
| scene | DIRECTLY_SEEN | 15室内场景类别；同Kitchen不是同源证明，异场景也不证明不同人 |
| quality/relevance/verified | DIRECTLY_SEEN | 注释者7点质量／脚本相关性、是否符合脚本；不是事件存在／区间准确的oracle |
| script/descriptions | DIRECTLY_SEEN | 拍摄脚本、观察者自由描述，多值；script是计划而非每个动作确实发生，description不是穷尽ground truth |
| actions | DIRECTLY_SEEN | 每动作由class、start、end三元组表示；类标签在独立类表解释。允许多条不证明同类多episode被分别保留 |
| length | DIRECTLY_SEEN | 视频时长，单位秒；2017-02-27 changelog称新增正式时长列。实际媒体同版时长未知 |
| action起止的单位／闭半开约定 | INFERRED／UNKNOWN | length以秒、区间数字与时间定位背景支持秒级解释；本README未单独完整定义actions单位、端点包含或量化误差，不擅自当整数帧号／精确PTS |
| train/test成员 | DIRECTLY_SEEN文件角色；实际映射UNKNOWN | 文件名说明split，不读取成员清单；不证明participant-disjoint或session-disjoint |
| 原始／480p／24fps导帧版本 | DIRECTLY_SEEN处理说明；实际桥接UNKNOWN | README称原媒体编码后保留原分辨率／帧率；提供的RGB另经24fps重采样及缩放，不能把frame序号/24当原视频PTS |

README同时给MATLAB和DictReader例子；MATLAB按列索引取actions的示例与文字字段次序存在潜在不一致，**未来须按实际header验证，不继承数字列索引**。本轮不运行其中代码，公开报告不复制真实样本或例子中的视频身份。

### 官方定位指标不是实例边界指标

README明确classification输出157类视频分数并计算mAP。官方v1 localization输出每个所评时刻的157类分数，评测点为t_j=j·length/25（j=0…24），计算**帧级分类mAP**。网页“localization”命名不代表按全部实例区间做det-mAP／tIoU匹配；官方25点可以漏掉短事件，也不提供重复实例交换率。未来新实例指标需独立定义并与标准检测／检索基线同时报告，不能偷偷改官方脚本后仍称同一指标。

[项目页](https://prior.allenai.org/projects/charades)宣称固定类别的穷尽注释，train由4名、test由8名worker共识；[HCOMP正式摘要](https://ojs.aaai.org/index.php/HCOMP/article/view/13290)描述多标签询问／共识及不完美worker。**这些是注释协议声明，不是任意事件不存在、每类所有episode准确切分或任意ordinal真值的证书**。没有真实包就不能验证重复、缺失、倒序、超界、同类合并或边界一致性。

## 4. STA与动作区间的有条件join

[作者README](https://github.com/jiyanggao/TALL)直接给格式：video name、start、end，再以##接sentence。文字格式可解析不等于与原id同名、同媒体时钟、同split和同revision已验证。原动作interval是固定类事件；STA interval是句子描述的moment，可能涵盖多个动作、对象或持续阶段，不能一对一等同。

| 必要步骤 | 要冻结的无答案合同 | 本轮状态 |
|---|---|---|
| 版本固定 | 原CSV/类表/媒体各revision与SHA；STA clean/original以及文件SHA分别记录 | 网页README revision可记录，真实包／外链版本UNKNOWN |
| ID join | 显式namespace、video name到id映射；只按经证实的后缀规则规范化，拒多对多碰撞 | schema名称不同，实际一一关系UNKNOWN；不默认去后缀即可连接 |
| split join | 保存两资源原split角色与来源组，核缺失／跨split重复；未知HOLD | 名称train/test可见，成员和相容性UNKNOWN |
| 时间join | 注释单位、clip原点、媒体stream/time_base、start/end约定、转码／裁剪映射与误差 | 未读取实际媒体，全部真实桥接UNKNOWN；不得自动平移／钳位 |
| 语义join | 句子target、固定类别、actor/object、可支持的事件实例分别标类型；重叠不是语义等价 | 需明确且合法的参考关系；纯IoU高不能认证句子与动作同一事件 |
| 失败与隔离 | 原始行ordinal只在受控评分侧；构造／歧义／冲突／缺失单列，完整planned分母保留 | 仅设计；未建manifest或读取任何答案 |

TOY SCHEMA ONLY（文字，无实际行）：原字段可表示`video_key / class / [s,e] / revision`；STA为`video_name / [u,v] / sentence / clean_revision`。只有已核映射f(video_name)=video_key且两区间同一坐标域，才可计算区间关系；即使关系可算，也不能推出句子target等于class或所有同类实例已标全。本轮没有生成toy脚本或伪造统计。

不得从未标区间造全局negative；不得把同类第二条直接命名“第二次”；不得为了join改写sentence后仍称官方STA标签；缺少权利或语义参考时STA保持HOLD。未来可以先审原CSV元数据完整性，不能借此解封STA权利、视频或模型调用。

结论：原schema文档层可读，**SCHEMA初筛条件PASS，实际parser／数据一致性UNKNOWN；STA join、真实时钟、clean version与ordinal可辨识性UNKNOWN**。0注释获取、样本读取、真实视频处理或代码执行。
