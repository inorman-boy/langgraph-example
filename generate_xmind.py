# -*- coding: utf-8 -*-
"""生成 LangGraph 知识点思维导图 (.xmind)

XMind 文件本质是一个 ZIP 包，新版核心为 content.json。
重要知识点节点以红色 + 加粗标记。
"""
import json
import zipfile

# 红色样式（重要节点）
RED = "#FF0000"

# ---------------------------------------------------------------------------
# 知识点树结构：{"title", "important"(可选, 默认False), "children"(可选)}
# ---------------------------------------------------------------------------
TREE = {
    "title": "LangGraph 知识体系",
    "important": True,
    "children": [
        {
            "title": "核心概念",
            "important": True,
            "children": [
                {"title": "Graph 图 / 工作流", "important": True},
                {"title": "State 状态", "important": True},
                {"title": "Node 节点", "important": True},
                {"title": "Edge 边", "important": True},
                {"title": "Message 消息"},
            ],
        },
        {
            "title": "图构建基础",
            "important": True,
            "children": [
                {"title": "StateGraph 状态图", "important": True},
                {"title": "add_node / add_edge", "important": True},
                {"title": "compile 编译 + invoke 调用", "important": True},
                {"title": "条件边 add_conditional_edges", "important": True},
                {"title": "MessagesState 默认状态"},
                {"title": "START / END 端点"},
            ],
        },
        {
            "title": "工具调用",
            "important": True,
            "children": [
                {"title": "@tool 装饰器", "important": True},
                {"title": "bind_tools 绑定工具", "important": True},
                {"title": "ToolNode 内置工具节点", "important": True},
                {"title": "ToolRuntime 访问运行时状态"},
                {"title": "结构化输出 with_structured_output"},
                {"title": "Command 动态路由"},
            ],
        },
        {
            "title": "Agent 模式",
            "children": [
                {"title": "create_agent 声明式 Agent"},
                {
                    "title": "5 种工作流模式",
                    "children": [
                        {"title": "提示串联 Prompt Chaining"},
                        {"title": "并行化 Parallelization"},
                        {"title": "路由 Routing"},
                        {"title": "编排-工作者 Orchestrator-Worker"},
                        {"title": "评估-优化 Evaluator-Optimizer"},
                    ],
                },
            ],
        },
        {
            "title": "持久化 Checkpointer",
            "important": True,
            "children": [
                {"title": "Checkpointer 检查点", "important": True},
                {"title": "thread_id 会话隔离", "important": True},
                {
                    "title": "存储后端",
                    "children": [
                        {"title": "InMemorySaver 内存"},
                        {"title": "SqliteSaver SQLite"},
                        {"title": "PyMySQLSaver MySQL"},
                        {"title": "PostgresSaver PostgreSQL"},
                    ],
                },
                {"title": "get_state 读取状态"},
                {"title": "get_state_history 状态历史"},
                {"title": "replay 重放"},
                {"title": "update_state 修改状态"},
            ],
        },
        {
            "title": "长时记忆 Store",
            "children": [
                {
                    "title": "存储后端",
                    "children": [
                        {"title": "InMemoryStore 内存"},
                        {"title": "PostgresStore PostgreSQL"},
                    ],
                },
                {"title": "namespace 命名空间"},
                {"title": "put / get / search / delete"},
                {"title": "语义检索（Embedding）"},
            ],
        },
        {
            "title": "容错机制",
            "children": [
                {"title": "RetryPolicy 重试策略", "important": True},
                {"title": "run_timeout 运行超时"},
                {"title": "idle_timeout 空闲超时"},
                {"title": "错误处理 error handling"},
                {"title": "set_node_defaults 节点默认配置"},
            ],
        },
        {
            "title": "流式输出",
            "children": [
                {"title": "stream / stream_mode"},
                {"title": "stream_events 事件流"},
                {"title": "get_stream_writer 自定义流"},
            ],
        },
        {
            "title": "人机交互 Interrupt",
            "important": True,
            "children": [
                {"title": "interrupt 中断", "important": True},
                {"title": "Command(resume=...) 恢复", "important": True},
                {"title": "审批 / 拒绝模式"},
                {"title": "审核 / 编辑模式"},
                {"title": "工具内中断"},
            ],
        },
        {
            "title": "子图 Subgraph",
            "children": [
                {"title": "子图作为节点"},
                {"title": "节点内调用子图"},
                {"title": "子图持久化"},
                {"title": "子 Agent 作为工具"},
            ],
        },
        {
            "title": "时间旅行",
            "important": True,
            "children": [
                {"title": "replay 重放", "important": True},
                {"title": "fork 分支"},
                {"title": "跳转指定节点"},
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# 构造 content.json
# ---------------------------------------------------------------------------
_counter = {"n": 0}


def _next_id():
    _counter["n"] += 1
    return "topic-%d" % _counter["n"]


def build_topic(node):
    topic = {
        "id": _next_id(),
        "class": "topic",
        "title": node["title"],
    }
    if node.get("important"):
        topic["style"] = {
            "id": _next_id() + "-style",
            "properties": {
                "fo:color": RED,
                "fo:font-weight": "bold",
            },
        }
    children = node.get("children")
    if children:
        topic["children"] = {
            "attached": [build_topic(c) for c in children]
        }
    return topic


def build_content():
    root_topic = build_topic(TREE)
    return [
        {
            "id": _next_id(),
            "class": "sheet",
            "title": "LangGraph 知识体系",
            "rootTopic": root_topic,
        }
    ]


def main(out_path):
    content = build_content()

    metadata = {
        "dataStructureVersion": "2",
        "creator": {
            "name": "Claude Code",
            "version": "1.0.0",
        },
    }

    manifest = {
        "file-entries": {
            "content.json": {},
            "metadata.json": {},
        }
    }

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "content.json",
            json.dumps(content, ensure_ascii=False, indent=2).encode("utf-8"),
        )
        zf.writestr(
            "metadata.json",
            json.dumps(metadata, ensure_ascii=False, indent=2).encode("utf-8"),
        )
        zf.writestr(
            "manifest.json",
            json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8"),
        )

    print("已生成:", out_path)


if __name__ == "__main__":
    main("LangGraph知识点思维导图.xmind")
