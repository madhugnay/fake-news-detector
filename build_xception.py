from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

base = Xception(
    weights=None,
    include_top=False,
    input_shape=(299,299,3)
)

x = GlobalAveragePooling2D()(base.output)

# ADD THIS EXTRA DENSE
x = Dense(
    1024,
    activation="relu"
)(x)

x = Dropout(0.2)(x)

output = Dense(
    3,
    activation="softmax"
)(x)

model = Model(
    base.input,
    output
)

print("Loading weights...")

model.load_weights(
    "backend/xception_weights.weights.h5"
)

print("Saving model...")

model.save(
    "backend/xception_render.keras"
)

print("Done")