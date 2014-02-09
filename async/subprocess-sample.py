import asyncio
import sys
from asyncio import subprocess

@asyncio.coroutine
def getstatusoutput(*args):
    proc = yield from asyncio.create_subprocess_exec(
                                  *args,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
    try:
        stdout, _ = yield from proc.communicate()
    except:
        proc.kill()
        yield from proc.wait()
        raise
    exitcode = yield from proc.wait()
    return (exitcode, stdout)

loop = asyncio.get_event_loop()
coro = getstatusoutput(sys.executable, '-m', 'platform')
exitcode, stdout = loop.run_until_complete(coro)
if not exitcode:
    stdout = stdout.decode('ascii').rstrip()
    print("Platform: %s" % stdout)
else:
    print("Python failed with exit code %s:" % exitcode)
    sys.stdout.flush()
    sys.stdout.buffer.flush()
    sys.stdout.buffer.write(stdout)
    sys.stdout.buffer.flush()
loop.close()
