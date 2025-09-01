from pybricks.parameters import Button
from pybricks.tools import wait
from movement import hub
import run1, run2, run3, run4  # make sure your runs are in Code/ folder with __init__.py
from pybricks.hubs import PrimeHub

# List of run functions
runs = [run1.run, run2.run, run3.run, run4.run]
current_run = 0

# Display initial selection

while True:
    hub = PrimeHub()
    pressed = hub.buttons.pressed()

    # Scroll through runs with RIGHT button
    if Button.RIGHT in pressed:
        current_run = (current_run + 1) % len(runs)
        hub.display.number(current_run + 1)

        wait(400)  # debounce to avoid multiple triggers

    # Start run with LEFT button
    elif Button.LEFT in pressed:

        runs[current_run]()  # execute the run

        # Pause after run

        wait(1000)

        # Return to selection screen

