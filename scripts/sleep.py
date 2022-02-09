import sys
sys.path.append('hyperdrive')
from TimeMachine import TimeTraveller  # noqa autopep8

time = sys.argv[1] or "00:00"
traveller = TimeTraveller()

print(time)
traveller.sleep_until(time)
