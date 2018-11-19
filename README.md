#### Recognizer (Распознаватель)

##### Требования для запуска
1. Python (3 и выше версии)
2. Зависимости из файла Pipfile, для того чтобы их установить:
```
pipenv install
```

##### Запуск 
##### 1. Для тренировки системы (файл train.py):
Перед стартом нужно чтобы в /recognizer/training_images были изображения разбитые по классам и файл classes.json

Пример:

```
pipenv run python /recognizer/train.py
```

##### 2. Для того, чтобы распознать (файл predict.py):
Имеются два параметра:
1. flag: "-f" если мы хотим выводить результат в файл и консоль, и "-c" если хотим выводить результат только в консоль
2. path: до папки с изображениями, которые мы хотим распознать или путь до файла, который мы хотим распознать 

```
pipenv run python /recognizer/predict flag path
```

Пример:

```pipenv run python /recognizer/predict.py -f /recognizer/testing_images```

```pipenv run python /recognizer/predict.py -f /recognizer/testing_images/0_00004.pbm```


#### Server (Сервер)

##### Требования для запуска
Такие же, как и для распознавателя.

##### Запуск 
```
pipenv run python /server/server.py
```

#### Client (Клиент)

##### Требования для запуска
1. NodeJS
2. Зависимости из файла package.json, для того чтобы их установить:
```
cd /client
npm install
```

##### Запуск 
```
npm start
```

UI будет расположен по адресу http://localhost:4200
