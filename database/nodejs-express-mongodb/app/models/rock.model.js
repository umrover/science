module.exports = mongoose => {
    const RockModel = mongoose.model(
        "rock",
        mongoose.Schema(
            {
                rock_name: String,
                type: String,
                color: Array,
                material: Array,
                formation: String,
                notes: String
            },
            { timestamps: false }
        )
    );

    return RockModel;
};
