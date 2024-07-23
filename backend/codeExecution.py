import sys
import traceback
from io import StringIO
import multiprocessing as mp

class CaptureOutput:
    def __enter__(self):
        self._stdout_output = ''
        self._stderr_output = ''

        self._stdout = sys.stdout
        sys.stdout = StringIO()

        self._stderr = sys.stderr
        sys.stderr = StringIO()

        return self

    def __exit__(self, *args):
        self._stdout_output = sys.stdout.getvalue()
        sys.stdout = self._stdout

        self._stderr_output = sys.stderr.getvalue()
        sys.stderr = self._stderr

    def get_stdout(self):
        return self._stdout_output

    def get_stderr(self):
        return self._stderr_output
    

def execute(code : str):
    queue = mp.Queue()
    p = mp.Process(target=worker, args=(code, queue))
    p.start()
    # Must do this call before call to join:

    timeout = False
    try:
        stdout_output, stderr_output = queue.get(True, 5.0)
    except Exception:
        stdout_output = ""
        stderr_output = ""
        print("There has been a timeout waiting for queue")
        timeout = True

    # Check to see if the process timed out and add error message for that
    p.join(1.0)
    if p.is_alive():
        print("There has been a timeout waiting for join")
        trimmedError = "[ERROR] Your code timed out after 5 seconds and did not complete."
        timeout = True

    # This will kill the process if it is still running past timeout
    p.terminate()
    p.join()
    
    # Check to see whether process has been ended
    if p.is_alive():
        print("Code execution process orphaned.")
    else:
        # This will release all resource associated with the process
        p.close()
        print("Code execution process successfully closed.")

    if not timeout:
        trimmedError = stderr_output
        strippedError = str(stderr_output).strip()
        if(len(strippedError) != 0):
            # We only want to grab the error type and string, not the stack trace from the execution engine
            firstNewline = strippedError.rindex('\n')
            trimmedError = strippedError[firstNewline + 1 : ]

    return stdout_output, trimmedError


def worker(code, queue):
    with CaptureOutput() as capturer:
        try:
            runCode(code)
        except Exception:
            print(traceback.format_exc(), file=sys.stderr)
    queue.put((capturer.get_stdout(), capturer.get_stderr()))


def runCode(code : str):
    # set globals parameter to none
    globalsParameter = {'__builtins__' : None}
    # set locals parameter to take only print()
    localsParameter = {'print': print, 'str': str}
    # successful execution will result in None returned
    return exec(code, globalsParameter, localsParameter)