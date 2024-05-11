"""Creating indexes for mongodb"""

from db import collections


def create_indexes():
    """Creating indexes for mongodb"""

    # users
    collections.users.create_index(
        {"email": 1},
        partialFilterExpression={"email": {"$ne": None}}
    )
    # contests
    collections.contests.create_index(
        {
            "group_id": 1,
            "local_domain": 1
        }
    )
