# 长程智能体研究资料

本目录整理《Towards Long-Horizon Agents: A Survey》和配套仓库的中文研究笔记，并把综述中的开放方向转成可执行的问题清单。

- [综述详细总结](01_综述详细总结.md)：按 Foundation、Evolution、Harness、Optimization、Application、Frontier 六部分解释论文的概念、方法、边界和批判性阅读要点。
- [亟需解决的问题与研究机会](02_亟需解决的问题与研究机会.md)：结合仓库条目和 2025–2026 年代表性工作，给出 P0/P1 优先级、研究假设、实验设计与验收指标。
- [仓库地图与研究方案](03_仓库地图与研究方案.md)：说明仓库结构、数量统计、代表性资源、证据强度和建议的选题路线。
- [检索与证据记录](04_检索与证据记录.md)：记录来源、版本、抓取日期、统计脚本和使用限制。
- [场景、数据合成、质量判准与训练路线](05_场景数据合成_质量判准与训练路线.md)：回答 terminal、computer use、writing 等场景如何采集/合成数据、怎样校准 judge、怎样训练；逐项对照已有工作提出六个待验证缺口。附 [原始来源阅读记录](data/synthesis_evidence.md)。

## 来源与版本

- 综述：Guanting Dong 等，*Towards Long-Horizon Agents: A Survey*，预印本 DOI [10.20944/preprints202607.1328.v1](https://doi.org/10.20944/preprints202607.1328.v1)，本地 PDF：`../long-horizon-1/sources/Towards_Long_Horizon_Agents_A_Survey.pdf`。
- 配套仓库：[RUC-NLPIR/Awesome-Long-Horizon-Agents](https://github.com/RUC-NLPIR/Awesome-Long-Horizon-Agents)，固定快照 commit `084cafe83e3d10814ae0b63329bd10aa5945fd97`，访问日期 2026-09-10。
- 本地快照数据：`../long-horizon-1/data/repository_catalog.csv`、`catalog_stats.json`、`primary_evidence.json`。仓库会继续更新，文中的数量只对上述 commit 有效。

## 如何使用

先阅读综述总结建立 H1/H2/H3 和“模型 + harness”的共同框架，再用问题清单选择研究问题，最后按仓库地图中的 benchmark 组合做受控实验。统计数字用于描述覆盖面，不能替代论文复现或统一排行榜。
