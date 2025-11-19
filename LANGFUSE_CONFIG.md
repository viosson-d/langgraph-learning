# Langfuse 配置指南

## 方案 1: 使用 Langfuse Cloud（推荐快速开始）

### 步骤 1: 注册账户
访问 https://cloud.langfuse.com 注册免费账户

### 步骤 2: 获取凭证
- 登录后进入 Dashboard → Settings → API Keys
- 复制 `Public Key` 和 `Secret Key`

### 步骤 3: 在 Python 中配置
```python
import os
from langfuse.callback import CallbackHandler

os.environ["LANGFUSE_PUBLIC_KEY"] = "pk_xxx..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk_xxx..."

langfuse_callback = CallbackHandler()
```

---

## 方案 2: 本地部署 Langfuse

### 步骤 1: 安装 Docker（如果未安装）
```bash
# macOS
brew install docker
# 或下载 Docker Desktop: https://www.docker.com/products/docker-desktop
```

### 步骤 2: 启动 Langfuse 本地实例
```bash
docker run \
  -e DATABASE_URL="postgresql://postgres:postgres@db:5432/langfuse" \
  -e NEXTAUTH_SECRET="your-secret-key" \
  -p 3000:3000 \
  ghcr.io/langfuse/langfuse:latest
```

或使用 Docker Compose（更简单）：
```bash
# 创建 docker-compose.yml 文件，内容见下方
docker-compose up -d
```

### 步骤 3: 访问本地仪表板
访问 http://localhost:3000

### 步骤 4: 创建 API 密钥
- 点击 Settings → API Keys
- 创建新的 Public/Secret Key

### 步骤 5: 在 Python 中配置
```python
import os
from langfuse.callback import CallbackHandler

os.environ["LANGFUSE_PUBLIC_KEY"] = "your-public-key"
os.environ["LANGFUSE_SECRET_KEY"] = "your-secret-key"
os.environ["LANGFUSE_HOST"] = "http://localhost:3000"

langfuse_callback = CallbackHandler()
```

---

## 使用示例

运行脚本追踪你的 LangGraph：
```bash
python3 langgraph_langfuse.py
```

然后访问 Langfuse Dashboard 查看：
- 📊 执行流程可视化
- ⏱️ 性能指标
- 🔍 详细的调用追踪
- 💾 成本统计

---

## docker-compose.yml 示例（用于本地部署）

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: langfuse
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  langfuse:
    image: ghcr.io/langfuse/langfuse:latest
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/langfuse
      NEXTAUTH_SECRET: your-secret-key
      NEXTAUTH_URL: http://localhost:3000
    depends_on:
      - db

volumes:
  postgres_data:
```

保存为 `docker-compose.yml`，运行 `docker-compose up -d` 即可！
