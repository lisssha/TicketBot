

def logger():
    def decorator(func):
        def wrapper(*args, **kwargs):
            print(f'Запускаем функцию {func.__name__}')
            result = func(*args, **kwargs)
            print(f'Функция {func.__name__} завершила свою работу')
        return wrapper
    return decorator


@logger()
def foo(n, name=''):
    for i in range(n):
        print(f'{name} - говорит что он покакал')


foo(4, name='andrew')