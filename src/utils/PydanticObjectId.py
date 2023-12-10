from bson import ObjectId


class PydanticObjectId(ObjectId):
    @classmethod
    def __get_validators(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v

        if ObjectId.is_valid(v):
            return ObjectId(v)

        raise ValueError("ObjectId required")
