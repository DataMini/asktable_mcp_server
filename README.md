# asktable-mcp-server

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/asktable-mcp-server.svg)](https://pypi.org/project/asktable-mcp-server/)

`asktable-mcp-server` 是为 [AskTable](https://www.asktable.com/) 提供的 MCP 服务，支持通过 Stdio 或 SSE 协议与 AskTable SaaS 或本地部署服务交互。

## 快速开始

### 安装与配置
本地先安装uv配置工具。
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## 2×2 配置方式总览

| 模式          | `--transport` | `--port`（仅SSE） | `base_url` 环境变量         |
|---------------|--------------|------------------|-----------------------------|
| Stdio + SaaS  | stdio        | 无               | 不填                        |
| Stdio + 本地  | stdio        | 无               | 填写本地地址                 |
| SSE + SaaS    | sse          | 必填             | 不填                        |
| SSE + 本地    | sse          | 必填             | 填写本地地址                 |

- **Stdio/SSE** 由 `--transport` 决定
- **SaaS/本地** 由 `base_url` 是否填写决定
- SSE 必须加 `--port`，Stdio 不需要

---

## 参数说明

- `api_key`：AskTable API 密钥（必需，环境变量）
- `datasource_id`：数据源ID（必需，环境变量）
- `base_url`：本地IP服务地址（可选，填写则走本地部署）
- `--transport`：通信协议，`stdio` 或 `sse`
- `--port`：SSE模式端口（仅SSE时必填）

---

## 配置示例

> 以下为 `mcpServers` 配置片段，只需根据实际情况选择一种模式即可。

<details>
<summary>Stdio + SaaS</summary>

```json
{
  "mcpServers": {
    "asktable-mcp-server": {
      "command": "uvx",
      "args": ["asktable-mcp-server@latest", "--transport", "stdio"],
      "env": {
        "api_key": "your_api_key",
        "datasource_id": "your_datasource_id"
      }
    }
  }
}
```
</details>

<details>
<summary>Stdio + 本地部署</summary>

```json
{
  "mcpServers": {
    "asktable-mcp-server": {
      "command": "uvx",
      "args": ["asktable-mcp-server@latest", "--transport", "stdio"],
      "env": {
        "api_key": "your_api_key",
        "datasource_id": "your_datasource_id",
        "base_url": "http://192.168.1.3:8030/api"
      }
    }
  }
}
```
</details>

<details>
<summary>SSE + SaaS</summary>

```json
{
  "mcpServers": {
    "asktable-mcp-server": {
      "command": "uvx",
      "args": ["asktable-mcp-server@latest", "--transport", "sse", "--port", "9000"],
      "env": {
        "api_key": "your_api_key",
        "datasource_id": "your_datasource_id"
      }
    }
  }
}
```
</details>

<details>
<summary>SSE + 本地部署</summary>

```json
{
  "mcpServers": {
    "asktable-mcp-server": {
      "command": "uvx",
      "args": ["asktable-mcp-server@latest", "--transport", "sse", "--port", "9000"],
      "env": {
        "api_key": "your_api_key",
        "datasource_id": "your_datasource_id",
        "base_url": "http://192.168.1.3:8030/api"
      }
    }
  }
}
```
</details>

---

## 启动命令示例

- Stdio 模式（本地或SaaS）：
  ```bash
  uvx asktable-mcp-server@latest --transport stdio
  ```

- SSE 模式（本地或SaaS）：
  ```bash
  uvx asktable-mcp-server@latest --transport sse --port 9000
  ```

---

如需进一步帮助，请查阅官方文档或联系我们。