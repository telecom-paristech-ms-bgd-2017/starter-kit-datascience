def donuts(count):
    if count < 10:
        return "Number of donuts: " + str(count)
    else:
        return "Number of donuts: many"


def both_ends(s):
    result = ""
    if len(s) <= 2:
        return result
    else:
        result = s[0:2] + s[len(s) - 2:len(s)]
        return result


def fix_start(s):
    if len(s) <= 1:
        print("Please make sur string length is greater than 1")
        return
    else:
        sf = s[1:]
        return s[0] + sf.replace(s[0], "*")


def mix_up(a, b):
    newb = a[0:2] + b[2:]
    newa = b[0:2] + a[2:]
    return newa + " " + newb


def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


def main():
    print("\n")
    'donuts '
    # Each line calls donuts, compares its result to the expected for that call.
    test(donuts(4), 'Number of donuts: 4')
    test(donuts(9), 'Number of donuts: 9')
    test(donuts(10), 'Number of donuts: many')
    test(donuts(99), 'Number of donuts: many')

    print("\n")
    print("\n")
    'both_ends'
    test(both_ends('spring'), 'spng')
    test(both_ends('Hello'), 'Helo')
    test(both_ends('a'), '')
    test(both_ends('xyz'), 'xyyz')

    print("\n")
    print("\n")
    'fix_start'
    test(fix_start('babble'), 'ba**le')
    test(fix_start('aardvark'), 'a*rdv*rk')
    test(fix_start('google'), 'goo*le')
    test(fix_start('donut'), 'donut')

    print("\n")
    print("\n")
    'mix_up'
    test(mix_up('mix', 'pod'), 'pox mid')
    test(mix_up('dog', 'dinner'), 'dig donner')
    test(mix_up('gnash', 'sport'), 'spash gnort')
    test(mix_up('pezzy', 'firm'), 'fizzy perm')


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
    main()











