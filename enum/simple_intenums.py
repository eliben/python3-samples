#-------------------------------------------------------------------------------
# Basic examples of using IntEnum.
#
# Eli Bendersky (eliben@gmail.com)
# This code is in hte public domain
#-------------------------------------------------------------------------------
from enum import IntEnum

class Request(IntEnum):
    post = 1
    get = 2

req = Request.post
print('req =', req)

# Unlike regular Enums, IntEnums are also integers and thus can be compared to
# other integers.
print('req == 1?', req == 1)

# Beware, the above means they can also be compared to members of other,
# unrelated IntEnums.
class Dummy(IntEnum):
    foo = 1
    bar = 2

print('req == Dummy.foo?', req == Dummy.foo)
