import keras
import os
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import *
import matplotlib.pyplot as plt

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
picSize = 224


class ModelGenerator:

    def generate_model(self):
        '''
        Using Sequential in Keras to build neural networks, and using the fit_generator in keras to feed the data to
        the network for training.
        :return:
        '''

        model = Sequential()
        # level1
        model.add(Conv2D(filters=96, kernel_size=(11, 11),
                         strides=(4, 4), padding='valid',
                         input_shape=(picSize, picSize, 3),
                         activation='relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(3, 3),
                               strides=(2, 2),
                               padding='valid'))
        # level_2
        model.add(Conv2D(filters=256, kernel_size=(5, 5),
                         strides=(1, 1), padding='same',
                         activation='relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(3, 3),
                               strides=(2, 2),
                               padding='valid'))
        # layer_3
        model.add(Conv2D(filters=384, kernel_size=(3, 3),
                         strides=(1, 1), padding='same',
                         activation='relu'))
        model.add(BatchNormalization())
        model.add(Conv2D(filters=384, kernel_size=(3, 3),
                         strides=(1, 1), padding='same',
                         activation='relu'))
        model.add(BatchNormalization())
        model.add(Conv2D(filters=356, kernel_size=(3, 3),
                         activation='relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(3, 3),
                               strides=(2, 2), padding='valid'))

        # layer_4
        model.add(Flatten())
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))

        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))

        model.add(Dense(1000, activation='relu'))
        model.add(Dropout(0.5))

        # output layer
        model.add(Dense(21))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='sgd',
                      metrics=['accuracy'])

        tbCallBack = keras.callbacks.TensorBoard(log_dir='./logs/1',
                                                 histogram_freq=0,
                                                 write_graph=True,
                                                 write_images=True)

        his = model.fit_generator(CatData.train_flow,
                                  steps_per_epoch=538,
                                  epochs=50,
                                  verbose=1,
                                  validation_data=CatData.test_flow,
                                  validation_steps=28,
                                  callbacks=[tbCallBack])

        plt.plot(his.history['acc'])
        plt.plot(his.history['val_acc'])
        plt.title('model_accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        plt.plot(his.history['loss'])
        plt.plot(his.history['val_loss'])
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
        model.save('./weights/catdogs_model.h5')


class CatData:
    '''
    Data collation and generation using operations of the ImageDataGenerator class in keras.
    '''

    # Training sample catalogue and test sample catalogue
    train_dir = 'data/train/'
    test_dir = 'data/validation/'
    # Data enhancement of training images
    train_pic_gen = ImageDataGenerator(rescale=1./255,
                                       rotation_range=20,
                                       width_shift_range=0.2,
                                       height_shift_range=0.2,
                                       shear_range=0.2,
                                       zoom_range=0.5,
                                       horizontal_flip=True,
                                       fill_mode='nearest')
    # Data enhancement of test images
    test_pic_gen = ImageDataGenerator(rescale=1./255)
    # Generate training data with the .flow_from_directory function
    train_flow = train_pic_gen.flow_from_directory(train_dir,
                                                   target_size=(picSize, picSize),
                                                   batch_size=50,
                                                   class_mode='categorical')
    # Generating test data with the .flow_from_directory function
    test_flow = test_pic_gen.flow_from_directory(test_dir,
                                                 target_size=(picSize, picSize),
                                                 batch_size=50,
                                                 class_mode='categorical')


if __name__ == '__main__':
    mg = ModelGenerator()
    mg.generate_model()