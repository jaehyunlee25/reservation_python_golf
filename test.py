# exec(open('app.py').read())

def pyRead(file):
    l = open(file, 'r')
    lcon = l.read()
    l.close()
    return lcon

header = pyRead('py/header.py')
common = pyRead('py/common.py')
footer = pyRead('py/footer.py')
div = '\n\n# file division =================================\n\n'

arr = [
    'py/header.py',
    'py/common.py',
    'island/island.py',
    # 'jinyang/jinyang.py',
    'py/footer.py',
]

f = open('app.py', 'w')
for el in arr:
    f.write(pyRead(el))
    f.write(div)
f.close()

exec(pyRead('app.py'))