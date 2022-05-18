const db = require("../models");
const Rock = db.rocks;

// Create and Save a new Rock
exports.create = (req, res) => {
    // Validate request
    if (!req.body.rock_name) {
        res.status(400).send({message: "Must include rock name!"});
        return;
    }
    if (!req.body.type) {
        res.status(400).send({message: "Must include rock type!"});
        return;
    }
    if (!req.body.color) {
        res.status(400).send({message: "Must include rock color in array format!"});
        return;
    }
    if (!req.body.material) {
        res.status(400).send({message: "Must include rock material in array format!"});
        return;
    }
    if (!req.body.formation) {
        res.status(400).send({message: "Must include rock formation!"});
        return;
    }

    let rock_notes = "";
    if (req.body.notes) {
        rock_notes = req.body.notes;
    }

    // Create a Rock object
    const rock = new Rock({
        rock_name: req.body.rock_name,
        type: req.body.type,
        color: req.body.color,
        material: req.body.material,
        formation: req.body.formation,
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

    if (req.query.rock_name) {
        condition[rock_name] = { $regex: new RegExp(req.query.rock_name), $options: "i" }
    }
    if (req.query.type) {
        condition[type] = { $regex: new RegExp(req.query.type), $options: "i" }
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

