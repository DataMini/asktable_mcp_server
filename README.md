# asktable-mcp-server

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/asktable-mcp-server.svg)](https://pypi.org/project/asktable-mcp-server/)

`asktable-mcp-server` 是一个为 [AskTable](https://www.asktable.com/) 提供的 MCP 服务。它允许用户通过 AskTable 的接口与数据库进行交互，执行查询和获取数据。

## 快速开始

### 安装与配置
本地先安装uv工具，然后克隆该项目到本地
```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```
## 使用
目前支持stdio本地通信，你可以通过 AskTable 的客户端与 asktable-mcp-server 进行交互，执行查询和获取数据。


### MCP Server 配置示例
现已经支持[VS Code + Cline](https://cline.bot/)， [Trae](https://www.trae.com.cn/)， [百炼MCP平台](https://bailian.console.aliyun.com/?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.6483521cesAnkN&tab=mcp#/mcp-market)
```json
{
    "mcpServers":{
        "asktable-mcp-server":{
            "command":"uvx",
            "args":[
                "asktable-mcp-server@latest"
            ],
            "env":{
                "api_key": "your api_key",
                "datasouce_id": "your datasouce_id"
                 }
                }
            }
}
```