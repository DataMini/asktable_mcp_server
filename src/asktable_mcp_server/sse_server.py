
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Annotated, Dict, Any, Optional

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse
import fastmcp
from pydantic import Field

from asktable_mcp_server.tools import (
    get_asktable_answer,
    get_asktable_sql,
)
from asktable_mcp_server.version import __version__

# 配置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 全局变量
server_ready = False
mcp = None  # 将在 main 函数中初始化


@asynccontextmanager
async def lifespan(fastmcp_instance):
    """服务器启动和关闭的生命周期管理"""
    global server_ready

    # 启动逻辑
    logger.info("服务器正在初始化...")

    await asyncio.sleep(2)

    server_ready = True
    logger.info("服务器初始化完成，准备接受请求")

    yield  # 服务器运行期间

    # 关闭逻辑
    logger.info("服务器正在关闭...")
    server_ready = False


def create_mcp_server(path_prefix: str = "", base_url: str = None):
    """创建 MCP 服务器实例"""
    global mcp

    
    # 创建服务器时传入 lifespan
    mcp = FastMCP(
        name="AskTable SSE MCP Server",
        lifespan=lifespan,
    )

    @mcp.custom_route(path_prefix + "/health", methods=["GET"])
    async def health_check(request: Request):
        """Health check endpoint to verify server is ready"""
        if not server_ready:
            return JSONResponse({"status": "initializing", "message": "Server is still initializing"})
        return JSONResponse({"status": "ready", "message": "Server is initialized and ready"})

    @mcp.custom_route(path_prefix + "/", methods=["GET"])
    async def home(request: Request):
        """Welcome page with configuration example"""
        # 从请求中获取主机名
        host = request.headers.get("host", "your-asktable-server-host") 
        scheme = request.url.scheme
        base_url = f"{scheme}://{host}"
        
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>AskTable MCP 服务（SSE）</title>
            <style>
                body {{
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                    line-height: 1.6;
                }}
                pre {{
                    background: #f5f5f5;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                code {{
                    white-space: pre-wrap;
                }}
                h1, h2 {{
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }}
                ul {{
                    padding-left: 20px;
                }}
            </style>
        </head>
        <body>
            <h1>欢迎访问 AskTable MCP 服务（SSE）!</h1>
            <p>当前版本: v{__version__}</p>

            <h2>配置示例</h2>
            <p>在您的 Agent 配置文件中，添加以下配置:</p>
            <pre><code>{{
    "mcpServers": {{
        "asktable": {{
            "type": "sse",
            "url": "{base_url}{path_prefix}/sse/?apikey=YOUR_API_KEY&datasource_id=YOUR_DATASOURCE_ID",
            "headers": {{}},
            "timeout": 300,
            "sse_read_timeout": 300
        }}
    }}
}}</code></pre>

            <h2>工具</h2>
            <ul>
                <li>使用 AskTable 生成 SQL</li>
                <li>使用 AskTable 查询数据</li>
                <li>列出 AskTable 中的所有数据</li>
            </ul>
            <h2>帮助文档</h2>
            <p>更多详细信息，请访问 <a href="https://docs.asktable.com/docs/integration/mcp/use-asktable-mcp">使用 MCP 访问 AskTable</a></p>
        </body>
        </html>
        """
        return HTMLResponse(content=content)

    @mcp.tool(name="使用 AskTable 生成 SQL")
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
        global server_ready

        if not server_ready:
            return "Server is still initializing, please wait"

        request = get_http_request()
        api_key = request.query_params.get("apikey", None)
        datasource_id = request.query_params.get("datasource_id", None)

        logging.info(f"api_key:{api_key}")
        logging.info(f"datasource_id:{datasource_id}")
        logging.info(f"role_id:{role_id}")
        logging.info(f"role_variables:{role_variables}")

        params = {
            "api_key": api_key,
            "datasource_id": datasource_id,
            "question": question,
            "base_url": base_url,
            "role_id": role_id,
            "role_variables": role_variables,
        }

        message = await get_asktable_sql(**params)
        return message

    @mcp.tool(name="使用 AskTable 查询数据")
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
        global server_ready

        if not server_ready:
            return "Server is still initializing, please wait"

        request = get_http_request()
        api_key = request.query_params.get("apikey", None)
        datasource_id = request.query_params.get("datasource_id", None)

        params = {
            "api_key": api_key,
            "datasource_id": datasource_id,
            "question": question,
            "base_url": base_url,
            "role_id": role_id,
            "role_variables": role_variables,
        }

        message = await get_asktable_answer(**params)
        return message


    return mcp


def main(base_url: str = None, path_prefix: str = "", port: int = 8095):
    """
    启动 SSE 服务器的主函数
    
    :param base_url: 请求所用的服务器主机地址，填写了则使用指定服务器地址，否则使用默认的AskTable服务地址
    :param path_prefix: 路径前缀，用于在反向代理环境中设置正确的路径（如：/mcp）
    :param port: 服务器端口号
    """
    global mcp

    fastmcp.settings.sse_path = path_prefix + "/sse/"
    fastmcp.settings.message_path = path_prefix + "/messages/"
    
    # 创建 MCP 服务器实例
    mcp = create_mcp_server(path_prefix=path_prefix, base_url=base_url)
    
    # 记录配置信息
    logger.info("启动 SSE 服务器")
    logger.info(f"base_url: {base_url}")
    logger.info(f"path_prefix: {path_prefix}")
    logger.info(f"port: {port}")


    # 启动服务器
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port,
        path=fastmcp.settings.sse_path,
    )


if __name__ == "__main__":
    print("Please use the server.py file to start the SSE server")
