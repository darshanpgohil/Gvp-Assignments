def my_decorator(fun):
    def wrapper():
        print("my first function")
        fun()
    return wrapper

@my_decorator
def second_function():
    print("second function")

second_function()