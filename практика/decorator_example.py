import time


def some_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Время работы функции: {time.time() - start_time} s")

        return result

    return wrapper


@some_decorator
def some_function(arg, name):
    print(f"Executing {name}, arg = {arg}")
    time.sleep(5)

    return 'Результат работы функции func'

# some_function = some_decorator(some_function) -> @some_decorator


result = some_function('Аргумент', name='Имя функции')
result
