# LangGraph 学习示例

一套从入门到进阶的 LangGraph 学习示例，基于 **DeepSeek 大模型**，覆盖图构建、工具调用、工作流模式、持久化、容错、流式输出、人机交互、子图、时间旅行等核心能力。

> 目录结构由 `D:\Project\example\demo\LangGraphStudy` 迁移而来，已移除 `egg-info`、`__pycache__`、`checkpoints.db` 等构建/运行时产物。

---

## 目录总览

| 目录 | 主题 |
|------|------|
| [01_langgraph_quickstart](#01_langgraph_quickstart) | 快速上手：最小图 + 工具调用 |
| [02_langgraph_use](#02_langgraph_use) | 实战：邮件分类、工具运行时、Agent、5 种工作流模式 |
| [03_langgraph_checkpointer](#03_langgraph_checkpointer) | 检查点：线程、持久化、状态回放 |
| [04_langgraph_store](#04_langgraph_store) | 长时记忆 Store |
| [05_langgraph_fault_tolerance](#05_langgraph_fault_tolerance) | 容错：重试、超时、错误处理 |
| [06_langgraph_streaming](#06_langgraph_streaming) | 流式输出与事件流 |
| [07_langgraph_interrupt](#07_langgraph_interrupt) | 中断与人工介入 |
| [08_langgraph_subgraphs](#08_langgraph_subgraphs) | 子图与子 Agent |
| [09_langgraph_timetravel](#09_langgraph_timetravel) | 时间旅行：replay / fork / 跳转 |

顶层文件：

- `pyproject.toml` — 项目元信息与依赖声明
- `langgraph.json` — LangGraph 平台部署配置（定义 graph、checkpointer、store）
- `init_llm.py` — 初始化 DeepSeek 模型
- `env_utils.py` — 从 `.env` 加载环境变量
- `.env.example` — 环境变量模板

---

## 环境准备

### 1. 前置条件

- Python >= 3.10

### 2. 安装依赖

```bash
# 核心依赖（langgraph + langchain）
pip install -e .

# 额外依赖（按需，见下方依赖清单）
pip install python-dotenv langchain-community dashscope pymysql "psycopg[binary]" langgraph-sdk
```

### 3. 配置环境变量

```bash
# 复制模板并填入真实密钥
cp .env.example .env
```

`.env` 中至少需要：

```env
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

### 4. 运行示例

```bash
# 方式一：直接运行单个脚本（大多数示例）
python 01_langgraph_quickstart/01_hello_world.py

# 方式二：启动 LangGraph 服务（配合 client 示例）
langgraph dev
```

---

## 依赖清单

| 依赖 | 用途 | 必需性 |
|------|------|--------|
| `langgraph>=1.2` | 图构建、checkpointer、store、retry、interrupt、subgraph | ✅ 核心 |
| `langchain>=1.2` | `create_agent`、`init_chat_model`、工具 | ✅ 核心 |
| `langchain-core` | messages、tools、language_models | ✅ 随 langchain 自动安装 |
| `pydantic` | 结构化输出（`BaseModel`） | ✅ 随 langchain-core |
| `python-dotenv` | `env_utils.py` 加载 `.env` | ✅ 核心 |
| `langgraph-sdk` | `02/08`、`03/13 client`、`04/07 client` 连接 server | ⚠️ 仅 client 示例 |
| `langchain-community` | `04/03` 语义搜索 `DashScopeEmbeddings` | ⚠️ 仅语义搜索 |
| `dashscope` | `DashScopeEmbeddings` 底层 SDK | ⚠️ 仅语义搜索 |
| `pymysql` | `03/10` MySQL 持久化 `PyMySQLSaver` | ⚠️ 仅 MySQL |
| `psycopg` | `03/11-13`、`04/05-07` PostgreSQL 持久化 | ⚠️ 仅 PostgreSQL |

> 说明：SQLite 持久化（`03/09`）使用 Python 内置 `sqlite3`，无需额外安装。

---

## 各模块详解

### 01_langgraph_quickstart

| 文件 | 说明 |
|------|------|
| `01_hello_world.py` | 最小图：单 LLM 节点，认识 `StateGraph` / `add_node` / `add_edge` / `compile` / `invoke` 与 `MessagesState` |
| `02_calculator_demo.py` | 工具调用计算器：`@tool` + 手写 `tool_node` + `add_conditional_edges` |
| `03_calculator_demo2.py` | 计算器升级版（带 `__main__` 入口） |

### 02_langgraph_use

| 文件 | 说明 |
|------|------|
| `01_email_demo.py` | 邮件分类处理：结构化输出 + `Command` 条件路由 + 生成回复 |
| `02_email_demo2.py` | 邮件处理升级版 |
| `03_workflow_mode/` | **5 种常见工作流模式**（含 PNG 图） |
| ├ `01_prompt_chaining.py` | 提示串联 |
| ├ `02_parallelization.py` | 并行化（多任务并行 → 聚合） |
| ├ `03_routing.py` | 路由 |
| ├ `04_orchestrator_worker.py` | 编排-工作者 |
| └ `05_evaluator_optimizer.py` | 评估-优化 |
| `04_toolnode_calculator_demo.py` | 用内置 `ToolNode` 重构计算器 |
| `05_tool_runtime_demo.py` | `ToolRuntime`：工具内访问运行时状态（`langgraph.json` 的 `my_graph`） |
| `06_tool_runtime_demo2.py` | `ToolRuntime` 升级版 |
| `07_agent_demo.py` | `create_agent` 声明式 Agent（`langgraph.json` 的 `my_agent`） |
| `08_graph_client.py` | `langgraph-sdk` 客户端，连接 `langgraph dev` 服务 |

### 03_langgraph_checkpointer

| 文件 | 说明 |
|------|------|
| `01_thread_and_checkpointer.py` | checkpointer 基础 + `thread_id` 会话隔离 |
| `02_super_step_case.py` | 超级步骤（super-step） |
| `03_checkpointer_state.py` | 检查点状态 |
| `04_get_state_case.py` | `get_state` 读取最新状态 |
| `05_get_state_history_case.py` | `get_state_history` 状态历史 |
| `06_checkpoint_replay_case.py` | 检查点重放（replay） |
| `07_update_state_case.py` | `update_state` 修改状态 |
| `08_durablity_mode_case.py` | 持久化模式（durability） |
| `09_sqlite_saver_case.py` | SQLite 持久化（内置 `sqlite3`） |
| `10_mysql_saver_case.py` | MySQL 持久化 `PyMySQLSaver` |
| `11_postgres_saver_case.py` | PostgreSQL 持久化 `PostgresSaver` |
| `12_checkpointer_demo.py` | checkpointer 综合 demo |
| `13_langgraph_checkpoint_demo/` | 完整服务 demo（`graph.py` / `checkpointer.py` / `client.py`） |

### 04_langgraph_store

| 文件 | 说明 |
|------|------|
| `01_store_base.py` | Store 基础：`put` / `get` / `search` / `delete` / `list_namespaces` |
| `02_store_page.py` | 分页查询 |
| `03_semanti_search.py` | 语义检索（`DashScopeEmbeddings`） |
| `04_langgraph_store_inmemory.py` | 图内使用内存 Store |
| `05_langgraph_store_inpostgres.py` | 图内使用 Postgres Store |
| `06_store_demo.py` | Store 综合 demo |
| `07_langgraph_store_demo/` | 完整服务 demo（`graph.py` / `store.py` / `client.py`） |

### 05_langgraph_fault_tolerance

| 文件 | 说明 |
|------|------|
| `01_retrypolicy_case.py` | `RetryPolicy` 重试策略 |
| `02_custom_retrypolicy_case.py` | 自定义重试策略 |
| `03_run_timeout_case.py` | 运行超时 |
| `04_idle_timeout_case.py` | 空闲超时 |
| `05_retry_and_timeout_case.py` | 重试 + 超时组合 |
| `06_error_handling_case1.py` | 错误处理（一） |
| `07_error_handling_case2.py` | 错误处理（二） |
| `08_set_node_defaults_case.py` | 节点默认配置 `set_node_defaults` |

### 06_langgraph_streaming

| 文件 | 说明 |
|------|------|
| `01_langgraph_stream_case.py` | `stream` 基础（`stream_mode`） |
| `02_langgraph_stream_v2_case.py` | stream v2 |
| `03_stream_messages_filter.py` | 消息过滤 |
| `04_stream_state_case.py` | 状态流式输出 |
| `05_event_streaming_case.py` | 事件流 |
| `06_event_stream_interleave.py` | 事件交错 |

### 07_langgraph_interrupt

| 文件 | 说明 |
|------|------|
| `01_interrupt_basic_case.py` | `interrupt` 基础 + `Command(resume=...)` 恢复 |
| `02_interrupt_basic_case2.py` | 中断基础（二） |
| `03_interrupt_case3.py` | 中断（三） |
| `04_interrupt_approve_reject_case.py` | 审批 / 拒绝模式 |
| `05_interrupt_review_edit_case.py` | 审核 / 编辑模式 |
| `06_interrupt_multiple_case.py` | 多中断 |
| `07_interrupt_in_tool_case.py` | 工具内中断 |

### 08_langgraph_subgraphs

| 文件 | 说明 |
|------|------|
| `01_subgraphs_case.py` | 子图作为主图节点（订单支付 → 发货子图） |
| `02_call_subgraph_inside_node.py` | 节点内调用子图 |
| `03_subgraphs_case2.py` | 子图（二） |
| `04_subgraphs_persistence.py` | 子图持久化 |
| `05_subagent_as_tool.py` | 子 Agent 作为工具 |
| `06_subagent_per_thread.py` | 每线程独立子 Agent |
| `07_view_subgraph_state.py` | 查看子图状态 |
| `08_subgraph_comprehensive_case.py` | 子图综合案例 |

### 09_langgraph_timetravel

| 文件 | 说明 |
|------|------|
| `01_time_travel_replay_case.py` | Replay：从历史检查点重放 |
| `02_time_travel_fork_case.py` | Fork：分支新线程 |
| `03_time_travel_jump_node_case.py` | 跳转到指定节点 |
| `04_time_travel_interrupt_case.py` | 中断中的时间旅行 |
| `05_time_travel_in_interrupt.py` | 中断场景内的时间旅行 |

---

## 运行命令索引

### 直接运行（`python <path>`）

```bash
# 快速上手
python 01_langgraph_quickstart/01_hello_world.py
python 01_langgraph_quickstart/02_calculator_demo.py
python 01_langgraph_quickstart/03_calculator_demo2.py

# 实战
python 02_langgraph_use/01_email_demo.py
python 02_langgraph_use/02_email_demo2.py
python 02_langgraph_use/03_workflow_mode/01_prompt_chaining.py
python 02_langgraph_use/03_workflow_mode/02_parallelization.py
python 02_langgraph_use/03_workflow_mode/03_routing.py
python 02_langgraph_use/03_workflow_mode/04_orchestrator_worker.py
python 02_langgraph_use/03_workflow_mode/05_evaluator_optimizer.py
python 02_langgraph_use/04_toolnode_calculator_demo.py
python 02_langgraph_use/06_tool_runtime_demo2.py

# 检查点
python 03_langgraph_checkpointer/01_thread_and_checkpointer.py
python 03_langgraph_checkpointer/08_durablity_mode_case.py
python 03_langgraph_checkpointer/09_sqlite_saver_case.py
python 03_langgraph_checkpointer/12_checkpointer_demo.py

# Store
python 04_langgraph_store/01_store_base.py
python 04_langgraph_store/02_store_page.py
python 04_langgraph_store/06_store_demo.py

# 容错
python 05_langgraph_fault_tolerance/07_error_handling_case2.py

# 流式
python 06_langgraph_streaming/01_langgraph_stream_case.py
python 06_langgraph_streaming/02_langgraph_stream_v2_case.py
python 06_langgraph_streaming/03_stream_messages_filter.py
python 06_langgraph_streaming/04_stream_state_case.py
python 06_langgraph_streaming/05_event_streaming_case.py
python 06_langgraph_streaming/06_event_stream_interleave.py

# 中断
python 07_langgraph_interrupt/02_interrupt_basic_case2.py
python 07_langgraph_interrupt/03_interrupt_case3.py
python 07_langgraph_interrupt/04_interrupt_approve_reject_case.py
python 07_langgraph_interrupt/05_interrupt_review_edit_case.py
python 07_langgraph_interrupt/06_interrupt_multiple_case.py
python 07_langgraph_interrupt/07_interrupt_in_tool_case.py

# 子图
python 08_langgraph_subgraphs/01_subgraphs_case.py
python 08_langgraph_subgraphs/03_subgraphs_case2.py
python 08_langgraph_subgraphs/04_subgraphs_persistence.py
python 08_langgraph_subgraphs/05_subagent_as_tool.py
python 08_langgraph_subgraphs/06_subagent_per_thread.py
python 08_langgraph_subgraphs/07_view_subgraph_state.py
python 08_langgraph_subgraphs/08_subgraph_comprehensive_case.py

# 时间旅行
python 09_langgraph_timetravel/01_time_travel_replay_case.py
python 09_langgraph_timetravel/02_time_travel_fork_case.py
python 09_langgraph_timetravel/03_time_travel_jump_node_case.py
python 09_langgraph_timetravel/04_time_travel_interrupt_case.py
python 09_langgraph_timetravel/05_time_travel_in_interrupt.py
```

### 通过 LangGraph 服务运行（`langgraph dev` + client）

`langgraph.json` 注册了 4 个 graph，启动服务后可用 `langgraph-sdk` 客户端调用：

```bash
# 启动服务（默认端口 2024）
langgraph dev

# 另一个终端，用客户端调用
python 02_langgraph_use/08_graph_client.py
python 03_langgraph_checkpointer/13_langgraph_checkpoint_demo/client.py
python 04_langgraph_store/07_langgraph_store_demo/client.py
```

注册的 graph：

| 名称 | 入口 |
|------|------|
| `my_graph` | `02_langgraph_use/05_tool_runtime_demo.py:agent` |
| `my_agent` | `02_langgraph_use/07_agent_demo.py:agentx` |
| `langgraph_checkpoint` | `03_langgraph_checkpointer/13_langgraph_checkpoint_demo/graph.py:graph` |
| `langgraph_store` | `04_langgraph_store/07_langgraph_store_demo/graph.py:graph` |

---

## 注意事项

- `.env.example` 中含真实 `LANGSMITH_API_KEY` 与 `DEEPSEEK_API_KEY` 占位，正式使用请替换为自己的密钥；提交代码前建议将密钥改回占位符。
- 涉及 MySQL / PostgreSQL 的示例需自备对应数据库，并按文件内 `DB_URI` 修改连接串。
- 首次运行会调用 DeepSeek 大模型，请确保网络与额度正常。
