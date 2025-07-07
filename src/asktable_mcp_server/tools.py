from asktable import Asktable
import json


async def get_asktable_data(
    api_key, datasource_id, question, base_url=None, role_id: str=None, role_variables: dict = None
):
    """
    获取asktable数据
    :param api_key:
    :param datasource_id:
    :param question:
    :param base_url:
    :param role_id:
    :param role_variables:
    :return:
    """

    asktable_client = Asktable(api_key=api_key, base_url=base_url)
    answer_response = asktable_client.answers.create(
        datasource_id=datasource_id, 
        question=question, 
        role_id=role_id,
        role_variables=role_variables
    )
    if answer_response.answer is None:
        return "没有查询到相关信息"
    return answer_response.answer.text


async def get_asktable_sql(
    api_key, datasource_id, question, base_url=None, role_id: str=None, role_variables: dict = None
):

    asktable_client = Asktable(api_key=api_key, base_url=base_url)
    query_response = asktable_client.sqls.create(
        datasource_id=datasource_id, 
        question=question, 
        role_id=role_id,
        role_variables=role_variables
    )
    if query_response.query is None:
        return "没有查询到相关信息"
    return query_response.query.sql


async def get_datasources_info(api_key, base_url=None):
    """ "
    返回用户数据库meta_data;
    若输入roleid，则返回该角色可访问的数据库meta_data
    若不输入roleid，则返回所有数据库meta_data
    args:
        api_key: str
        base_url: str
    return:
        {
            "status": "success" or "failure",
            "data": json.dumps(result, ensure_ascii=False, indent=2)
        }
    """
    asktable_client = Asktable(api_key=api_key, base_url=base_url)

    meta_data_list = asktable_client.datasources.list()
    if not meta_data_list.items:
        return {
            "status": "failure",
            "data": "该用户还没有创建任何数据库"
        }
    result = [
        {
            "datasource_id": ds.id,
            "数据库名称": ds.name,
            "数据库引擎": ds.engine,
            "数据库描述": ds.desc,
        }
        for ds in meta_data_list.items
    ]
    return {
        "status": "success",
        "data": json.dumps(result, ensure_ascii=False, indent=2)
    }

