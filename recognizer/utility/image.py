import cv2
import os
import glob
from sklearn.utils import shuffle
import numpy as np
from models.dataset import DataSet
import urllib.request


def get_image_by_url(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    return cv2.imdecode(arr, -1)


def get_image_by_path(path):
    return cv2.imread(path)


def prepare_image(image, image_size):
    # Подготовка изображения для дальнейшего распознавания
    image = cv2.resize(
        image,
        (image_size, image_size),
        0,
        0,
        cv2.INTER_LINEAR
    )
    image = image.astype(np.float32)
    image = np.multiply(image, 1.0 / 255.0)
    return image


def load_images(train_path, image_size, classes):
    # Функция позволяет загрузить изображения по переданому пути
    images = []
    labels = []
    img_names = []
    cls = []

    for fields in classes:
        index = classes.index(fields)
        path = os.path.join(train_path, fields, '*g')
        files = glob.glob(path)
        for file_name in files:
            # Изображения
            image = get_image_by_path(file_name)
            images.append(prepare_image(image, image_size))

            # label изображения
            label = np.zeros(len(classes))
            label[index] = 1.0
            labels.append(label)

            # Название изображения
            img_names.append(os.path.basename(file_name))

            # Класс изображения
            cls.append(fields)

    # images, labels, img_names, cls
    return np.array(images), np.array(labels), np.array(img_names), np.array(cls)


def read_train_sets(train_path, image_size, classes, test_size):
    images, labels, img_names, cls = load_images(
        train_path, image_size, classes
    )
    images, labels, img_names, cls = shuffle(images, labels, img_names, cls)

    if isinstance(test_size, float):
        test_size = int(test_size * images.shape[0])

    class DataSets(object):
        pass
    data_sets = DataSets()

    # Тренировочные данные
    train_images = images[test_size:]
    train_labels = labels[test_size:]
    train_img_names = img_names[test_size:]
    train_cls = cls[test_size:]
    data_sets.train = DataSet(
        train_images, train_labels, train_img_names, train_cls
    )

    # Данные для тестирования
    test_images = images[:test_size]
    test_labels = labels[:test_size]
    test_img_names = img_names[:test_size]
    test_cls = cls[:test_size]
    data_sets.test = DataSet(
        test_images, test_labels, test_img_names, test_cls
    )

    return data_sets
