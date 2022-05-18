module.exports = app => {
    const rock_api = require("../controllers/rock.controller.js");

    var router = require("express").Router();

    // Create a new rock entry
    router.post("/", rock_api.create);

    // Retrieve filtered rock collection
    router.get("/", rock_api.findFiltered);

    // Retrieve a single rock with ID
    router.get("/:id", rock_api.findOne);

    // Delete all tutorials
    router.delete("/", rock_api.deleteAll);

    app.use("/api/rocks", router);
}