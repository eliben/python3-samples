#-------------------------------------------------------------------------------
# Basic examples of using the enum module.
#
# Eli Bendersky (eliben@gmail.com)
# This code is in hte public domain
#-------------------------------------------------------------------------------
from enum import Enum

# Define an enum and access it in basic ways
class Color(Enum):
    red = 1
    green = 2
    blue = 3

mycolor = Color.red
print('mycolor =', mycolor)
print('is mycolor a Color?', isinstance(mycolor, Color))
print('mycolor is green?', mycolor == Color.green)
print('mycolor == 1?', mycolor == 1)

print()

# Define some other enum.
# Note: values are arbitrary for the enum module itself - they don't compare
# equal among different kinds of enums. They also don't affect iteration order.
# They may carry meaning in the user's code.
class Season(Enum):
    winter = 20
    spring = 2
    summer = 200
    autumn = 2000

# Even though the numeric value of different enum kinds is equal, the enums
# themselves are not.
print('The value of Color.green =', Color.green.value)
print('The value of Season.spring =', Season.spring.value)
if Color.green == Season.spring:
    print('Oops, Color.green is equal to Season.spring')
else:
    print('Color.green != Season.spring')

print('Iterating over Seasons. Iteration is in definition, not value, order:')
for s in Season:
    print(' ', s)

print()

# Using the functional API makes sense in a lot of cases, to save typing and
# having to come up with arbitrary values:
Animal = Enum('Animal', 'ant bee cat dog')
print('The type of Animal.dog is', type(Animal.dog))

print('Iterating over Animals, with their values')
for animal in Animal:
    print('  {0} = {1}'.format(animal, animal.value))


