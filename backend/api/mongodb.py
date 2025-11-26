from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
from typing import List, Dict, Any
from config import config

class MongoDB:
    def __init__(self):
        """
        Initialize the MongoDB client
        """
        try:
            self._client = MongoClient(
                config.MONGODB_URL,
                maxPoolSize=10,
                minPoolSize=1,
                maxIdleTimeMS=30000,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

    def get_database(self, database_name: str) -> Database:
        """
        Get a database
        """
        return self._client[database_name]
    
    def get_collection(self, database_name: str, collection_name: str) -> Collection:
        """
        Get a collection
        """
        return self.get_database(database_name)[collection_name]
    
    def _convert_id_to_objectid(self, filter_dict: Dict[str, Any]) -> None:
        """
        將 filter_dict 中的字串 _id 轉換為 ObjectId
        
        Args:
            filter_dict: 查詢條件字典
        """
        if "_id" in filter_dict and isinstance(filter_dict["_id"], str):
            try:
                filter_dict["_id"] = ObjectId(filter_dict["_id"])
            except Exception as e:
                raise Exception(f"Error converting _id to ObjectId: {str(e)}")

    def build_query(self, **conditions) -> Dict[str, Any]:
        """
        建立查詢條件
        
        Args:
            **conditions: 查詢條件，格式為 field__operator=value

            例如: email__eq="test@example.com", age__gt=18
        
        Returns:
            查詢條件字典
        """
        operators = {
            'eq': lambda v: v,
            'ne': lambda v: {'$ne': v},
            'gt': lambda v: {'$gt': v},
            'gte': lambda v: {'$gte': v},
            'lt': lambda v: {'$lt': v},
            'lte': lambda v: {'$lte': v},
            'in': lambda v: {'$in': v if isinstance(v, list) else [v]},
            'nin': lambda v: {'$nin': v if isinstance(v, list) else [v]},
            'exists': lambda v: {'$exists': v},
            'regex': lambda v: {'$regex': v, '$options': 'i'},
            'contains': lambda v: {'$regex': v, '$options': 'i'},
            'starts_with': lambda v: {'$regex': f'^{v}', '$options': 'i'},
            'ends_with': lambda v: {'$regex': f'{v}$', '$options': 'i'},
            'all': lambda v: {'$all': v if isinstance(v, list) else [v]},
            'size': lambda v: {'$size': v}
        }
        
        query = {}
        for key, value in conditions.items():
            if '__' in key:
                field, operator = key.split('__', 1)
                if operator in operators:
                    query[field] = operators[operator](value)
            else:
                # 沒有操作符，預設為等於
                query[key] = value
        return query

    def get_data(self, database_name: str, collection_name: str,
            filter_dict: Dict[str, Any] = {}, projection: Dict[str, Any] = {},
            sort_list: List[tuple] = None, limit: int = None, skip: int = None,
            **conditions
        ) -> List[Dict[str, Any]]:
        """
        查詢多個文件
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            filter_dict: 查詢條件 (MongoDB 原生格式)，可選
            projection: 欄位投影，可選
            sort_list: 排序條件列表 [("field", 1), ("field2", -1)]，可選
            limit: 限制返回數量，可選
            skip: 跳過數量，可選
            **conditions: 簡化查詢條件，格式為 field__operator=value
                        例如: email__eq="test@example.com", age__gt=18
        
        Returns:
            文件列表
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            
            # 如果有簡化查詢條件，先轉換為 MongoDB 格式
            if conditions:
                query_conditions = self.build_query(**conditions)
                # 合併 filter_dict 和 conditions
                filter_dict = {**filter_dict, **query_conditions}
            
            self._convert_id_to_objectid(filter_dict)
            
            cursor = collection.find(filter_dict, projection)
            
            if sort_list:
                cursor = cursor.sort(sort_list)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            
            documents = []
            for doc in cursor:
                if "_id" in doc:
                    doc["_id"] = str(doc["_id"])
                documents.append(doc)
                
            return documents
        except Exception as e:
            raise Exception(f"Error finding documents in {database_name}.{collection_name}: {str(e)}")

    def aggregate(self, database_name: str, collection_name: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        聚合查詢
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            pipeline: 聚合管道
            
        Returns:
            聚合結果列表
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            results = list(collection.aggregate(pipeline))
            
            for doc in results:
                if "_id" in doc:
                    doc["_id"] = str(doc["_id"])
                    
            return results
        except Exception as e:
            raise Exception(f"Error aggregating data in {database_name}.{collection_name}: {str(e)}")

    def add_data(self, database_name: str, collection_name: str, document: Dict[str, Any]) -> str:
        """
        插入單一文件
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            document: 要插入的文件
            
        Returns:
            插入的文件 ID
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except Exception as e:
            raise Exception(f"Error inserting document in {database_name}.{collection_name}: {str(e)}")
    
    def add_datas(self, database_name: str, collection_name: str, documents: List[Dict[str, Any]]) -> List[str]:
        """
        插入多個文件
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            documents: 要插入的文件列表
            
        Returns:
            插入的文件 ID 列表
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            result = collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        except Exception as e:
            raise Exception(f"Error inserting documents in {database_name}.{collection_name}: {str(e)}")

    def update_data(self, database_name: str, collection_name: str, filter_dict: Dict[str, Any], update_dict: Dict[str, Any], upsert: bool = False) -> bool:
        """
        更新單一文件
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            filter_dict: 查詢條件
            update_dict: 更新內容
            upsert: 如果不存在是否插入
            
        Returns:
            是否成功更新
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            
            # Convert string _id to ObjectId if present in filter
            self._convert_id_to_objectid(filter_dict)
            
            result = collection.update_one(filter_dict, {"$set": update_dict}, upsert=upsert)
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            raise Exception(f"Error updating document in {database_name}.{collection_name}: {str(e)}")
    
    def update_datas(self, database_name: str, collection_name: str, filter_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> int:
        """
        更新多個文件
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            filter_dict: 查詢條件
            update_dict: 更新內容
            
        Returns:
            更新的文件數量
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            
            # Convert string _id to ObjectId if present in filter
            self._convert_id_to_objectid(filter_dict)
            
            result = collection.update_many(filter_dict, {"$set": update_dict})
            return result.modified_count
        except Exception as e:
            raise Exception(f"Error updating documents in {database_name}.{collection_name}: {str(e)}")

    def delete_data(self, database_name: str, collection_name: str, filter_dict: Dict[str, Any]) -> bool:
        """
        刪除單一文件
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            filter_dict: 查詢條件
            
        Returns:
            是否成功刪除
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            
            # Convert string _id to ObjectId if present in filter
            self._convert_id_to_objectid(filter_dict)
            
            result = collection.delete_one(filter_dict)
            return result.deleted_count > 0
        except Exception as e:
            raise Exception(f"Error deleting document in {database_name}.{collection_name}: {str(e)}")
    
    def delete_datas(self, database_name: str, collection_name: str, filter_dict: Dict[str, Any]) -> int:
        """
        刪除多個文件
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            filter_dict: 查詢條件
            
        Returns:
            刪除的文件數量
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            
            # Convert string _id to ObjectId if present in filter
            self._convert_id_to_objectid(filter_dict)
            
            result = collection.delete_many(filter_dict)
            return result.deleted_count
        except Exception as e:
            raise Exception(f"Error deleting documents in {database_name}.{collection_name}: {str(e)}")

    def count_documents(self, database_name: str, collection_name: str, filter_dict: Dict[str, Any] = {}, **conditions) -> int:
        """
        計算文件數量
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            filter_dict: 查詢條件
            **conditions: 簡化查詢條件，格式為 field__operator=value
            
        Returns:
            文件數量
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            
            # 如果有簡化查詢條件，先轉換為 MongoDB 格式
            if conditions:
                query_conditions = self.build_query(**conditions)
                # 合併 filter_dict 和 conditions
                filter_dict = {**filter_dict, **query_conditions}
            
            self._convert_id_to_objectid(filter_dict)
            
            return collection.count_documents(filter_dict)
        except Exception as e:
            raise Exception(f"Error counting documents in {database_name}.{collection_name}: {str(e)}")
    
    def distinct(self, database_name: str, collection_name: str, field: str, filter_dict: Dict[str, Any] = {}, **conditions) -> List[Any]:
        """
        獲取欄位的唯一值
        
        Args:
            database_name: 資料庫名稱
            collection_name: 集合名稱
            field: 欄位名稱
            filter_dict: 查詢條件
            **conditions: 簡化查詢條件，格式為 field__operator=value
            
        Returns:
            唯一值列表
        """
        try:
            collection = self.get_collection(database_name, collection_name)
            
            # 如果有簡化查詢條件，先轉換為 MongoDB 格式
            if conditions:
                query_conditions = self.build_query(**conditions)
                # 合併 filter_dict 和 conditions
                filter_dict = {**filter_dict, **query_conditions}
            
            self._convert_id_to_objectid(filter_dict)
            
            return collection.distinct(field, filter_dict)
        except Exception as e:
            raise Exception(f"Error getting distinct values in {database_name}.{collection_name}: {str(e)}")

    def close(self):
        """
        Close the MongoDB client
        """
        if self._client:
            self._client.close()

mongodb = MongoDB()