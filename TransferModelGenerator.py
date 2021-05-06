import keras
from keras.layers import Dense, Dropout, GlobalAveragePooling2D
from keras.applications import ResNet152V2
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
import os

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


class TransferModelGenerator():
    '''
    Migration learning using weights already trained in keras.
    '''

    def generate_model(self):
        resize = 224
        tb_call_back = keras.callbacks.TensorBoard(log_dir='./logs',
                                                   histogram_freq=0,
                                                   write_graph=True,
                                                   write_images=True)

        base_model = ResNet152V2(weights='imagenet',
                                    include_top=False,
                                    pooling=None,
                                    input_shape=(resize, resize, 3),
                                    classes=13)

        for layer in base_model.layers:
            layer.trainable = False
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.5)(x)
        predictions = Dense(13, activation='sigmoid')(x)

        model = Model(inputs=base_model.input, outputs=predictions)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'], )

        model.fit_generator(CatData.train_flow,
                            steps_per_epoch=570,
                            epochs=10,
                            verbose=1,
                            validation_data=CatData.test_flow,
                            validation_steps=67,
                            callbacks=[tb_call_back])

        model.save('./model/catbreed_model.h5')


class CatData():
    '''
    Data collation and generation using operations of the ImageDataGenerator class in keras.
    '''

    # Training sample catalogue and test sample catalogue
    train_dir = './data/train/'
    test_dir = './data/validation/'

    # Data enhancement of training images
    train_pic_gen = ImageDataGenerator(rescale=1. / 255,
                                       rotation_range=20,
                                       width_shift_range=0.2,
                                       height_shift_range=0.2,
                                       shear_range=0.2,
                                       zoom_range=0.5,
                                       horizontal_flip=True,
                                       fill_mode='nearest')
    # Data enhancement of test images
    test_pic_gen = ImageDataGenerator(rescale=1. / 255)
    # Generate training data with the .flow_from_directory function
    train_flow = train_pic_gen.flow_from_directory(train_dir,
                                                   target_size=(224, 224),
                                                   batch_size=50,
                                                   class_mode='categorical')
    # Generating test data with the .flow_from_directory function
    test_flow = test_pic_gen.flow_from_directory(test_dir,
                                                 target_size=(224, 224),
                                                 batch_size=50,
                                                 class_mode='categorical')


if __name__ == '__main__':
    mg = TransferModelGenerator()
    mg.generate_model()