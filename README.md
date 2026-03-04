# 🧠 Fluid Memory

> 🧬 流体认知记忆架构 - 你的赛博大脑

**inspired by 艾宾浩斯遗忘曲线 + MemGPT + OpenClaw**

[English](./README_EN.md) | [中文](./README.md)

---

## 🌟 特性

- **🔄 动态遗忘**: 不是所有记忆都要永远记住。权重低的记忆会被自动遗忘。
- **⚡ 语义理解**: 基于 ChromaDB 向量检索，理解"饮料"="可乐"。
- **💪 强化机制**: 被检索次数越多的记忆，越难被遗忘。
- **🌙 梦境模式**: 每天自动整理大脑，归档低价值记忆。
- **🔌 OpenClaw Ready**: 开箱即用的 OpenClaw Skill。

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Fluid Memory Core                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
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
│                              │                             │
│                              ▼                             │
│                      ┌─────────────┐                       │
│                      │   梦境守护   │                       │
│                      │  Maintenance│                       │
│                      └─────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧪 核心算法

### 流体评分公式

$$ Score = (相似度 \times e^{-\lambda \times t}) + \alpha \times \log(1 + N) $$

其中：
- $\lambda$ (lambda): 遗忘速率
- $t$: 距离上次访问的天数
- $\alpha$ (alpha): 强化系数
- $N$: 被访问(检索)的次数

**原理**：
- 越久没被提及的记忆，分数越低
- 越常被检索的记忆，分数越高

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- chromadb
- openai (可选，用于 embedding)

### 安装

```bash
# 克隆仓库
git clone https://github.com/AgaintA/fluid-memory.git
cd fluid-memory

# 安装依赖
pip install -r requirements.txt
```

### 使用

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

#### 4. 启动梦境守护 (每天自动整理)

```bash
python dream_daemon.py
```

---

## 📁 项目结构

```
fluid-memory/
├── SKILL.md              # OpenClaw Skill 定义
├── fluid_skill.py       # 核心引擎
├── maintenance.py       # 梦境整理脚本
├── dream_daemon.py    # 定时守护进程
├── wrapper.py         # CLI 封装
├── config.yaml        # 配置文件
├── LICENSE            # MIT 许可证
└── README.md          # 本文件
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License - see [LICENSE](./LICENSE) file.

---

## 🙏 致谢

- [ChromaDB](https://www.trychroma.com/) - 向量存储
- [OpenClaw](https://github.com/openclaw/openclaw) - AI Agent 框架
- 艾宾浩斯遗忘曲线 - 理论基石

---

**Made with 💕 by Aga & Rin**
