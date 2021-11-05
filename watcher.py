import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import combine
import os
import json

dir = os.curdir
jsonConfigName = os.path.abspath(dir + '/config.json')

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

def run(_from, _to, filelist):
    files = {}

    tree = os.walk(os.path.abspath(_from))
    for element in tree:
        current_path = element[0]
        for file_name in element[2]:
            if (file_name.split('.')[-1]=='py'):
                read_file_name = os.path.abspath(current_path + '/' + file_name)
                files[file_name] = read_file_name

    with open(_to, "w") as script:
        for fname in filelist:
            script.write(f'# {fname}\n' + file_get_contents(files[fname]) + '\n')
            print('write', fname)


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
        
        return jsonConfigData
    else:
        print('config.json - ненайден')
        exit()








def changes(event):
    print(event.event_type)

    data = getConfig()
    run(data['from'], data['to'], data['list'])


if __name__ == "__main__":

    jsonConfig = getConfig()
    
    event_handler = FileSystemEventHandler()
    event_handler.on_any_event = changes


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