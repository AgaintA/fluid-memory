---
name: fluid-memory
description: 基于流体认知架构的记忆系统。特点：会遗忘、需强化、懂语义。支持Hook自动同步。
command-dispatch: tool
---

# Fluid Memory Skill

这是你的「赛博大脑」。它不是死板的数据库，而是一个活着的系统——会遗忘不重要的事，会强化常被提及的知识。

## 自动学习模式 (Auto Learn)

**通过 Hook 自动触发！** 每次 AI 回复消息后，系统会自动记录对话。

- 依赖 `fluid-memory-sync` Hook（监听 message:sent 事件）
- 无需手动说「记住xxx」，系统会自动累积
- 可在 `config.yaml` 中关闭：`auto_learn: false`

## 遗忘机制

- **动态遗忘**：检索时分数 < 0.05 被过滤
- **主动遗忘**：调用 `fluid_forget` 归档指定记忆
- **梦境守护**：定时归档分数 < 0.15 的记忆

## 核心理念

- **植入 (Remember)**: 写入新记忆。
- **唤起 (Recall)**: 检索记忆。**每次检索都会强化该记忆**（访问次数+1）。
- **遗忘 (Forget)**: 将匹配的记忆归档。

## 工具 (Tools)

你 (OpenClaw LLM) 可以调用以下工具来与我（Fluid Memory）交互：

### 1. 植入记忆
当用户明确说「记住xxx」时使用。

**Trigger**: 用户说「记住...」「植入...」「记录...」
**Tool Call**:
```json
{
  "name": "fluid_remember",
  "arguments": {
    "content": "用户说的原话"
  }
}
```

### 2. 唤起记忆
当用户问「我之前说过什么」「记得xxx吗」「我的偏好是什么」时使用。

**Trigger**: 用户问「我喜不喜欢...」「还记得...」「我之前...」
**Tool Call**:
```json
{
  "name": "fluid_recall",
  "arguments": {
    "query": "用户的查询关键词"
  }
}
```

### 3. 遗忘
当用户说「忘记xxx」「不要再提xxx」时使用。

**Tool Call**:
```json
{
  "name": "fluid_forget",
  "arguments": {
    "keyword": "要遗忘的关键词"
  }
}
```

### 4. 状态
查看大脑状态。

**Tool Call**:
```json
{
  "name": "fluid_status",
  "arguments": {}
}
```

### 5. 多轮总结
当对话进行 N 轮后（默认3轮），自动总结关键信息。

**Trigger**: 对话达到一定轮次，或用户说"总结一下"

**Tool Call**:
```json
{
  "name": "fluid_summarize",
  "arguments": {
    "conversation": "用户说xxx | 我回复xxx | 用户说xxx | 我回复xxx"
  }
}
```

### 6. 增量总结（推荐）
每次只处理新增对话，自动累积，达到阈值后写入。节省 Token！

**Trigger**: 每次用户说话后调用

**Tool Call**:
```json
{
  "name": "fluid_increment_summarize",
  "arguments": {
    "conversation": "用户说xxx | 我回复xxx"
  }
}
```

## 内部实现 (供开发者参考)

实际执行命令：
```bash
# 使用 Conda 环境
C:\Users\41546\miniconda3\python.exe wrapper.py remember --content "..."
```

## 最佳实践

1.  **自然触发**: 不要机械地调用工具，要理解用户的意图。
2.  **强化重要记忆**: 如果用户多次提到某事，调用 `fluid_recall` 查询它，这会让它记得更牢。
3.  **接受遗忘**: 如果系统返回「没有相关记忆」，不要慌，这说明用户很久没提这件事了，或者确实没说过。
