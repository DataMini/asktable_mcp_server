FROM python:3.11-slim

WORKDIR /app

# 安装 pip 和 asktable-mcp-server
RUN apt-get update && apt-get install -y curl && \
    pip install --no-cache-dir asktable-mcp-server && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 暴露默认端口（SSE 模式）
EXPOSE 9000

# 默认环境变量
ENV BASE_URL=https://api.asktable.com
ENV PORT=9000

# 默认使用 sse 模式启动
CMD ["asktable-mcp-server", "--transport", "sse", "--port", "9000"]