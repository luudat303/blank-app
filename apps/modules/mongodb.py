#-*- encoding: utf-8 -*-

import pymongo

class MongoDBUtil:
 
    def __init__(self, authentication_string=None,db_name=None):
        
        self.client = pymongo.MongoClient(authentication_string)
        self.database = self.client[db_name]

    def __del__(self):
        # print("__del__")
        self.client.close()

    def create_database(self, db_name):
        return self.client.get_database(db_name)

    def drop_database(self, db_name):
        return self.client.drop_database(db_name)

    def select_database(self, db_name):
        self.database = self.client[db_name]
        return self.database

    def get_database(self, db_name):
        # return self.client[db_name]
        return self.client.get_database(db_name)

    def list_database_names(self):
        return self.client.list_database_names()

    def create_collection(self, collect_name):
        collect = self.database.get_collection(collect_name)
        if(collect is not None):
            print("collection %s already exists" % collect_name)
            return collect
        return self.database.create_collection(collect_name)

    def drop_collection(self, collect_name):
        return self.database.drop_collection(collect_name)

    def get_collection(self, collect_name):
        return self.database.get_collection(collect_name)

    def list_collection_names(self):
        return self.database.list_collection_names()

    def insert(self, collect_name, documents):
        return self.database.get_collection(collect_name).insert(documents)

    def insert_one(self, collect_name, document):
        return self.database.get_collection(collect_name).insert_one(document)

    def insert_many(self, collect_name, documents):
        return self.database.get_collection(collect_name).insert_many(documents)

    def delete_one(self, collect_name, filter, collation=None, hint=None, session=None):
        return self.database.get_collection(collect_name).delete_one(filter, collation, hint, session)

    def delete_many(self, collect_name, filter, collation=None, hint=None, session=None):
        return self.database.get_collection(collect_name).delete_many(filter, collation, hint, session)

    def find_one_and_delete(self, collect_name, filter, projection=None, sort=None, hint=None, session=None, **kwargs):
        return self.database.get_collection(collect_name).find_one_and_delete(filter, projection, sort, hint, session, **kwargs)

    def count_documents(self, collect_name, filter, session=None, **kwargs):
        return self.database.get_collection(collect_name).count_documents(filter, session, **kwargs)

    def find_one(self, collect_name, filter=None, *args, **kwargs):
        return self.database.get_collection(collect_name).find_one(filter, *args, **kwargs)

    def find(self, collect_name, *args, **kwargs):
        return self.database.get_collection(collect_name).find(*args, **kwargs)

    def update(self, collect_name, spec, document, upsert=False, manipulate=False,
               multi=False, check_keys=True, **kwargs):
        return self.database.get_collection(collect_name).update(spec, document,
                                upsert, manipulate, multi, check_keys, **kwargs)

    def update_one(self, collect_name, filter, update, upsert=False, bypass_document_validation=False,
                                collation=None, array_filters=None, hint=None, session=None):
        return self.database.get_collection(collect_name).update_one(filter, update,
                                upsert, bypass_document_validation, collation, array_filters, hint, session)

    def update_many(self, collect_name, filter, update, upsert=False, array_filters=None,
                                bypass_document_validation=False, collation=None, hint=None, session=None):
        return self.database.get_collection(collect_name).update_many(filter, update,
                                upsert, array_filters, bypass_document_validation, collation, hint, session)

    def find_one_and_update(self, collect_name, filter, update, projection=None, sort=None, upsert=False,
                           return_document=False, array_filters=None, hint=None, session=None, **kwargs):
        return self.database.get_collection(collect_name).find_one_and_update(filter, update, projection,
                                sort, upsert, return_document, array_filters, hint, session, **kwargs)

authen_string="""mongodb://ADMIN:9HtZUabEhLqY@GC75055711DD49C-MHB60I7QXIM7XU82.adb.us-sanjose-1.oraclecloudapps.com:27017/admin?authMechanism=PLAIN&authSource=$external&ssl=true&retryWrites=false&loadBalanced=true"""
mongo_cli=MongoDBUtil(authentication_string=authen_string)