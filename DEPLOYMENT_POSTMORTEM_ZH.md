# Langfuse 本地部署全链路复盘与 SOP (macOS/ARM64)

## 1. 项目背景与核心挑战

本次项目的目标是在 macOS (Apple Silicon/ARM64) 环境下本地部署 Langfuse，以便配合 LangGraph 进行链路追踪测试。

**核心痛点**：
*   **耗时过长**：整个部署过程耗费数小时，经历了反复的调试和失败。
*   **模型能力瓶颈**：此前尝试使用其他大模型辅助部署均未成功，无法准确通过日志定位到核心的架构兼容性问题。
*   **网络与环境复杂性**：涉及国内网络环境下 Docker 镜像拉取困难、ARM64 架构兼容性、以及新旧版本 SDK 的适配问题。

**里程碑**：
本次通过 **Gemini 3.0** 模型，在经历了从网络配置、参数调试到最终版本决策的全过程后，成功解决了困扰已久的“无限重启”问题，并跑通了全链路测试。这是一个标杆性的调试案例，证明了在复杂运维场景下，精准的问题定位和灵活的变通策略（降级方案）的重要性。

---

## 2. 深度复盘：我们经历了什么？

### 第一阶段：网络环境与镜像拉取 (The Network Hurdle)
*   **问题**：由于国内网络环境限制，直接从 Docker Hub 拉取 `langfuse/langfuse` 镜像极其缓慢甚至失败。
*   **解决**：
    *   放弃官方源，转而使用国内镜像源（如华为云 `swr.cn-north-4.myhuaweicloud.com`）。
    *   **经验**：在任何部署开始前，必须优先解决“粮草”问题——确保镜像源畅通。

### 第二阶段：配置地狱与无限重启 (The Configuration Hell)
*   **问题**：Langfuse v3 容器启动后陷入 CrashLoopBackOff（无限重启），日志报错 `TypeError: Cannot set property message of ZodError`。
*   **尝试过的弯路**：
    *   反复修改 `NEXTAUTH_URL`、`HOSTNAME`、`PORT` 等环境变量（无效）。
    *   重新生成加密密钥 `ENCRYPTION_KEY` 和 `SALT`（无效）。
    *   尝试锁定 v3 的不同小版本（3.0.0, 3.1.0）（无效）。
    *   多次执行 `docker-compose down -v` 清空数据（无效）。
*   **Gemini 3.0 的突破**：
    *   通过深度分析日志，识别出该错误并非配置问题，而是 **Node.js 运行时在 ARM64 架构下与 Langfuse v3 镜像的底层兼容性问题**。
    *   果断提出**降级策略**，不再死磕 v3，转而部署极其稳定的 v2 版本。

### 第三阶段：SDK 版本适配 (The Integration Gap)
*   **问题**：服务端降级到 v2 后，本地 Python 脚本运行报错 `404 Not Found` 和 `ImportError`。
*   **原因**：本地安装的 `langfuse` Python 包是 v3 版本，默认请求 v3 API 接口，且代码中使用了 v3 独有的 `observe` 导入路径。
*   **解决**：
    *   强制降级 Python 包：`pip install "langfuse<3"`。
    *   修正代码导入：从 `from langfuse import observe` 改为 `from langfuse.decorators import observe`。

---

## 3. 标准化操作流程 (SOP) - 下次部署只需 5 分钟

为了避免下次在服务器或其他电脑上重复“造轮子”，请严格执行以下 SOP。

### 3.1 环境准备清单
1.  **Docker 环境**: 确保 Docker Engine 已安装并运行。
2.  **网络检查**: 确认可以拉取镜像（必要时配置镜像加速器）。
3.  **端口检查**: 确保本地 `3000` 端口未被占用。

### 3.2 部署配置文件 (docker-compose.yml)
直接使用这份经过验证的 v2 稳定版配置，**不要轻易尝试 v3 (除非确认架构兼容)**。

```yaml
version: '3.9'
services:
  langfuse:
    # 核心决策：使用 v2 镜像以保证 ARM64 稳定性
    image: ghcr.io/langfuse/langfuse:2
    depends_on:
      - db
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
      - NEXTAUTH_SECRET=mysecret
      - SALT=mysalt
      - NEXTAUTH_URL=http://localhost:3000
      - TELEMETRY_ENABLED=false
      - NEXT_TELEMETRY_DISABLED=1
    restart: always

  db:
    image: postgres
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=postgres
    ports:
      - "5432:5432"
    volumes:
      - database_data:/var/lib/postgresql/data

volumes:
  database_data:
    driver: local
```

### 3.3 一键启动指令集
在终端中依次执行：

```bash
# 1. 清理旧环境（防止残留数据干扰）
docker-compose down -v

# 2. 启动服务
docker-compose up -d

# 3. 检查健康状态（关键步骤）
# 等待日志出现 "Ready in ...ms"
docker logs -f <容器ID或名称>
```

### 3.4 客户端接入规范
服务端是 v2，客户端**必须**也是 v2。

1.  **安装依赖**:
    ```bash
    pip install "langfuse<3"
    ```

2.  **配置环境变量 (.env)**:
    ```env
    LANGFUSE_HOST=http://localhost:3000
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_SECRET_KEY=sk-lf-...
    ```

3.  **代码模板**:
    ```python
    # 适配 v2 的导入方式
    from langfuse.decorators import observe
    from langfuse import Langfuse
    
    # 初始化
    langfuse = Langfuse()
    
    @observe()
    def my_function():
        pass
    ```

---

## 4. 总结
本次部署的成功不仅仅是解决了一个 Bug，而是验证了一套**“遇到底层架构不兼容时，快速降级以保业务可用”**的工程化思维。Gemini 3.0 在此过程中起到了关键的决策辅助作用，帮助我们跳出了配置文件的死循环，直接通过架构调整解决了问题。
