# DEMAND来源与许可核验

来源：Joachim Thiemann、Nobutaka Ito、Emmanuel Vincent，DEMAND，Zenodo记录1227121，https://zenodo.org/records/1227121 ，核验日期2026-11-08。

## 当前官方信息存在冲突

- Zenodo API metadata.license.id 为 cc-by-4.0，原始响应保存于zenodo_record.json。
- 同一记录的Description写CC BY-SA 3.0。
- 官方随附DEMAND.pdf开头和第5节也写CC BY-SA 3.0；PDF的MD5已与官方文件清单核对。

因此不能只保留API的CC BY 4.0字段，也不能声称官方已经给出单一无歧义许可。保留原始文档、原署名和BY-SA告示，在最终README记录上述差异；公开分发原始/派生音频前应厘清适用许可。当前核验不替原作者重新许可。

## 下载与完整性范围

官方清单实际含18个环境，17个有16kHz ZIP，SCAFE只有48kHz ZIP。本次固定ch01，SCAFE用scipy.signal.resample_poly转换到16kHz。为避免下载全部多通道数据，通过HTTP Range获取官方ZIP中央目录和ch01压缩成员；每个成员均验证ZIP CRC32，原始WAV另记SHA256。没有下载完整ZIP，所以没有声称完整ZIP的MD5已验证；官方ZIP校验值仅作为来源元数据保存。

分析16kHz WAV另记文件SHA256和解码后float32样本SHA256，区分音频变化与WAV文件头创建时间变化。其余通道不视作额外独立来源。
