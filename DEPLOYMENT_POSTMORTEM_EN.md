# Langfuse Local Deployment Post-Mortem & SOP (macOS/ARM64)

## 1. Project Background & Core Challenges

The goal of this project was to deploy Langfuse locally on a macOS (Apple Silicon/ARM64) environment to facilitate LangGraph trace testing.

**Core Pain Points**:
*   **Excessive Time Cost**: The deployment process took several hours, involving repeated debugging and failures.
*   **Model Limitations**: Previous attempts with other LLMs failed to accurately pinpoint the root cause of the crash loop.
*   **Complexity**: The task involved navigating China's network restrictions (Docker image pulling), ARM64 architecture compatibility, and SDK version mismatches.

**Milestone**:
With the assistance of **Gemini 3.0**, we successfully resolved the persistent "infinite restart" issue and verified the full testing link. This serves as a benchmark case, demonstrating the importance of precise problem diagnosis and flexible strategies (downgrading) in complex DevOps scenarios.

---

## 2. Deep Dive: What Happened?

### Phase 1: The Network Hurdle
*   **Issue**: Due to network restrictions in China, pulling the official `langfuse/langfuse` image from Docker Hub was extremely slow or failed.
*   **Solution**: Switched to a domestic mirror (e.g., Huawei Cloud `swr.cn-north-4.myhuaweicloud.com`).
*   **Lesson**: Always secure your "supply chain" (image sources) before starting deployment.

### Phase 2: Configuration Hell & The Crash Loop
*   **Issue**: The Langfuse v3 container would start and immediately crash, entering a CrashLoopBackOff. Logs showed `TypeError: Cannot set property message of ZodError`.
*   **Failed Attempts**:
    *   Repeatedly modifying `NEXTAUTH_URL`, `HOSTNAME`, `PORT`.
    *   Regenerating `ENCRYPTION_KEY` and `SALT`.
    *   Pinning specific v3 minor versions (3.0.0, 3.1.0).
    *   Wiping Docker volumes (`docker-compose down -v`).
*   **The Gemini 3.0 Breakthrough**:
    *   Analyzed the logs to identify that the error was not a configuration issue, but a **fundamental incompatibility between the Node.js runtime in the v3 image and the ARM64 architecture**.
    *   Decisively proposed a **downgrade strategy**, pivoting to the stable v2 version instead of fighting the v3 incompatibility.

### Phase 3: SDK Integration Gap
*   **Issue**: After downgrading the server to v2, local Python scripts failed with `404 Not Found` and `ImportError`.
*   **Reason**: The local environment had `langfuse` v3 installed, which defaults to v3 API endpoints and uses different import paths.
*   **Solution**:
    *   Downgraded the Python package: `pip install "langfuse<3"`.
    *   Fixed code imports: Changed `from langfuse import observe` to `from langfuse.decorators import observe`.

---

## 3. Standard Operating Procedure (SOP)

To avoid "reinventing the wheel" next time, strictly follow this SOP.

### 3.1 Pre-requisites
1.  **Docker**: Ensure Docker Engine is running.
2.  **Network**: Verify image pull connectivity.
3.  **Ports**: Ensure port `3000` is free.

### 3.2 Configuration (docker-compose.yml)
Use this verified v2 configuration. **Do not attempt v3 unless architecture compatibility is confirmed.**

```yaml
version: '3.9'
services:
  langfuse:
    # Key Decision: Use v2 for ARM64 stability
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

### 3.3 Launch Commands
Run in terminal:

```bash
# 1. Clean up old environment
docker-compose down -v

# 2. Start services
docker-compose up -d

# 3. Health Check (Critical)
# Wait for "Ready in ...ms"
docker logs -f <container_id>
```

### 3.4 Client Setup
Server is v2, so Client **must** be v2.

1.  **Install Dependency**:
    ```bash
    pip install "langfuse<3"
    ```

2.  **Configure .env**:
    ```env
    LANGFUSE_HOST=http://localhost:3000
    LANGFUSE_PUBLIC_KEY=pk-lf-...
    LANGFUSE_SECRET_KEY=sk-lf-...
    ```

3.  **Code Template**:
    ```python
    # Import for v2 SDK
    from langfuse.decorators import observe
    from langfuse import Langfuse
    
    langfuse = Langfuse()
    
    @observe()
    def my_function():
        pass
    ```

---

## 4. Summary
The success of this deployment was not just about fixing a bug, but validating an engineering mindset: **"When facing fundamental architectural incompatibility, downgrade quickly to ensure business continuity."** Gemini 3.0 played a crucial role in this decision-making process, helping us break out of the configuration loop and solve the problem through architectural adjustment.
