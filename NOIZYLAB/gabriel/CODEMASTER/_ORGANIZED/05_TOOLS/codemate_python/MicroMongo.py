from tinydb import TinyDB, Query
from tinydb.operations import set, increment, delete
from tinydb.table import Document


class InsertOneResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class InsertManyResult:
    def __init__(self, inserted_ids):
        self.inserted_ids = inserted_ids


class UpdateResult:
    def __init__(self, matched_count, modified_count, upserted_id=None):
        self.matched_count = matched_count
        self.modified_count = modified_count
        self.upserted_id = upserted_id


class DeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


class TinyMongoCursor:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return iter(self.data)

    def limit(self, n):
        self.data = self.data[:n]
        return self

    def skip(self, n):
        self.data = self.data[n:]
        return self

    # Additional cursor methods can be added here if needed


class TinyMongoCollection:
    def __init__(self, db, name):
        self.table = db.table(name)
        self.query = Query()

    def insert_one(self, document):
        inserted_id = self.table.insert(document)
        return InsertOneResult(inserted_id)

    def insert_many(self, documents):
        inserted_ids = self.table.insert_multiple(documents)
        return InsertManyResult(inserted_ids)

    def find(self, filter=None):
        if filter is None or filter == {}:
            data = self.table.all()
        else:
            condition = self._parse_filter(filter)
            data = self.table.search(condition)
        return TinyMongoCursor(data)

    def find_one(self, filter=None):
        cursor = self.find(filter)
        for doc in cursor:
            return doc
        return None

    def update_one(self, filter, update, upsert=False):
        condition = self._parse_filter(filter)
        docs = self.table.search(condition)
        updated_count = 0
        if docs:
            self._apply_update(docs[0].doc_id, update)
            updated_count = 1
        elif upsert:
            doc = filter.copy()
            self._apply_update_to_document(doc, update)
            inserted_id = self.table.insert(doc)
            return UpdateResult(0, 1, inserted_id)
        return UpdateResult(len(docs), updated_count)

    def update_many(self, filter, update, upsert=False):
        condition = self._parse_filter(filter)
        docs = self.table.search(condition)
        for doc in docs:
            self._apply_update(doc.doc_id, update)
        modified_count = len(docs)
        if not docs and upsert:
            doc = filter.copy()
            self._apply_update_to_document(doc, update)
            inserted_id = self.table.insert(doc)
            return UpdateResult(0, 1, inserted_id)
        return UpdateResult(len(docs), modified_count)

    def replace_one(self, filter, replacement, upsert=False):
        condition = self._parse_filter(filter)
        docs = self.table.search(condition)
        if docs:
            self.table.remove(doc_ids=[docs[0].doc_id])
            inserted_id = self.table.insert(replacement)
            return UpdateResult(1, 1)
        elif upsert:
            inserted_id = self.table.insert(replacement)
            return UpdateResult(0, 1, inserted_id)
        else:
            return UpdateResult(0, 0)

    def delete_one(self, filter):
        condition = self._parse_filter(filter)
        docs = self.table.search(condition)
        if docs:
            self.table.remove(doc_ids=[docs[0].doc_id])
            return DeleteResult(1)
        else:
            return DeleteResult(0)

    def delete_many(self, filter):
        condition = self._parse_filter(filter)
        docs = self.table.search(condition)
        count = len(docs)
        self.table.remove(condition)
        return DeleteResult(count)

    def count_documents(self, filter=None):
        if filter is None or filter == {}:
            return len(self.table)
        else:
            condition = self._parse_filter(filter)
            return len(self.table.search(condition))

    def _parse_filter(self, filter):
        """
        Parses a MongoDB-style filter dictionary into a TinyDB query condition.
        Supports basic comparison and logical operators.
        """
        q = Query()
        conditions = []

        for key, value in filter.items():
            if key == "$or" and isinstance(value, list):
                or_conditions = [self._parse_filter(sub_filter) for sub_filter in value]
                conditions.append(
                    self._combine_conditions(or_conditions, operator="or")
                )
            elif key == "$and" and isinstance(value, list):
                and_conditions = [
                    self._parse_filter(sub_filter) for sub_filter in value
                ]
                conditions.append(
                    self._combine_conditions(and_conditions, operator="and")
                )
            elif isinstance(value, dict):
                for op, v in value.items():
                    if op == "$gt":
                        conditions.append(q[key] > v)
                    elif op == "$gte":
                        conditions.append(q[key] >= v)
                    elif op == "$lt":
                        conditions.append(q[key] < v)
                    elif op == "$lte":
                        conditions.append(q[key] <= v)
                    elif op == "$ne":
                        conditions.append(q[key] != v)
                    elif op == "$in":
                        conditions.append(q[key].one_of(v))
                    elif op == "$nin":
                        conditions.append(q[key].test(lambda x: x not in v))
                    elif op == "$exists":
                        if v:
                            conditions.append(q[key].exists())
                        else:
                            conditions.append(~q[key].exists())
                    # Additional operators can be added here
            else:
                conditions.append(q[key] == value)

        if conditions:
            return self._combine_conditions(conditions, operator="and")
        else:
            return None

    def _combine_conditions(self, conditions, operator="and"):
        """
        Combines multiple TinyDB query conditions using logical AND or OR.
        """
        from functools import reduce
        import operator as op

        if operator == "and":
            return reduce(op.and_, conditions)
        elif operator == "or":
            return reduce(op.or_, conditions)

    def _apply_update(self, doc_id, update):
        for op, fields in update.items():
            if op == "$set":
                for field, value in fields.items():
                    self.table.update(set(field, value), doc_ids=[doc_id])
            elif op == "$inc":
                for field, value in fields.items():
                    self.table.update(increment(field, value), doc_ids=[doc_id])
            # Additional update operators can be added here

    def _apply_update_to_document(self, doc, update):
        """
        Applies update operators directly to a document dictionary.
        Used when upserting a new document.
        """
        for op, fields in update.items():
            if op == "$set":
                doc.update(fields)
            elif op == "$inc":
                for field, value in fields.items():
                    doc[field] = doc.get(field, 0) + value
            # Additional update operators can be added here


