import bisect

bisectTest = [(-5, 4), (-3, 2)]

item = (-6, 9)
insertionReference = item[0]

index = bisect.bisect_left(bisectTest, (insertionReference, ))

bisectTest.insert(index, item)
print(bisectTest)
