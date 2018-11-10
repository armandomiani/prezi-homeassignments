#!/bin/bash

echo "Dropping database..."
mongo ${DB_HOST}:27017/prezi --eval 'db.prezies.drop();'
echo "Importing Collections..."
mongoimport --host ${DB_HOST}:27017 --db prezi --collection prezies --file /work/seed.json --jsonArray
echo "Updating the seed data..."
mongo ${DB_HOST}:27017/prezi /work/bulk-mongo.js
echo "Database is ready!"
tail -f /dev/null
