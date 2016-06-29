import slave_a2
import imp

imp.reload(slave_a2)


data = list(range(0,100))

s = slave_a2.SlaveA2()
s.start(data)

while True:
    q = s.get_query()

    if q is None:
        print('done')
        break
    else:
        a = q > 50 or (q > 40 and q % 2 == 0)
        s.answer_query(a)
        input('Press any key to continue ...')
    

