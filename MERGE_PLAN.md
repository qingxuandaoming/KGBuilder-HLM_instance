# 项目合并与集成计划 (KGBuilder & KGQA_HLM)

本计划旨在将 `Neo4j-KGBuilder` (Java/Vue 知识图谱构建平台) 与 `KGQA_HLM` (Python 红楼梦问答系统) 进行深度集成，形成一个统一的“知识图谱构建与问答平台”。

## 1. 项目现状分析

| 特性 | Neo4j-KGBuilder | KGQA_HLM |
| :--- | :--- | :--- |
| **后端语言** | Java (Spring Boot) | Python (Flask) |
| **前端技术** | Vue.js + Element UI | HTML + jQuery + Jinja2 |
| **数据库** | Neo4j | Neo4j |
| **核心功能** | 图谱构建、可视化、管理 | 垂直领域(红楼梦)问答、关系检索 |
| **运行端口** | 8081 (API), 80/8080 (UI) | 5000 |

## 2. 合并目标

1.  **统一入口**：用户通过统一的 Web 界面访问图谱构建和问答功能。
2.  **数据互通**：两者共享同一个 Neo4j 数据库实例。
3.  **架构解耦**：保留 Python 在 NLP 处理上的优势，将其作为微服务运行；Java 作为主后端处理业务逻辑和图谱管理。

## 3. 详细实施步骤

### 第一阶段：目录重构与环境统一
**目标**：整理项目结构，使其清晰可维护。

1.  **根目录整理**：
    ```text
    /
    ├── backend-java/       <-- 原 Neo4j-KGBuilder (后端模块)
    ├── backend-python/     <-- 原 KGQA_HLM
    ├── frontend/           <-- 原 Neo4j-KGBuilder/kgBuilder-ui
    ├── docs/               <-- 文档
    ├── scripts/            <-- 启动脚本
    └── README.md
    ```
2.  **依赖管理**：
    *   Java: 确认 Maven 构建无误。
    *   Python: 在 `backend-python` 下生成标准 `requirements.txt`。

### 第二阶段：数据库集成
**目标**：确保两个系统能操作同一份数据。

1.  **统一配置**：
    *   修改 `backend-python/neo_db/config.py` (如有) 和 `backend-java/.../application-dev.yml`，使其指向同一个 Neo4j 实例（默认 `bolt://localhost:7687`）。
2.  **数据迁移**：
    *   利用 `KGQA_HLM` 的 `create_graph.py` 将红楼梦数据导入 Neo4j。
    *   验证 `KGBuilder` 能否读取并可视化这些数据。

### 第三阶段：后端微服务化
**目标**：Java 后端能够调用 Python 的 NLP 能力，或前端直接调用 Python API。

1.  **Python API 增强**：
    *   确保 `KGQA_HLM` 的 Flask 接口支持跨域 (CORS)，以便前端直接调用。
    *   保留 `/KGQA_answer`, `/get_profile` 等核心接口。
2.  **接口代理 (可选)**：
    *   在 Java 端建立 Proxy Controller，转发请求到 Python 端 (如 `/api/qa/*` -> `localhost:5000/*`)，这样前端只需面对一个域名。

### 第四阶段：前端融合
**目标**：将红楼梦问答界面移植到 Vue。

1.  **组件化**：
    *   在 `frontend/src/views` 下新建 `QA` 目录。
    *   将 `KGQA_HLM/templates/KGQA.html` 的逻辑移植为 `QAPanel.vue`。
    *   将 `KGQA_HLM/templates/search.html` 的逻辑移植为 `SearchPanel.vue`。
2.  **路由配置**：
    *   在 `frontend/src/router/index.js` 添加 `/qa` 和 `/search` 路由。
3.  **API 调用**：
    *   使用 `axios` 替换原有的 jQuery AJAX 调用，指向 Python 后端接口。

### 第五阶段：统一启动
**目标**：一键启动所有服务。

1.  编写 `start_all.py` 或 `docker-compose.yml`，同时启动：
    *   Neo4j (如果容器化)
    *   Java Backend (Spring Boot)
    *   Python Backend (Flask)
    *   Frontend (Nginx 或 Dev Server)

## 4. 立即执行计划 (Quick Wins)

为了快速验证，我们将执行以下操作：
1.  **整理目录**：将现有的文件夹重命名并移动到标准结构。
2.  **生成启动脚本**：创建一个 Python 脚本来同时启动 Java 和 Python 服务。
3.  **文档更新**：更新 README 说明如何运行合并后的项目。
