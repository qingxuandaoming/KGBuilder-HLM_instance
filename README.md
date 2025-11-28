# Knowledge Graph Builder & QA Platform

这是一个集成了 **KGBuilder** (知识图谱构建平台) 和 **KGQA_HLM** (红楼梦智能问答) 的统一项目。
项目来源于两个开源项目，它们分别是Neo4j-KGBuilder<https://github.com/MiracleTanC/Neo4j-KGBuilder.git>和KGQA_HLM<https://github.com/chizhu/KGQA_HLM.git>

## 项目结构

*   `backend-java/`: 原 Neo4j-KGBuilder 后端 (Java/Spring Boot)。负责图谱管理、可视化。
*   `backend-python/`: 原 KGQA_HLM 后端 (Python/Flask)。负责红楼梦领域的自然语言问答。
*   `frontend/`: 前端界面 (Vue.js)。统一的用户交互入口。
*   `start_all.py`: 一键启动脚本。

## 快速开始

### 前置条件
*   JDK 17+
*   Maven 3+
*   Python 3.10+
*   Node.js 16+
*   Neo4j 4.x/5.x (运行在 `bolt://localhost:7687`, 用户名 `neo4j`, 密码 `12345678`)
*   **注意**: 必须安装 Neo4j **APOC** 插件，否则 Java 后端部分功能不可用。

### 安装依赖

1.  **Python 依赖**:
    ```bash
    cd backend-python
    pip install -r requirements.txt
    ```

2.  **前端依赖**:
    ```bash
    cd frontend
    npm install
    ```

3.  **Java 依赖**:
    ```bash
    cd backend-java
    mvn clean install
    ```

### 启动项目

在根目录下运行：

```bash
python start_all.py
```

该脚本将同时启动：
*   Java 后端 (Port 8081)
*   Python 后端 (Port 5000)
*   前端开发服务器 (通常 Port 8080)

## 集成计划

详细的合并与集成路线图请参考 [MERGE_PLAN.md](./MERGE_PLAN.md)。
