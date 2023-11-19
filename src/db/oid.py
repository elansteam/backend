from bson import ObjectId


class OID(str):
    """Extended ObjectID class with validation"""
    def __new__(cls, v):
        if v == '':
            raise ValueError('ObjectId is empty')
        if ObjectId.is_valid(v) is False:
            raise ValueError('ObjectId is invalid')
        return str(v)
