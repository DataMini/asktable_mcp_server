import argparse
import os
from typing import Annotated, Dict, Any, Optional
from pydantic import Field
from fastmcp import FastMCP

from asktable_mcp_server.tools import (
    get_asktable_answer,
    get_asktable_sql,
)
from asktable_mcp_server.sse_server import main as sse_main

mcp = FastMCP(name="Asktable stdio mcp server running...")


@mcp.tool(name='使用 AskTable 生成 SQL')
async def gen_sql(
    question: Annotated[str, Field(description="用户的自然语言查询描述。示例：生成查询昨天订单总金额的SQL、写一个SQL查询销售额前10的产品、帮我写一个统计各部门员工数量的SQL")],
    role_id: Annotated[Optional[str], Field(description="角色ID，用于访问控制，当需要进行精细化的数据访问控制时使用。示例：'role_123456'，可以为空（使用默认权限）。详见：https://docs.asktable.com/docs/role-and-permission-management/introduction")] = None,
    role_variables: Annotated[Optional[Dict[str, Any]], Field(description="角色变量，用于角色访问控制时的变量传递。示例：{'employee_id': 2}（限定员工可见范围）或{'department_id': 'dept_001'}（限定部门可见范围），可以为空（不使用变量限制）")] = None
) -> dict:
    """
    将自然语言查询转换为标准SQL语句。
    这是一个智能SQL生成工具，可以理解用户的自然语言描述，并生成相应的SQL查询语句。
    该工具仅返回SQL文本，不会执行查询操作。

    适用场景：
        - 需要将业务需求快速转换为SQL查询语句
        - 在执行查询前想要检查和验证SQL语句
        - 需要获取SQL语句用于其他系统或工具
        - 学习或理解如何编写特定查询的SQL语句
    """
    # 构建基本参数
    params = {
        "api_key": os.getenv("API_KEY"),
        "datasource_id": os.getenv("DATASOURCE_ID"),
        "question": question,
        "base_url": os.getenv("BASE_URL") or None,
        "role_id": role_id,
        "role_variables": role_variables,
    }

    # 调用API获取SQL
    message = await get_asktable_sql(**params)
    return message


@mcp.tool(name='使用 AskTable 查询数据')
async def query(
    question: Annotated[str, Field(description="用户的自然语言查询描述。示例：查询昨天订单总金额、查询销售额前10的产品、统计各部门员工数量")],
    role_id: Annotated[Optional[str], Field(description="角色ID，用于访问控制，当需要进行精细化的数据访问控制时使用。示例：'role_123456'，可以为空（使用默认权限）。详见：https://docs.asktable.com/docs/role-and-permission-management/introduction")] = None,
    role_variables: Annotated[Optional[Dict[str, Any]], Field(description="角色变量，用于角色访问控制时的变量传递。示例：{'employee_id': 2}（限定员工可见范围）或{'department_id': 'dept_001'}（限定部门可见范围），可以为空（不使用变量限制）")] = None
) -> dict:
    """
    将自然语言查询转换为实际数据结果。
    这是一个智能数据查询工具，可以理解用户的自然语言描述，并返回相应的查询结果。

    适用场景：
        - 需要快速获取业务数据的查询结果
        - 直接获取数据分析结果和洞察
        - 需要以自然语言方式查询数据库
        - 获取实时数据报表和统计信息
        - 通过角色访问控制实现数据安全访问
    """
    # 构建基本参数
    params = {
        "api_key": os.getenv("API_KEY"),
        "datasource_id": os.getenv("DATASOURCE_ID"),
        "question": question,
        "base_url": os.getenv("BASE_URL") or None,
        "role_id": role_id,
        "role_variables": role_variables,
    }

    # 调用API获取数据
    message = await get_asktable_answer(**params)
    return message



def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="Asktable MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="选择通信协议: stdio或sse",
    )
    parser.add_argument("--port", type=int, default=8095, help="SSE模式使用的端口号")
    parser.add_argument(
        "--path_prefix",
        type=str,
        default="",
        help="路径前缀，用于在反向代理环境中设置正确的路径（如：/mcp）",
    )
    parser.add_argument(
        "--base_url",
        type=str,
        default=None,
        help="请求所用的AskTable API地址，填写了则使用指定服务器地址，否则使用默认的AskTable API地址",
    )
    args = parser.parse_args()

    # 根据参数启动不同协议
    if args.transport == "stdio":
        mcp.run(transport="stdio")  # 保持原有stdio模式
    else:
        # SSE模式需要额外配置
        sse_main(
            port=args.port,
            base_url=args.base_url,
            path_prefix=args.path_prefix,
        )


if __name__ == "__main__":
    main()
