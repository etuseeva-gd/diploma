import tensorflow as tf
import numpy as np
import os
import glob
import cv2
import sys
import argparse
import config
from myutils import read_image


def predict(x_batch, classes):
    session = tf.Session()

    # ВОССТАНОВЛЕНИЕ МОДЕЛИ
    # ----------
    # Загружаем/восстанавливаем сохраненную обученную модель
    saver = tf.train.import_meta_graph(
        config.model_dir + config.model_name + '.meta'
    )
    saver.restore(session, tf.train.latest_checkpoint(config.model_dir))

    graph = tf.get_default_graph()

    # Отвечает за предсказание сети
    y_pred = graph.get_tensor_by_name("y_pred:0")

    # Передаем данные сети на вход
    x = graph.get_tensor_by_name("x:0")
    y = graph.get_tensor_by_name("y:0")

    y_test_images = np.zeros((1, classes))

    # ПРЕДСКАЗАНИЕ
    # ----------
    feed_dict_test = {x: x_batch, y: y_test_images}

    return session.run(y_pred, feed_dict=feed_dict_test)


def init():
    # ПОДГОТОВКА ВХОДНЫХ ДАННЫХ
    # ----------
    # Получаем данные о местоположении файла
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = sys.argv[1]
    file_name = dir_path + '/' + image_path

    # Считываем изображение, которое необходимо распознать
    # Ввиду того, что вход НС имеет вид [None, image_height, image_width, num_channels]
    # мы преобразуем наши данные к нужной форме
    images = [read_image(file_name, config.image_size)]
    images = np.array(images, dtype=np.uint8)
    x_batch = images.reshape(
        1,
        config.image_height,
        config.image_width,
        config.num_channels
    )

    classes = os.listdir(config.train_path)
    num_classes = len(classes)

    # Получили результат
    result = predict(x_batch, num_classes)

    print(result)
    print('Это {0} на {1}%'.format(classes[np.argmax(result)], np.amax(result) * 100))


if __name__ == '__main__':
    init()
