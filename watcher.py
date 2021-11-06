from posixpath import split
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
import shutil

dir = os.curdir
jsonConfigName = os.path.abspath(dir + '/config.json')





def file_get_contents(filename):
    with open(filename, encoding="utf8") as f:
        return f.read()







def run(_from, _to, filelist):
    if not os.path.isdir(_from):
        print('Директория отсутствует ' + _from)
        exit()

    if not os.path.isdir(os.path.dirname(_to)):
        print('Некорректный путь ' + _to)
        exit()

    files = {}

    tree = os.walk(_from)
    for element in tree:
        current_path = element[0]
        for file_name in element[2]:
            if (file_name.split('.')[-1]=='py'):
                read_file_name = os.path.abspath(current_path + '/' + file_name)
                files[file_name] = read_file_name

    # try:
    if True:
        print('open', _to)
        with open(_to, "w+", encoding="utf8") as script:
            for fname in filelist:

                script.write(f'# {fname}\n')

                code = file_get_contents(files[fname])
                code_list = code.split('#ignore')


                for codeLine in code_list:
                    print("readCODE")
                    if (codeLine[0:6]=='_start'):
                        script.write( '#'+ '\n#'.join(codeLine[6:].split('\n')) + '\n')
                    elif (codeLine[0:4]=='_end'):
                        script.write(codeLine[4:] + '\n')
                    else:
                        script.write(codeLine + '\n')

            print('write', _to)
    # except ValueError:
    #     print(ValueError)








def getConfig():
    global jsonConfigName
    if os.path.isfile(jsonConfigName):
        jsonConfigData = json.loads(file_get_contents(jsonConfigName))
        if ('to' not in jsonConfigData):
            print('config.json - укажите путь к конечному файлу (to)')
            exit()

        if ('from' not in jsonConfigData):
            print('config.json - укажите путь к папке с файлами (from)')
            exit()


        jsonConfigData['from'] = os.path.abspath(jsonConfigData['from'])
        jsonConfigData['to'] = os.path.abspath(jsonConfigData['to'])

        if ('copy' in jsonConfigData):
            jsonConfigData['copy'] = os.path.abspath(jsonConfigData['copy'])

        return jsonConfigData
    else:
        print('config.json - ненайден')
        exit()




def changes(event):
    print(event)

    data = getConfig()
    run(data['from'], data['to'], data['list'])
    if ('copy' in data):
        shutil.copy2(data['to'], data['copy'])
    return data


if __name__ == "__main__":

    jsonConfig = changes('start')
    
    event_handler = FileSystemEventHandler()
    event_handler.on_any_event = lambda event: changes(event.event_type)


    observer = Observer()
    observer.schedule(event_handler, jsonConfig['from'], recursive=True)
    observer.start()
    try:
        print(f'wait changer at ', jsonConfig['from'])
        while True:
            time.sleep(1)
    finally:
        print('stop')
        observer.stop()
        observer.join()