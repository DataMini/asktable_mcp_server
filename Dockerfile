# 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装依赖工具
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    rm -rf /var/lib/apt/lists/*

# 安装 asktable-mcp-server
RUN /root/.cargo/bin/uv pip install --system asktable-mcp-server

# 暴露 SSE 默认端口（可按需调整）
EXPOSE 9000

# 设置环境变量，支持覆盖
ENV BASE_URL=https://api.asktable.com
ENV PORT=9000

# 启动命令（使用 uvx 启动 MCP 服务）
CMD ["uvx", "asktable-mcp-server", "--transport", "sse", "--port", "9000"]