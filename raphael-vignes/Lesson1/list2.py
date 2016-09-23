def remove_adjacent(nums):
    resultList = []
    if len(nums) > 0:
        resultList.append(nums[0])
        print(nums[0])
        previousnumb = nums[0]
        for num in nums[1:]:
            if num != previousnumb:
                resultList.append(num)
            previousnumb = num
    return resultList


def linear_merge(list1, list2):
    resultList = []
    while len(list1) and len(list2):
        if list1[0] < list2[0]:
            resultList.append(list1.pop(0))
        else :
            resultList.append(list2.pop(0))
    resultList.extend(list1)
    resultList.extend(list2)
    return resultList

def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print(prefix+" Got : "+repr(got)+" Expected : " +repr(expected))


# Calls the above functions with interesting inputs.
def main():
  print('remove_adjacent')
  test(remove_adjacent([1, 2, 2, 3]), [1, 2, 3])
  test(remove_adjacent([2, 2, 3, 3, 3]), [2, 3])
  test(remove_adjacent([]), [])

  print
  print('linear_merge')
  test(linear_merge(['aa', 'xx', 'zz'], ['bb', 'cc']),
       ['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'xx'], ['bb', 'cc', 'zz']),
       ['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'aa'], ['aa', 'bb', 'bb']),
       ['aa', 'aa', 'aa', 'bb', 'bb'])


if __name__ == '__main__':
  main()
