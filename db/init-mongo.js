db.createUser(
    {
        user: "crpytoRW",
        pwd: "cryptotestpls",
        roles: [
            {
                role: "readWrite",
                db: "crypto"
            }
        ]
    }
)