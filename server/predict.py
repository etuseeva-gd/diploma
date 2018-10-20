import tensorflow as tf
import numpy as np
import os
import glob
import cv2
import sys
import argparse
import config

# @todo сделать чтобы было несколько изображений
# подумать над тем, чтобы разбить файлик


def predict(x_batch):
    session = tf.Session()

    # ВОССТАНОВЛЕНИЕ МОДЕЛИ
    # ----------
    # Загружаем/восстанавливаем сохраненную обученную модель
    saver = tf.train.import_meta_graph(
        config.model_dir + config.model_name + '.meta')
    saver.restore(session, tf.train.latest_checkpoint(config.model_dir))

    graph = tf.get_default_graph()

    # Отвечает за предсказание сети
    y_pred = graph.get_tensor_by_name("y_pred:0")

    # Передаем данные сети на вход
    x = graph.get_tensor_by_name("x:0")
    y_true = graph.get_tensor_by_name("y_true:0")
    y_test_images = np.zeros((1, len(os.listdir(config.train_path))))

    # ПРЕДСКАЗАНИЕ
    # ----------
    feed_dict_testing = {x: x_batch, y_true: y_test_images}

    return session.run(y_pred, feed_dict=feed_dict_testing)


def init():
    # ПОДГОТОВКА ВХОДНЫХ ДАННЫХ
    # ----------
    # Получаем данные о местоположении файла
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = sys.argv[1]
    filename = dir_path + '/' + image_path

    # Считываем изображение, которое необходимо распознать
    image = cv2.imread(filename)
    image = cv2.resize(
        image, (config.image_size, config.image_size), 0, 0, cv2.INTER_LINEAR)

    # Ввиду того, что вход НС имеет вид [None image_size image_size num_channels]
    # мы преобразуем наши данные к нужной форме
    images = []
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0 / 255.0)
    x_batch = images.reshape(1, config.image_size,
                             config.image_size, config.num_channels)

    print('Полученный результат:')
    result = predict(x_batch)
    print(result)


if __name__ == '__main__':
    init()
