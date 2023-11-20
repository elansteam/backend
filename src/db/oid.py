from bson import ObjectId


class OID(str):
    """Расширенный класс ObjectId с возможностью валидации"""

    def __new__(cls, v):
        if v == '':
            raise ValueError('ObjectId is empty')
        if ObjectId.is_valid(v) is False:
            raise ValueError('ObjectId invalid')
        return str(v)
