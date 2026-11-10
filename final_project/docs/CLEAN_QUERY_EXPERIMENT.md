# 已完成的 Clean-query 补充实验

## 直接查看

项目主目录的 **final_project.mlx** 是唯一主入口：第 1–24 节保留原有分析，第 25 节为干净查询补充实验，第 26 节为最终总结。原主结果表和全部 20 张保存图均保留。旧版主文件与独立补充文件已完整归档，位置见项目根目录的 MERGE_RECEIPT.json。

直接打开主文件，查看第 25–26 节的保存结果即可，无需重新运行。完整 Run All 会按当前运行重新计算 Clean 检查；清空变量后单独执行第 25 节则只读取保存结果。

## 主要结果

每组均为 60 genuine / 600 external trials；共同阈值固定为 **0.270078811669524**。

| 干净输入处理 | EER % | FAR % | FRR % | BER % | False accepts / 600 |
|---|---:|---:|---:|---:|---:|
| Clean reference | 0.000 | 2.500 | 0.000 | 1.250 | 15 |
| Clean → 默认 SS | 0.167 | 4.000 | 0.000 | 2.000 | 24 |
| Clean → DeepFilterNet | 0.000 | 3.000 | 0.000 | 1.500 | 18 |
| 仅重采样（接口对照） | 0.000 | 2.833 | 0.000 | 1.417 | 17 |
| PCM16 adapter（接口对照） | 0.000 | 2.833 | 0.000 | 1.417 | 17 |

EER 由分数阈值扫描得到，FAR/FRR/BER 使用固定开发阈值。因此 EER 为 0 与固定阈值下 15 次误接受并不矛盾。本样本中干净 genuine/external 分数可以分开，但沿用的 Noisy-development 阈值并不在零错误的分隔区间。

默认 SS 的 EER 0.167% 是原始插值 EER 定义的结果，**不是一条 genuine 的 1.667% FRR 步长**。不要把“插值 EER 分辨率”与 FRR 的最小计数步长混同。

## 这次具体做了什么

- 从当前完成 run 中选择 90 条唯一测试查询，保留原始 5 秒裁剪、16 kHz、去均值与混合前峰值 0.7。
- 沿用原导出链：共同 gain=0.5、PCM24，所以 clean 的模型输入峰值约 0.35。Clean 输入文件 SHA256 与主运行已嵌入的文件相同；不是新裁剪、重新选取或另加峰值归一化。
- 20 条主注册录音保持原样；没有把测试语音当注册语音，也未使用备用注册集。
- 从本次提供的 `final_project.mlx` 提取原 MATLAB STFT、iSTFT、percentile PSD、谱减增益与验证指标函数。
- Clean→SS 仍用 α=1.5、β=0.02，让原估计器自己从输入估计噪声；没有把真噪声设置为 0 来人为制造恒等处理。
- DeepFilterNet 沿用固定模型/可执行文件、48 kHz 接口、padding、延迟补偿和 16 kHz 输出；附带原重采样和 PCM16 接口对照。
- 重新提取 470 个 embedding（20 注册 + 90 Clean + 90 SS + 90 DFN + 90 重采样 + 90 adapter），避免只依赖旧缓存。110 个原 clean/注册 embedding 与缓存的最大绝对差异为 0。
- 对模型文件逐项验证 SHA256；用原 MATLAB 指标函数交叉核对五组结果，Python/MATLAB 最大差异为 **0 个百分点**。
- 由原缓存重算主 Noisy、SS、DeepFilterNet 的 EER，分别复现 7.083333%、8.763889%、9.027778%。没有调整阈值，也没有把干净语音复制 12 次。

## 如何解释

Clean EER 为 0，主 Noisy EER 为 7.083%，可报告本测试设计下的描述性增加 7.083 个百分点。Clean 只有 60/600 trials，主结果有 720/7200，并有不同噪声条件权重；不能把这个差值当新增显著性结论，也不能套用原四项预先声明比较的 bootstrap 区间。

默认 SS 在本样本上的干净 EER 和 BER 均有所增加。DeepFilterNet 的干净 EER 没增加，但 BER 增加 0.250 个百分点，即误接受净增加 3 次；接口对照本身也净增 2 次。不能从如此少量、相关的比较中声称“已经证明神经网络伪影导致主实验退化”，也不能因 EER 相同而声称完全无损。

## 报告如何补

`results/report/sections/clean_query.tex` 是可插入的短节和独立表。建议放在主结果讨论之后，不把 Clean 的较小试验集悄悄合并成主表的同等精度行。按当前报告的标签定位主结果，不依赖口头所说 Table 2/3 的编号。

报告若有以下局限句：

> A clean-query verification baseline was not part of the primary summary, so the report does not quantify the full error change from clean to noisy speech.

应删除或替换成下面的事实说明，避免和新增实验矛盾：

> The supplementary clean-query reference uses 60 genuine and 600 external-impostor trials. Its smaller query set and different condition weighting limit direct comparison with the pooled noisy results.

主报告中“one fixed ECAPA model”“20 enrolled / 10 external speakers”“no causal mechanism identified”等局限继续保留。摘要和结论不必为一个补充结果大幅重写。当前任务没有替换你的原报告文件；补充内容可独立核对后插入。

## 视频如何补

见 **docs/VIDEO_ADDENDUM.md**。只补录一个约 45–70 秒的小段即可，严格按“MATLAB 停留画面 → 讲稿 → 下个画面 → 讲稿”编排。这里不要求你重录已有视频。

## 文件

- `results/tables/clean_query/clean_query_summary.csv`：五组结果与计数、分数范围。
- `results/tables/clean_query/clean_query_trials.csv`：每组 660 次真实评分及判决、相对 Clean 的分数变化。
- `results/tables/clean_query/paired_decision_changes.csv`：Clean→各处理的正确/错误转换。
- `results/tables/clean_query/metric_check.mat`：MATLAB 可直接读取的全部 trial scores 和标签。
- `results/audits/clean_query/analysis_audit.json`、`results/audits/clean_query/matlab_validation.json`：输入、计数、复现与指标核对。
- `results/audits/clean_query/provenance.json`：原 MLX、embedding 与提取 helper 的哈希来源。
- `results/figures/clean_score_distributions.pdf/png`：模型分数分布图。
- `src/scripts/clean_query/` 与 `src/matlab/clean_query/`：小实验复算入口，不运行原主实验。

完整模型推理日志、生成音频与 embedding 保留在本地工作目录：

`/Users/zhangchenxin/Documents/ChatGPT/elec5305 2/outputs/clean_query_supplement_20261110/experiment`

## 在当前电脑重新算这组小实验

使用新的输出目录，避免覆盖本次结果。以下命令只读现有 completed run；它不会重新生成 1,080 条主测试混合：

```sh
'/Users/zhangchenxin/Documents/ChatGPT/elec5305 2/.venv-speaker/bin/python' src/scripts/clean_query/reproduce.py \
  --project '/Users/zhangchenxin/Documents/ELEC5305/final_project/final project' \
  --run '/Users/zhangchenxin/Documents/ELEC5305/final_project/final project/runs/experiment_en_tp498abfc3_ace1_447e_96e9_2010c85be3ff' \
  --output '/Users/zhangchenxin/Documents/ChatGPT/elec5305 2/outputs/clean_query_supplement_20261110/repeat_01' \
  --python '/Users/zhangchenxin/Documents/ChatGPT/elec5305 2/.venv-speaker/bin/python'
```

这需要现有本地模型、完整 run 与 MATLAB 工具箱。查看保存结果不需要模型或 Python。所有处理在本机完成，没有上传资料。
