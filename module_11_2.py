# Интроспекция
import inspect
import sys
from pprint import pprint


def test_function():
    '''Это тестовая функция для просмотра содержания'''
    test_var = 'Это тестовая переменная'
    return test_var


class test_class():
    '''Это тестовый класс для просмотра содержания класса'''
    test_attr = None

    def __Init__(self):
        self.test_attr = 15

    def test_method(self):
        print('Это тестовый метод')


class introspection_info():
    '''Данный класс просматривает атрибуты и методы объекта
    Имеет атрибут
    object - В данном атрибуте хранится значение переданное классу в качестве параметра
    Класс имеет следующие методы:
    __init__ принимает параметр и содержащий объект для изучения.
        число - 42 имеет отдельную дополнительную обработку :-)
    SysInfo - Выводит информацию об операционной системе и подключенных модулях
    ObjectInfo - Выводит информацию об объекте, атрибуты и методы'''
    object = None

    def __init__(self, object):
        self.object = object
        if self.object == 42:
            print(
                f'Ответ на вопрос - "Жизни, вселенной и вообще" это {self.object} \n '
                f'{chr(169)} "Автостопом по галактике"')

    def SysInfo(self):
        OperationalSystem = sys.platform
        if OperationalSystem == 'win32':
            print('Python выполняется на операционной системе windows')
        elif OperationalSystem == 'darwin':
            print('Python выполняется на операционной системе macOS')
        elif OperationalSystem == 'linux':
            print('Python выполняется на операционной системе Linux')
        print('Выведем импортированные модули')
        pprint(sys.modules)

    def ObjectInfo(self):
        InformationOutput = {}
        TypeObject = type(self.object)
        # Выводим сообщение о типах в соответствии с типом переданного параметра
        # перечислена часть типов, на остальные выводится стандартное сообщение функции - Type/
        if TypeObject == int:
            print('Это целое число, класс - int')
        elif TypeObject == float:
            print('Это число с плавающей запятой, класс - float')
        elif TypeObject == str:
            print('Это строка, класс - str')
        elif TypeObject == tuple:
            print('Это кортеж, класс - tuple')
        elif TypeObject == list:
            print('Это список, класс - list')
        elif inspect.ismodule(self.object):
            print('Это модуль, класс module')
        elif inspect.ismethod(self.object):
            print('Это метод, класс method')
        elif inspect.isfunction(self.object):
            print('Это функция, класс function')
        elif inspect.isclass(self.object):
            print('Это класс, класс type')
        else:
            print(type(self.object))

        ListfAttributes = dir(self.object)
        ListAttrib = []
        ListMethods = []
        for i in ListfAttributes:
            ValueAttributes = str(getattr(self.object, i))
            #            print(f"{i}:", getattr(self.object, i))
            if ValueAttributes.find('method') > 0 and ValueAttributes.find('slot wrapper') \
                    and ValueAttributes.find('function'):
                ListMethods.append(i)
            else:
                ListAttrib.append(i)
        InformationOutput['type'] = str(type(self.object)).split("'")[1]
        InformationOutput['attributes'] = ListAttrib
        InformationOutput['methods'] = ListMethods
        if hasattr(self.object, '__module__'):
            InformationOutput['module'] = self.object.__module__
        # Выведем дополнительную информацию
        if hasattr(self.object, '__doc__') and self.object.__doc__ != None:
            InformationOutput['doc'] = self.object.__doc__
        # вывод
        #pprint(InformationOutput, sort_dicts=False)
        return InformationOutput

intro_inf = introspection_info(42)
#print(intro_inf.SysInfo())
pprint(intro_inf.ObjectInfo(), sort_dicts=False)
print()
#тестовый класс
intro_inf = introspection_info(test_class)
pprint(intro_inf.ObjectInfo(), sort_dicts=False)
print()
#Теустовая функция
intro_inf = introspection_info(test_function)
pprint(intro_inf.ObjectInfo(), sort_dicts=False)
