module.exports = mongoose => {
    const RockModel = mongoose.model(
        "rock",
        mongoose.Schema(
            {
                rock_name: String,
                classification: String,
                color: Array,
                texture: Array,
                material: Array,
                environment: String,
                notes: String
            },
            { timestamps: false }
        )
    );

    return RockModel;
};
