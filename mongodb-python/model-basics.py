from motor import motor_asyncio

# create a single instance of `AsyncIOMotorClient` at the time your application starts up.
client = motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

# A single instance of MongoDB can support multiple independent databases.
db = client.sample_metro

# 1. Find One
async def find_one(id:int):
    """
    Find One
    ----
    id:int
      This function return only value, given the id
    """
    assert isinstance(id, int), "id must integer"
    # Getting a collection called `products` and find one
    result = await db.products.find_one({"data_id":id}, {"_id":0})
    if result:
        return result
    else:
        print('No exist id')
        return result

# 2. Insert One

async def insert_one(document:dict):
    assert isinstance(document, dict), "document must be `dict` data type"
    # Getting a collection called `products` 
    result = await db.products.insert_one(document)
    print(result.inserted_id)
    

# 3. Delete One

async def delete_one(id:int):
    
    assert isinstance(id, int), "id must be `int` data type"
    products = db.products
    n = await products.count_documents({})
    print('%s documents before calling delete_one()' % n)
    result = await db.products.delete_one({"data_id":id})
    print('%s documents after' % (await products.count_documents({})))

# 4. Update One

async def update_one(id:int, field):

    assert isinstance(field, dict), "document must be `dict` data type"
    assert isinstance(id, int), "id must be `int` data type"

    result = await db.products.update_one({"data_id":id}, {"$set":field})
    print('replaced %s document' % result.modified_count)


if __name__ == "__main__":
    loop = client.get_io_loop()
    
    # 1. Find One 
    data_id = 8615
    # Run
    product_only = loop.run_until_complete(find_one(data_id))
    print(product_only)

    # 2. Insert One
    document = dict(data_id = 8615,
        data_price = 9.5,
        data_brand = "Metro",
        data_uri = "https://wongfood.vteximg.com.br/arquivos/ids/209986-230-230/PETIT-PAN-X-25UN-PI---COCA-COLA-15L-CON-PETIT---COCACOLA-1-6797.jpg?v=636546708534830000",
        data_name = "Gaseosa Coca Cola Botella 1.5 Lt + Petit Pan La Panadería Bolsa 25 unid",
        data_category ="panes-embolsados")
    # Run 
    # loop.run_until_complete(insert_one(document))
    
    # 3. Delete One 
    data_id = 8615
    # Run
    # loop.run_until_complete(delete_one(data_id))

    # 4. Replace One
    data_id = 8615
    field = {"data_brand":"La Leña"}
    # Run
    # loop.run_until_complete(update_one(id=data_id, field=field))


    