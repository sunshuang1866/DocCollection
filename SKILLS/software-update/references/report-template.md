# Report Template

Use this template to generate the final markdown report. Replace all `<...>` placeholders with actual values. Omit sections that have no data (e.g., omit "Base OS 版本" table if no version info was found).

```markdown
# <Repo Name> <时间段>更新汇总

> 数据来源：<repo-url>
> 统计周期：<时间段>
> 合并 PR 总数：**<N> 个**

## 概览

| 类型 | 数量 | 涉及软件 |
|---|---|---|
| 新增镜像 | <N> | <software list> |
| 自动升级 | <N> | <software list> |
| 其他 | <N> | <software list> |

**涉及 Base OS 版本**（如适用）：

| Base OS 版本 | 涉及 PR 数量 |
|---|---|
| <os-version> | <N> |

## 软件更新清单（按分类）

### <Category> 类

| 软件 | 新版本 | Base OS 版本 | PR | 类型 |
|---|---|---|---|---|
| <software> | <version> | <base-os-version> | <pr-ref> | <type> |

## 重要说明

- **新增镜像**：<highlight key new images added this period>

*文档生成时间：<YYYY-MM-DD>*
```

## Field Reference

| Placeholder | Source |
|---|---|
| `<Repo Name>` | Last path segment of repo URL |
| `<时间段>` | User-provided period (e.g., `2025年2月`) |
| `<repo-url>` | Full repository URL (GitHub or GitCode) |
| `<N>` | Counted from subagent data |
| `<software list>` | Comma-separated software names for that type |
| `<base-os-version>` | Normalized uppercase (e.g., `24.03-lts-sp3` → `24.03-LTS-SP3`) |
| `<pr-ref>` | `#NNNN` for GitHub, `!NNNN` for GitCode |
| `<type>` | 新增镜像 / 自动升级 / 其他 |

## Platform Notes

| Platform | PR ref format | Merge commit subject pattern |
|---|---|---|
| GitHub | `#NNNN` | `Merge pull request #NNNN from ...` |
| GitCode | `!NNNN` | `Merge branch '...' into '...' !NNNN` or subject contains `!NNNN` |
