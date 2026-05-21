from tensorflow.keras.applications import Xception
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

base = Xception(
    weights=None,
    include_top=False,
    input_shape=(299,299,3)
)

x = GlobalAveragePooling2D()(base.output)

output = Dense(
    3,
    activation="softmax"
)(x)

model = Model(
    base.input,
    output
)

model.load_weights(
    "backend/xception_weights.weights.h5"
)

model.save(
    "backend/xception_render.keras"
)

print("Done")