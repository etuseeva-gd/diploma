import tensorflow as tf
import numpy as np
import os
import glob
import cv2
import sys
import argparse

# КОНСТАНТЫ
# ----------
image_size = 128
num_channels = 3
model_name = 'model/model.meta'
model_name_2 = 'model/'

# ПОДГОТОВКА ВХОДНЫХ ДАННЫХ
# ----------
# Получаем данные о местоположении файла
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = sys.argv[1]
filename = dir_path + '/' + image_path

# Считываем изображение, которое необходимо распознать
image = cv2.imread(filename)
image = cv2.resize(image, (image_size, image_size), 0, 0, cv2.INTER_LINEAR)

# Ввиду того, что вход НС имеет вид [None image_size image_size num_channels]
# мы преобразуем наши данные к нужной форме
images = []
images.append(image)
images = np.array(images, dtype=np.uint8)
images = images.astype('float32')
images = np.multiply(images, 1.0 / 255.0)
x_batch = images.reshape(1, image_size, image_size, num_channels)

session = tf.Session()

# ВОССТАНОВЛЕНИЕ МОДЕЛИ
# ----------

# Загружаем/восстанавливаем сохраненную обученную модель
saver = tf.train.import_meta_graph(model_name)
saver.restore(session, tf.train.latest_checkpoint(model_name_2))

graph = tf.get_default_graph()

y_pred = graph.get_tensor_by_name("y_pred:0") # Отвечает за предсказание сети

# Передаем данные сети на вход
x = graph.get_tensor_by_name("x:0")
y_true = graph.get_tensor_by_name("y_true:0")
y_test_images = np.zeros((1, len(os.listdir('training_data'))))

# ПРЕДСКАЗАНИЕ
# ----------
feed_dict_testing = {x: x_batch, y_true: y_test_images}
result = session.run(y_pred, feed_dict=feed_dict_testing)

print('Полученный результат:')
print(result)

print('Конец')