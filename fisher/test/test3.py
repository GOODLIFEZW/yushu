
# class MyResourse:

    # def __enter__(self):
    #     print('enter')
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     print('exit')

    # def query(self):
    #     print('query')


# with MyResourse() as r:
#         r.query()

from contextlib import contextmanager

@contextmanager
def make_response():
    print('enter')
    yield
    print('exit')


with make_response():
    print('你好')

