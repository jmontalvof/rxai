
import kfp
from kfp import dsl
# from kfp.components import create_component_from_func

@dsl.component(
    base_image="jmontalvof/rxai-pipeline:latest"
)

def train_cnn_component(
    dropout_rate: float = 0.7,
    learning_rate: float = 0.0003,
    class_weight_covid: float = 2.0,
    class_weight_normal: float = 1.0,
    class_weight_viral: float = 3.0,
    freeze_layers: int = -20,
    epochs: int = 15
):
    import os
    import zipfile
    import boto3
    import tensorflow as tf
    import matplotlib.pyplot as plt
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
    import numpy as np

    # Descargar dataset desde MinIO
    s3 = boto3.client('s3',
        endpoint_url='http://minio-service.kubeflow:9000',
        aws_access_key_id='minio',
        aws_secret_access_key='minio123',
        region_name='us-east-1'
    )

    s3.download_file('rxai-data', 'dataset.zip', 'dataset.zip')
    with zipfile.ZipFile('dataset.zip', 'r') as zip_ref:
        zip_ref.extractall('./')

    dataset_path = "./data"
    train_dir = os.path.join(dataset_path, "train")
    val_dir = os.path.join(dataset_path, "test")

    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    img_size = (224, 224)
    batch_size = 32

    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        channel_shift_range=20,
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(train_dir, target_size=img_size, batch_size=batch_size, class_mode='categorical')
    val_generator = val_datagen.flow_from_directory(val_dir, target_size=img_size, batch_size=batch_size, class_mode='categorical', shuffle=False)

    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.optimizers import Adam
    from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

    # Descongelar parcialmente
    for layer in base_model.layers[:freeze_layers]:
        layer.trainable = False
    for layer in base_model.layers[freeze_layers:]:
        layer.trainable = True

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(dropout_rate)(x)
    predictions = Dense(3, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='categorical_crossentropy', metrics=['accuracy'])

    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=2, min_lr=1e-6, verbose=1)
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    class_weights = {0: class_weight_covid, 1: class_weight_normal, 2: class_weight_viral}
    model.fit(train_generator, validation_data=val_generator, epochs=epochs, class_weight=class_weights,
              callbacks=[reduce_lr, early_stopping])

    model.save("modelo_final.h5")

    predictions = model.predict(val_generator)
    y_pred = np.argmax(predictions, axis=1)
    y_true = val_generator.classes

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=list(val_generator.class_indices.keys()))
    disp.plot(xticks_rotation=45)
    plt.savefig("matriz_confusion.png")

    s3.upload_file("modelo_final.h5", "rxai-data", "modelo_final.h5")
    s3.upload_file("matriz_confusion.png", "rxai-data", "matriz_confusion.png")

@dsl.pipeline(
    name="RxAI CNN Pipeline Parametrizado",
    description="Pipeline con parámetros ajustables para fine-tuning de una CNN"
)
def rxai_pipeline(
    dropout_rate: float = 0.7,
    learning_rate: float = 0.0003,
    class_weight_covid: float = 2.0,
    class_weight_normal: float = 1.0,
    class_weight_viral: float = 3.0,
    freeze_layers: int = -20,
    epochs: int = 15
):
    train_cnn_component(
        dropout_rate=dropout_rate,
        learning_rate=learning_rate,
        class_weight_covid=class_weight_covid,
        class_weight_normal=class_weight_normal,
        class_weight_viral=class_weight_viral,
        freeze_layers=freeze_layers,
        epochs=epochs
    )

if __name__ == "__main__":
    from kfp import compiler
    compiler.Compiler().compile(rxai_pipeline, 'rxai_pipeline_parametrizable.yaml')
