class File:
    @staticmethod
    def read_file(path):
        file = open(path, 'r')
        lines = file.readlines()
        file.close()
        return lines

        # lines = []
        # if file.mode == 'r':
        #     data = file.read();
        #     return data

        # return ''

    @staticmethod
    def write_file(path, data):
        # Открываем файл в который собираемся записать данные,
        # если его нет, то создать его
        file = open(path, 'w+')
        file.write(data)
        file.close()

