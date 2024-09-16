rs.initiate({_id: 'rs0', members: [{ _id: 0, host: `${process.env.MONGO_HOSTNAME}:27017` }]})

while (!db.hello().isWritablePrimary) {sleep(1000)}

var adminDB = db.getSiblingDB(process.env.MONGO_INITDB_ROOT_DATABASE);
adminDB.createUser({
    user: process.env.MONGO_INITDB_ROOT_USERNAME,
    pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
    roles: [{ role: 'root', db: 'admin' }]
});

adminDB.auth(process.env.MONGO_INITDB_ROOT_USERNAME, process.env.MONGO_INITDB_ROOT_PASSWORD);
var dbName = db.getSiblingDB(process.env.COMMON_DATABASE);

adminDB.createUser({
    user: process.env.COMMON_USERNAME,
    pwd: process.env.COMMON_PASSWORD,
    roles: [{ role: 'readWrite', db: process.env.COMMON_DATABASE }]
});
