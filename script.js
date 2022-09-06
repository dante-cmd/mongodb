use "to_model_sales"
// ------------------------------
// Change the datatype of fields
// ------------------------------

db.product_data.find().forEach( 
    function (x) { 
        if (x['ProductId'] !== null){
            x['ProductId'] = new NumberInt(x['ProductId'])};
                
    db.product_data.save(x);
  });

db.sales_data.find().forEach( 
    function (x) { 
        if (x['Date'] !== null){
            x['Date'] = new ISODate(x['Date'])};
                
    db.sales_data.save(x);
  });

// ---------------------------------------------------------------
//  Compute the discount taking the difference between the prices.
// --------------------------------------------------------------

var pipeline = [
    {$set:{'division_to_discount':{$divide: ['$price-main-md', '$original-price']}}},
    {$set:{'discount':{$subtract: [1, '$division_to_discount']} }},
    {$unset:['division_to_discount'] }]

db.product_data.updateMany(
    {'original-price':{$gt:0}}, 
    pipeline)

// ---------------
// cluster by Age
// ---------------

var pipeline = [
    {$set:{"class_age":{$switch:
        {
            branches:[
                {
                    case:{$gte:["$Age", 50]},
                    then: ">=50"
                },
                {
                    case:{$gte:["$Age", 45]},
                    then: ">=45|<50"
                },
                {
                    case:{$gte:["$Age", 35]},
                    then: ">=35|<45"
                },
                {
                    case:{$gte:["$Age", 20]},
                    then: ">=20|<35"
                }
            ],
            default:"<20"
        }}}}
]

db.user_data.updateMany({'Age':{$gt:0}}, pipeline)

//compute the sales amount grouping by score of sellers.

pipeline = [
    {$lookup: {
            from: "product_data",
            localField: "Items.ProductId", 
            foreignField: "ProductId",
            as: "ProductKey"}}, 
        
        {$unwind: "$ProductKey"},
        {$unwind: "$Items"},
    {
        "$group": { _id: "$ProductKey.seller.score", "Total":{$sum:"$Items.Amount"}
            
        }
        
    },
    {$sort: {"Total":-1}}
    ]
db.sales_data.aggregate(pipeline)
    