stat = [('-', 212, 'fucking work'), ('-', 212, 'fucking work'), ('-', 111, 'food'), ('-', 111, 'food'),
        ('-', 200, 'work'), ('+', 5000, 'зарплата'), ('-', 200, 'dfqwwqe'), ('-', 200, 'work'), ('-', 200, 'work'),
        ('-', 200, 'work'), ('-', 2000, 'work'), ('-', 150, 'work'), ('+', 21000, 'зарплата')]

positive = []
negative = []
set_desc = {}
for i in stat:
    if i[0] == '+':
        positive.append((i[1], i[2]))
        set_desc[i[2]] = 0
        for a in positive:
            set_desc[i[2]] += i[1]
    if i[0] == '-':
        negative.append((i[1], i[2]))
        set_desc[i[2]] = 0
        for a in negative:
            set_desc[i[2]] -= i[1]

print(set_desc)
