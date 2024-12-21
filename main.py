import time
from log_output import add_time, forgot_checkout

try:
    add_time("50647504")
    time.sleep(10)
except KeyboardInterrupt:
    forgot_checkout()
