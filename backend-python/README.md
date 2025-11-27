# KGQA_HLM

基于知识图谱的《红楼梦》人物关系可视化与问答系统。

[![Project](https://img.shields.io/badge/project-KGQA_HLM-orange.svg)](https://github.com/qingxuandaoming/KGQA_HLM)
[![Python version](https://img.shields.io/badge/language-python3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![License](https://img.shields.io/badge/lisence-MIT-pink.svg)](https://github.com/qingxuandaoming/KGQA_HLM)

## 概要

- 使用 `Flask` 提供前端交互页面与接口。
- 使用 `Neo4j` + `py2neo` 构建与查询人物关系知识图谱。
- 使用 `HanLP` 对中文问题进行分词、词性标注与实体识别，完成关系链推理问答。

## 目录结构

```text
KGQA_HLM/
├─ app.py                  # 项目入口（Flask）
├─ requirements.txt        # Python 依赖
├─ docs/                   # 文档资源
├─ templates/              # 前端模板
├─ static/                 # 前端资源
│  └─ images/
│     └─ characters/       # 人物头像图片
├─ data/
│  └─ profile_data.json    # 人物百科数据
├─ raw_data/
│  └─ relation.txt         # 人物关系三元组原始数据
├─ neo_db/                 # 图谱构建与查询模块
│  ├─ config.py            # 图数据库连接配置
│  ├─ create_graph.py      # 构建知识图谱脚本
│  └─ query_graph.py       # 查询接口
├─ kgqa/                   # 问答逻辑模块
│  ├─ ltp.py               # NLP 处理（分词/词性/实体识别）
│  └─ utils.py             # 工具函数
└─ scripts/                # 辅助脚本
```

## 环境要求

- Python `3.10`
- Neo4j 图数据库（需启用 HTTP `http://localhost:7474`）

## 快速开始

### 1. 安装依赖

建议使用虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置 Neo4j 连接

修改 `neo_db/config.py` 中的配置，或创建 `neo_db/local_config.py`（推荐）：

```python
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your_password"
```

### 3. 构建知识图谱

在项目根目录执行：

```powershell
python neo_db/create_graph.py
```

### 4. 启动 Web 服务

```powershell
python app.py
```

浏览器访问 `http://127.0.0.1:5000/`。

## 功能说明

- **关系搜索**：输入人物名，查看其关系网络。
- **智能问答**：支持如“贾宝玉的父亲是谁”、“林黛玉的母亲的父亲是谁”等多跳关系问答。
- **全图概览**：展示所有人物关系图谱。

## 流程图

![流程](docs/images/图片%201.png)

## 许可证

MIT License
