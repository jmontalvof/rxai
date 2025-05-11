# Importar librerías
import tensorflow as tf
import os
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50, MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

# Montar Google Drive
#from google.colab import drive
#drive.mount('/content/drive')

# Directorios de datos
dataset_path = "./data"  # porque el zip se descomprime aquí
train_dir = os.path.join(dataset_path, "train")
val_dir = os.path.join(dataset_path, "test")

# Preparar los datos
img_size = (224, 224)
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,  # Rotaciones moderadas
    width_shift_range=0.2,
    height_shift_range=0.2,
    brightness_range=[0.8, 1.2],
    channel_shift_range=20,
    shear_range=0.1,    # Reducción de shear
    zoom_range=0.2,     # Zoom moderado
    horizontal_flip=True,
    fill_mode='nearest'
)

# Aplicar Data Augmentation solo en entrenamiento
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical'
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(train_dir,
                                                    target_size=img_size,
                                                    batch_size=batch_size,
                                                    class_mode='categorical')


val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False  # ← aquí debe ir
)

# Cargar MobileNetV2 preentrenado
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Congelar todas las capas del modelo base
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Capas personalizadas
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.8)(x)
predictions = Dense(3, activation='softmax')(x)

# Modelo final
model = Model(inputs=base_model.input, outputs=predictions)

# Compilar el modelo
model.compile(optimizer=Adam(learning_rate=0.0005), loss='categorical_crossentropy', metrics=['accuracy'])

# Callbacks
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=3, min_lr=1e-6, verbose=1)
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

class_weights = {0: 2.0, 1: 1.0, 2: 4.0}  # Aumentar el peso de COVID y Viral Pneumonia
history = model.fit(train_generator, validation_data=val_generator,
                    epochs=30, class_weight=class_weights)
# Evaluar el modelo en validación
loss, accuracy = model.evaluate(val_generator)
print(f"Loss en Validación: {loss:.4f}")
print(f"Accuracy en Validación: {accuracy:.4f}")

from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Predicciones en el set de validación
predictions = model.predict(val_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = val_generator.classes

# Matriz de Confusión
cm = confusion_matrix(y_true, y_pred)
print("Matriz de Confusión:")
print(cm)

# Clasificación
print("Reporte de Clasificación:")
print(classification_report(y_true, y_pred, target_names=val_generator.class_indices.keys()))

from tensorflow.keras.models import Model
import matplotlib.pyplot as plt
import numpy as np

# Obtener predicciones
predictions = model.predict(val_generator)
y_pred = np.argmax(predictions, axis=1)
y_true = val_generator.classes

# Visualizar Grad-CAM o imágenes más erróneas
