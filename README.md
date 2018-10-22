##### Recognizer (Распознаватель):
```
    /recognizer
        /models - модели
            detaset.py - регулирует работу с сетами изображений
            params.py - содержит классы, которые отвечают за параметры системы
        /params - параметры системы
            base.json - базовые параметры (где находятся изображения, их размер и тд)
            nn.json - параметры слоев сети
            train.json - параметры для обучения
        /testing_data - тестовые данные
            /class_1
            /class_2
        /training_data - тренировочные данные
            /class_1
            /class_2
        /utility - папка с вспомогательными модулями
            constants.py - содержит константы
            image.py - отвечает за работу с изображениями
            jsonfile.py - с json файлами
            network.py - с сетью (позволяет по переданными параметрам ее создать)
        Dokerfile - конфиг файл с докером
        predict.py - основной файл для запуска распознавания конкретного изображения
        train.py - основной файл для запуска создания и тренировки сети
```
Чтобы поработать с чисто распознавателем нужно перейти в папку: `  `

###### Создание и тренировка сети
Задать необходимые параметры в ` /recognizer/params/* ` и выполнить:
``` 
    python /recognizer/train.py 
```

##### Распознавание изображения
```  
    python /recognizer/predict.py path_to_image 
```
###### Пример: 
``` 
    python /recognizer/predict.py testing_data/cats/cat.1110.jpg 
```

##### Client (Клиент)
```
    cd /client
    npm start 
```

##### Server (Сервер)
```
    cd /server
    python server.py 
```