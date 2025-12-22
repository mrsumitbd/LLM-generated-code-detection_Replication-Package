import json
from redis.asyncio.client import Redis
from app.common.enums import RedisInitKeyConfig
from app.utils.excel_util import ExcelUtil
from typing import Any, List, Dict, Optional
from app.core.database import AsyncSessionLocal
from app.core.base_schema import BatchSetAvailable
from app.core.redis_crud import RedisCURD
from app.core.exceptions import CustomException
from app.core.logger import logger
from .schema import DictDataCreateSchema,DictDataOutSchema,DictDataUpdateSchema,DictTypeCreateSchema,DictTypeOutSchema,DictTypeUpdateSchema
from .param import DictDataQueryParam, DictTypeQueryParam
from .crud import DictDataCRUD, DictTypeCRUD
from app.api.v1.module_system.auth.schema import AuthSchema

class DictDataService:
    """
    字典数据管理模块服务层
    """
    
    @classmethod
    async def get_obj_detail_service(cls, auth: AuthSchema, id: int) -> Dict:
        """
        获取数据字典数据详情
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - id (int): 数据字典数据ID
        
        返回:
        - Dict: 数据字典数据详情字典
        """
        obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def get_obj_list_service(cls, auth: AuthSchema, search: Optional[DictDataQueryParam] = None, order_by: Optional[List[Dict[str, str]]] = None) -> List[Dict]:
        """
        获取数据字典数据列表
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - search (DictDataQueryParam | None): 搜索条件模型
        - order_by (List[Dict[str, str]] | None): 排序字段列表
        
        返回:
        - List[Dict]: 数据字典数据详情字典列表
        """
        obj_list = await DictDataCRUD(auth).get_obj_list_crud(search=search.__dict__, order_by=order_by)
        return [DictDataOutSchema.model_validate(obj).model_dump() for obj in obj_list]

    @classmethod
    async def init_dict_service(cls, redis: Redis):
        """
        应用初始化: 获取所有字典类型对应的字典数据信息并缓存service
        
        参数:
        - redis (Redis): Redis客户端
        
        返回:
        - None
        """
        async with AsyncSessionLocal() as session:
            async with session.begin():
                auth = AuthSchema(db=session)
                obj_list = await DictTypeCRUD(auth).get_obj_list_crud()
                if not obj_list:
                    logger.warning("❗️ 未找到任何字典类型数据")
                    return
                for obj in obj_list:
                    dict_type = obj.dict_type
                    dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': dict_type})
                    
                    if not dict_data_list:
                        logger.warning(f"❗️ 字典类型 {dict_type} 未找到对应的字典数据")
                        continue
                    
                    dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
                    # 保存到Redis并设置过期时间
                    redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{dict_type}"
                    try:
                        value = json.dumps(dict_data, ensure_ascii=False)
                        await RedisCURD(redis).set(
                                key=redis_key,
                                value=value,
                            )
                    except Exception as e:
                        logger.error(f"❌️ 初始化字典数据失败: {e}")
                        raise CustomException(msg=f"初始化字典数据失败 {e}")
    
    @classmethod
    async def get_init_dict_service(cls, redis: Redis, dict_type: str)->List[Dict]:
        """
        从缓存获取字典数据列表信息service
        
        参数:
        - redis (Redis): Redis客户端
        - dict_type (str): 字典类型
        
        返回:
        - List[Dict]: 字典数据列表
        """
        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{dict_type}"
        obj_list_dict = await RedisCURD(redis).get(redis_key)
        if not obj_list_dict:
            raise CustomException(msg="数据字典不存在")
        return obj_list_dict

    @classmethod
    async def create_obj_service(cls, auth: AuthSchema, redis: Redis, data: DictDataCreateSchema) -> Dict:
        """
        创建数据字典数据
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - data (DictDataCreateSchema): 数据字典数据创建模型
        
        返回:
        - Dict: 数据字典数据详情字典
        """
        exist_obj = await DictDataCRUD(auth).get(dict_label=data.dict_label)
        if exist_obj:
            raise CustomException(msg='创建失败，该字典数据已存在')
        obj = await DictDataCRUD(auth).create_obj_crud(data=data)

        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                )
            logger.info(f"创建字典数据写入缓存成功: {obj}")
        except Exception as e:
            logger.error(f"创建字典数据写入缓存失败: {e}")
            raise CustomException(msg=f"创建字典数据失败 {e}")

        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def update_obj_service(cls, auth: AuthSchema, redis: Redis, id:int, data: DictDataUpdateSchema) -> Dict:
        """
        更新数据字典数据
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - id (int): 数据字典数据ID
        - data (DictDataUpdateSchema): 数据字典数据更新模型
        
        返回:
        - Dict: 数据字典数据详情字典
        """
        exist_obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
        if not exist_obj:
            raise CustomException(msg='更新失败，该字典数据不存在')

        if exist_obj.id != id:
            raise CustomException(msg='更新失败，数据字典数据重复')
            
        # 如果字典类型变更，仅刷新旧类型缓存，不联动字典类型状态
        if exist_obj.dict_type != data.dict_type:
            dict_type = await DictTypeCRUD(auth).get(dict_type=exist_obj.dict_type)
            if dict_type:
                redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{dict_type.dict_type}"
                try:
                    dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': dict_type.dict_type})
                    dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
                    value = json.dumps(dict_data, ensure_ascii=False)
                    await RedisCURD(redis).set(
                            key=redis_key,
                            value=value,
                        )
                except Exception as e:
                    logger.error(f"更新字典数据类型变更时刷新旧缓存失败: {e}")
                
        obj = await DictDataCRUD(auth).update_obj_crud(id=id, data=data)
        redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{data.dict_type}"
        try:
            # 获取当前字典类型的所有字典数据
            dict_data_list = await DictDataCRUD(auth).get_obj_list_crud(search={'dict_type': data.dict_type})
            dict_data = [DictDataOutSchema.model_validate(row).model_dump() for row in dict_data_list if row]
            
            value = json.dumps(dict_data, ensure_ascii=False)
            await RedisCURD(redis).set(
                    key=redis_key,
                    value=value,
                )
            logger.info(f"更新字典数据写入缓存成功: {obj}")
        except Exception as e:
            logger.error(f"更新字典数据写入缓存失败: {e}")
            raise CustomException(msg=f"更新字典数据失败 {e}")

        return DictDataOutSchema.model_validate(obj).model_dump()
    
    @classmethod
    async def delete_obj_service(cls, auth: AuthSchema, redis: Redis, ids: list[int]) -> None:
        """
        删除数据字典数据
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - redis (Redis): Redis客户端
        - ids (list[int]): 数据字典数据ID列表
        
        返回:
        - None
        """
        if len(ids) < 1:
            raise CustomException(msg='删除失败，删除对象不能为空')
        
        for id in ids:

            exist_obj = await DictDataCRUD(auth).get_obj_by_id_crud(id=id)
            if not exist_obj:
                raise CustomException(msg=f'{id} 删除失败，该字典数据不存在')
            # 新增：系统默认字典数据不允许删除（通过 is_default 判断）
            if exist_obj.is_default:
                raise CustomException(msg='删除失败，系统默认字典数据不允许删除')
            # 删除Redis缓存
            redis_key = f"{RedisInitKeyConfig.SYSTEM_DICT.key}:{exist_obj.dict_type}"
            try:
                # 删除Redis缓存
                await RedisCURD(redis).delete(redis_key)
                logger.info(f"删除字典数据成功: {id}")
            except Exception as e:
                logger.error(f"删除字典数据失败: {e}")
                raise CustomException(msg=f"删除字典数据失败 {e}")
        await DictDataCRUD(auth).delete_obj_crud(ids=ids)

    @classmethod
    async def set_obj_available_service(cls, auth: AuthSchema, data: BatchSetAvailable) -> None:
        """
        批量修改数据字典数据状态
        
        参数:
        - auth (AuthSchema): 认证信息模型
        - data (BatchSetAvailable): 批量修改数据字典数据状态负载模型
        
        返回:
        - None
        """
        await DictDataCRUD(auth).set_obj_available_crud(ids=data.ids, status=data.status)

    @classmethod
    async def export_obj_service(cls, data_list: List[Dict[str, Any]]) -> bytes:
        """
        导出数据字典数据列表
        
        参数:
        - data_list (List[Dict[str, Any]]): 数据字典数据列表
        
        返回:
        - bytes: Excel文件字节流
        """
        mapping_dict = {
            'id': '编号',
            'dict_sort': '字典排序', 
            'dict_label': '字典标签', 
            'dict_value': '字典键值', 
            'dict_type': '字典类型',
            'css_class': '样式属性', 
            'list_class': '表格回显样式', 
            'is_default': '是否默认', 
            'status': '状态',
            'description': '备注',
            'created_at': '创建时间',
            'updated_at': '更新时间',
            'creator_id': '创建者ID',
            'creator': '创建者',
        }

        # 复制数据并转换状态
        data = data_list.copy()
        for item in data:
            # 处理状态
            item['status'] = '正常' if item.get('status') else '停用'
            # 处理是否默认
            item['is_default'] = '是' if item.get('is_default') else '否'
            item['creator'] = item.get('creator', {}).get('name', '未知') if isinstance(item.get('creator'), dict) else '未知'

        return ExcelUtil.export_list2excel(list_data=data, mapping_dict=mapping_dict)