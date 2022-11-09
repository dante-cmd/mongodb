from motor import motor_asyncio
import pymongo

# More information in:
# https://motor.readthedocs.io/en/stable/tutorial-tornado.html
# https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_motor_collection.html#motor.motor_asyncio.AsyncIOMotorCollection

# create a single instance of `AsyncIOMotorClient` at the time your application starts up.
client = motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

# A single instance of MongoDB can support multiple independent databases.
db = client.sample_metro


# 1. Find One
async def find_one(id: int):
    """
    Find One
    ----
    id:int
      This function return only value, given the id
    """
    assert isinstance(id, int), "id must integer"
    # Getting a collection called `products` and find one
    result = await db.products.find_one({"data_id": id})

    if result:
        object_id = result.get('_id')
        date_product = object_id.generation_time
        print("The product was created in : ", date_product)

        return result
    else:
        print('No exist id')
        return result


# 2. Delete a Field with Update Many


async def delete_field(field):

    assert isinstance(field, str), "`field` must be a string"
    result = await db.products.update_many({}, {"$unset": {field: 0}})
    print('replaced %s document' % result.modified_count)


# 3. Insert Many

# 4. Delete All Collection


# 5. Aggregate
async def agg(field: str):

    pipeline = [{
        "$group": {
            "_id": "${}".format(field),
            "total": {
                "$avg": "$data_price"
            }
        }
    }, {
        "$sort": {
            "total": 1
        }
    }, {
        "$project": {
            "total": 1,
            "_id": 1
        }
    }]
    async for result in db.products.aggregate(pipeline):
        print(result)


# 6. Top 5 with Aggregate
async def top_5():

    pipeline = [{
        "$sort": {
            "data_price": 1
        }
    }, {
        "$limit": 5
    }, {
        "$project": {
            "data_name": 1,
            "data_price": 1,
            "_id": 0
        }
    }]
    
    # async for result in db.products.aggregate(pipeline):
    #     print(result)
    
    # Other way to get the data
    cursor = db.products.aggregate(pipeline)
    # None point out no constraint
    result = await cursor.to_list(length=None)
    print(result)


if __name__ == "__main__":
    loop = client.get_io_loop()

    # 1. Find One
    data_id = 58468
    # Run
    # product_only = loop.run_until_complete(find_one(data_id))
    # print(product_only)

    # 2. Delete field
    field = "name"
    # loop.run_until_complete(delete_field(field))

    # 5. Aggregation
    field = 'data_brand'
    # Run
    # loop.run_until_complete(agg(field))

    # Top 5
    loop.run_until_complete(top_5())