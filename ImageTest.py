from keras.models import load_model
import cv2
import numpy as np

'''
Testing the prediction of cat breed with trained model.
'''

model = load_model('./model/catbreed_model.h5')
test_image = cv2.resize(cv2.imread('./upload/26473417_213.jpg'), (224, 224))
test_image = np.asarray(test_image.astype("float32"))
test_image = test_image/255.
test_image = test_image.reshape((1,224,224,3))
breed_prob = model.predict(test_image)
breed = breed_prob.argmax(axis=-1)
print(breed)
