"""Creates indexes for mongodb when imported"""


from db import collections


# users
collections.users.create_index(
    {"email": 1},
    partialFilterExpression={"email": {"$ne": None}}
)
