import cv2
import os
import glob
from sklearn.utils import shuffle
import numpy as np


class DataSet(object):
    def __init__(self, images, labels, img_names, cls):
        self._num_examples = images.shape[0]

        self._images = images
        self._labels = labels
        self._img_names = img_names
        self._cls = cls
        self._epochs_done = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def img_names(self):
        return self._img_names

    @property
    def cls(self):
        return self._cls

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_done(self):
        return self._epochs_done

    def next_batch(self, batch_size):
        start = self._index_in_epoch
        self._index_in_epoch += batch_size

        if self._index_in_epoch > self._num_examples:
            self._epochs_done += 1
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch

        return self._images[start:end], self._labels[start:end], self._img_names[start:end], self._cls[start:end]


def load_train(train_path, image_size, classes):
    # Функция позволяет загрузить изображения по переданому пути
    images = []
    labels = []
    img_names = []
    cls = []

    for fields in classes:
        index = classes.index(fields)
        path = os.path.join(train_path, fields, '*g')
        files = glob.glob(path)
        for fl in files:
            # Само изображения
            image = cv2.imread(fl)
            image = cv2.resize(
                image,
                (image_size, image_size),
                0,
                0,
                cv2.INTER_LINEAR
            )
            image = image.astype(np.float32)
            image = np.multiply(image, 1.0 / 255.0)
            images.append(image)

            # label изображения
            label = np.zeros(len(classes))
            label[index] = 1.0
            labels.append(label)

            # Название избображения
            flbase = os.path.basename(fl)
            img_names.append(flbase)

            # Класс изображения
            cls.append(fields)

    # images, labels, img_names, cls
    return np.array(images), np.array(labels), np.array(img_names), np.array(cls)


def read_train_sets(train_path, image_size, classes, test_size):
    images, labels, img_names, cls = load_train(
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
