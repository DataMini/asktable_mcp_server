# asktable-mcp-server

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PyPI Version](https://img.shields.io/pypi/v/asktable-mcp-server.svg)](https://pypi.org/project/asktable-mcp-server/)

`asktable-mcp-server` 是一个为 [AskTable](https://github.com/asktable/asktable) 提供的 MCP (Magic Cloud Platform) 服务。它允许用户通过 AskTable 的接口与数据库进行交互，执行查询和获取数据。

## 快速开始

### 安装与配置
本地先安装uv工具，然后克隆该项目到本地


### 使用
目前支持stdio本地通信，你可以通过 AskTable 的客户端与 asktable-mcp-server 进行交互，执行查询和获取数据。


### MCP Server 配置示例
```json
{
    "mcpServers":{
        "asktable-mcp-server":{
            "command":"uv",
            "args":[
                "--directory",
                "克隆该项目所在路径/src/asktable-mcp-server/",
                "run",
                "server.py"
            ],
            "env":{
                "api_key": "your_api_key",
                "datasouce_id": "your_datasource_id",
                 }
                }
            }
}
```