class TinyMongoDatabase:
    def __init__(self, path):
        self.db = TinyDB(path)
        self.collections = {}

    def __getitem__(self, name):
        if name not in self.collections:
            self.collections[name] = TinyMongoCollection(self.db, name)
        return self.collections[name]


class TinyMongoClient:
    def __init__(self, path):
        self.databases = {}
        self.path = path

    def __getitem__(self, name):
        if name not in self.databases:
            db_path = f"{self.path}_{name}.json"
            self.databases[name] = TinyMongoDatabase(db_path)
        return self.databases[name]


# Create a function similar to MongoClient in PyMongo
def MongoClient(path="tinydb"):
    return TinyMongoClient(path)


# Usage Example
# if __name__ == '__main__':
#     # Initialize client and database
#     client = MongoClient('my_tinydb')
#     db = client['test_db']  # Access database 'test_db'
#     collection = db['users']  # Access collection 'users'

#     # Insert one document
#     result = collection.insert_one({'name': 'Alice', 'age': 25})
#     print('Inserted ID:', result.inserted_id)

#     # Insert many documents
#     result = collection.insert_many([
#         {'name': 'Bob', 'age': 30},
#         {'name': 'Charlie', 'age': 35}
#     ])
#     print('Inserted IDs:', result.inserted_ids)

#     # Find documents
#     results = collection.find({'age': {'$gt': 25}})
#     print('Documents with age > 25:')
#     for doc in results:
#         print(doc)

#     # Find one document
#     result = collection.find_one({'name': 'Alice'})
#     print('Found document:', result)

#     # Update one document
#     result = collection.update_one({'name': 'Alice'}, {'$set': {'age': 26}})
#     print('Matched:', result.matched_count, 'Modified:', result.modified_count)

#     # Update many documents
#     result = collection.update_many({'age': {'$lt': 30}}, {'$inc': {'age': 1}})
#     print('Matched:', result.matched_count, 'Modified:', result.modified_count)

#     # Delete one document
#     result = collection.delete_one({'name': 'Bob'})
#     print('Deleted count:', result.deleted_count)

#     # Delete many documents
#     result = collection.delete_many({'age': {'$gte': 30}})
#     print('Deleted count:', result.deleted_count)
