import string
import random

def generate(size=10, chars=string.ascii_lowercase+string.digits):
    st=""
    for i in range(size):
        st+=random.choice(chars)
    return st

# print(generate())