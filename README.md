# 🧠 Fluid Memory

> 流体认知记忆架构 - 你的赛博大脑

Inspired by 艾宾浩斯遗忘曲线 + OpenClaw

---

## 特性

- **🧠 自动学习**: 每次对话自动记录（需启用 Hook）
- **🔄 动态遗忘**: 权重低的记忆会被自动淡化
- **⚡ 语义理解**: 基于 ChromaDB 向量检索
- **💪 强化机制**: 被检索次数越多的记忆，越难被遗忘
- **🔌 OpenClaw Ready**: 开箱即用的 OpenClaw Skill + Hook

---

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Fluid Memory Core                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐  │
│  │   植入      │ ──> │   向量存储   │ ──> │   检索      │  │
│  │  Remember  │     │  ChromaDB  │     │   Recall   │  │
│  └─────────────┘     └─────────────┘     └─────────────┘  │
│         │                                         │         │
│         │            ┌─────────────┐              │         │
│         └──────────>│  流体公式    │<─────────────┘         │
│                      │   Score     │                       │
│                      │ = Sim*Decay │                       │
│                      │    + Boost  │                       │
│                      └─────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 遗忘机制

Fluid Memory 有 3 种遗忘方式：

### 1. 动态遗忘（检索时过滤）

每次检索记忆时，用**流体评分公式**计算每条记忆的得分：

```
Score = (相似度 × e^(-λt)) + α × log(1+N)
```

| 参数 | 值 | 含义 |
|------|-----|------|
| λ (lambda) | 0.05 | 遗忘速度 |
| t | - | 距离上次访问的天数 |
| α (alpha) | 0.2 | 强化力度 |
| N | - | 被访问(检索)的次数 |

**低于 0.05 分的记忆会被过滤掉**，不返回给用户。

### 2. 主动遗忘（手动）

用户说「忘记xxx」时，调用 `forget` 命令，将记忆的 `status` 改为 `archive`（软删除）。

### 3. 梦境守护（定时归档）

运行 `maintenance.py` 或 `dream_daemon.py`，定时扫描所有活跃记忆：

```
base_score = e^(-λt) + α × log(1+N)
```

**低于 0.15 分的会自动归档**。

---

## 核心算法

### 流体评分公式

```
Score = (相似度 × e^(-λ × t)) + α × log(1 + N)
```

- λ (lambda): 遗忘速率
- t: 距离上次访问的天数
- α (alpha): 强化系数
- N: 被访问(检索)的次数

---

## 环境要求

- Python 3.8+
- chromadb
- pyyaml

---

## 安装

```bash
# 克隆仓库
git clone https://github.com/AgaintA/fluid-memory.git
cd fluid-memory

# 安装依赖
pip install chromadb pyyaml
```

---

## 使用

### 配置文件 (config.yaml)

```yaml
decay_rate: 0.05   # 遗忘速度
boost_factor: 0.2  # 强化力度
auto_learn: true   # 自动学习模式
summarize_threshold: 3  # 多少轮对话后自动总结
```

### 命令行

#### 1. 植入记忆

```bash
python fluid_skill.py remember --content "用户喜欢喝可乐"
```

#### 2. 检索记忆

```bash
python fluid_skill.py recall --query "用户喝什么"
```

#### 3. 遗忘记忆

```bash
python fluid_skill.py forget --content "青椒肉丝"
```

#### 4. 多轮对话总结

```bash
python fluid_skill.py summarize --conversation "用户说xxx | 我回复xxx | 用户说xxx"
```

#### 5. 增量总结（推荐）

```bash
python fluid_skill.py increment_summarize --conversation "用户说xxx | 我回复xxx"
```

#### 6. 查看状态

```bash
python fluid_skill.py status
```

---

## Hook 自动同步

支持 OpenClaw Hook，监听 `message:sent` 事件自动记录对话。

### 安装 Hook

```bash
# 复制 hook 到 OpenClaw hooks 目录
cp -r hooks/fluid-memory-sync ~/.openclaw/hooks/
```

### 配置

在 `openclaw.json` 中启用：

```json
{
  "hooks": {
    "internal": {
      "entries": {
        "fluid-memory-sync": {
          "enabled": true
        }
      }
    }
  }
}
```

---

## 项目结构

```
fluid-memory/
├── SKILL.md                    # OpenClaw Skill 定义
├── fluid_skill.py              # 核心引擎
├── maintenance.py              # 梦境整理脚本
├── dream_daemon.py             # 定时守护进程
├── wrapper.py                  # CLI 封装
├── config.yaml                # 配置文件
├── LICENSE                    # MIT 许可证
├── README.md                  # 本文件
└── hooks/
    └── fluid-memory-sync/      # 自动同步 Hook
        ├── HOOK.md
        └── handler.js
```

---

## 许可证

MIT License - see [LICENSE](./LICENSE) file.

---

## 致谢

- [ChromaDB](https://www.trychroma.com/) - 向量存储
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
- 艾宾浩斯遗忘曲线 - 理论基石

---

Made with 💕 by Aga
