# CW3
Cat Classifier is a web application that helps people identify cat breeds. It uses <a href='https://keras.io/api/applications/resnet/#resnet152v2-function'>ResNet152V2</a> provided by Keras to create the CNN model and uses over 20,000 photos of cats selected from the <a href='https://www.kaggle.com/ma7555/cat-breeds-dataset'>Cat Breeds Dataset</a> to train this model. Now it can classify 13 types of cats as well as the mixed breed. 
##Convolutional Neural Network (CNN)
To create your own CNN, you need to allocate the downloaded cat data into the train and validation folders. Then view all images and clean up the blurred and obviously incorrect images as many as possible.
- data
	- train
		- Bengal
		- British Shorthair
		- Siamese
		...
	- validation
		- Bengal
		- British Shorthair
		- Siamese
	...

After classifying the dataset,  using the ImageDataGenerator model in keras to collate the data, and using Sequential in Keras to build the CNN. Once the network is built, the data needs to be fed to the network for training, which can be done directly using fit_generator in keras. The relative code can be found in **ModelGenerator.py**.

In addition to using our own network for training and learning, we can also use the weights trained in keras for migration learning, which can increase the success rate of image recognition despite the lack of training data. I am using ResNet152V2, and the code can be found in **TransferModelGenerator.py**.

