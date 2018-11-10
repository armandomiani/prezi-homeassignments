// set the createdAt as UTC
//   and moves the id attribute to avoid conflict with the reserved _id
var bulk = db.prezies.initializeUnorderedBulkOp();
db.prezies.find({}).forEach(function (row) {
    bulk.find({'_id': row._id}).update({
        $set: {
            utcCreatedAt: new Date(row.createdAt),
            prezi_id: row.id
        },
        $unset: {
            id: ""
        }
    });
});
bulk.execute();

// creates an index for full-text
//   italian-language cause the text its in latin :)
db.prezies.createIndex(
    { title: "text" },
    { 
        default_language: "it",
        weights: {
           title: 10 
        }
    }
);