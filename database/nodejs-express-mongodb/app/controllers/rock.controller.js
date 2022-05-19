const db = require("../models");
const Rock = db.rocks;

// Create and Save a new Rock
exports.create = (req, res) => {
    // Validate request
    if (!req.body.rock_name) {
        res.status(400).send({message: "Must include rock name!"});
        return;
    }
    if (!req.body.classification) {
        res.status(400).send({message: "Must include rock classification!"});
        return;
    }
    if (!req.body.color) {
        res.status(400).send({message: "Must include rock color in array format!"});
        return;
    }
    if (!req.body.texture) {
        res.status(400).send({message: "Must include rock texture in array format!"});
        return;
    }
    if (!req.body.material) {
        res.status(400).send({message: "Must include rock material in array format!"});
        return;
    }
    if (!req.body.environment) {
        res.status(400).send({message: "Must include rock environment!"});
        return;
    }

    let rock_notes = "";
    if (req.body.notes) {
        rock_notes = req.body.notes;
    }

    // Create a Rock object
    const rock = new Rock({
        rock_name: req.body.rock_name,
        classification: req.body.classification,
        color: req.body.color,
        material: req.body.material,
        environment: req.body.environment,
        notes: rock_notes
    });

    rock
        .save(rock)
        .then(data => {
            res.send(data)
        })
        .catch(err => {
            res.status(500).send({
                message: err.message || "An error occurred while saving the rock to the database."
            })
        })
};

// Retrieve all Rocks from the database.
exports.findFiltered = (req, res) => {
    let condition = {}

    if (req.body.rock_name) {
        condition["rock_name"] = { $regex: new RegExp(req.body.rock_name), $options: "i" };
    }
    if (req.body.classification) {
        condition["classification"] = { $regex: new RegExp(req.body.classification), $options: "i" };
    }
    if (req.body.color) {
        condition["color"] = { $regex: new RegExp(req.body.color), $options: "i" };
    }
    if (req.body.texture) {
        condition["texture"] = { $regex: new RegExp(req.body.texture), $options: "i" };
    }
    if (req.body.material) {
        condition["material"] = { $regex: new RegExp(req.body.material), $options: "i" };
    }
    if (req.body.environment) {
        condition["environment"] = { $regex: new RegExp(req.body.environment), $options: "i" };
    }

    Rock.find(condition)
        .then(data => {
            res.send(data);
        })
        .catch(err => {
            res.status(500).send({
                message: err.message || "An error occurred while retrieving rocks."
            });
        });
    
};

// Find a single Rock with an id
exports.findOne = (req, res) => {
    const id = req.params.id;

    Rock.findById(id)
        .then(data => {
            if (!data) {
                res.status(404).send({message: "Could not find rock with ID " + id});
            }
            else {
                res.send(data)
            }
        })
        .catch(err => {
            res.status(500).send({message: "An error occurred while retrieving Rock with ID " + id})
        });
};

// Delete all Rocks from the database.
exports.deleteAll = (req, res) => {
    Rock.deleteMany({})
        .then(data => {
            res.send({
                message: `${data.deletedCount} rocks were successfully deleted.`
            });
        })
        .catch(err => {
            res.status(500).send({
                message: err.message || "An error occurred while deleting all rocks."
            });
        });
};

