db = db.getSiblingDB("ELANDB");
db.createUser({
  user: process.env.MONGO_ELANDB_USERNAME,
  pwd:  process.env.MONGO_ELANDB_PASSWORD,
  roles: [{ role: "readWrite", db: "ELANDB" }]
});
