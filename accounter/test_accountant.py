stat = [('-', 212, 'fucking work'), ('-', 212, 'fucking work'), ('-', 111, 'food'), ('-', 111, 'food'),
        ('-', 200, 'work'), ('+', 5000, 'зарплата'), ('-', 200, 'dfqwwqe'), ('-', 200, 'work'), ('-', 200, 'work'),
        ('-', 200, 'work'), ('-', 2000, 'work'), ('-', 150, 'work'), ('+', 21000, 'зарплата')]

set_plus = {}
set_minus = {}

for i in stat:
    if i[0] == '+':
        set_plus[i[2]] = 0
    if i[0] == '-':
        set_minus[i[2]] = 0

for i in stat:
    if i[0] == '+':
        set_plus[i[2]] += i[1]
    if i[0] == '-':
        set_minus[i[2]] -= i[1]

print(set_plus)
print(set_minus)



