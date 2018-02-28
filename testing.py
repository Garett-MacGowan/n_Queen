import bisect

bisectTest = [(-5, 4, 8), (-3, 2, 9)]

item = (-6, 9, 11)
insertionReference = item[0]

index = bisect.bisect_left(bisectTest, (insertionReference, ))

bisectTest.insert(index, item)
print(bisectTest)
