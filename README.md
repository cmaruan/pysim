# PYSIM
A tool to run parametrized simulations

## Instalation
For now, this package resides on TestPyPI. To install it, simply run

```
pip install -i https://test.pypi.org/simple/ py-sim
```

## Configuration
Py-Sim needs a configuration file to be able to run. The location of this file should be set in the 
environment variable PYSIM_SETTINGS. 

#### Example
Consider the folder pysim/sample 

```
pysim/sample
├── CMakeLists.txt
├── rect_area.c
└── settings.py
```
First, let's compile `rect_area.c` to have a executable to work with.
```bash
$ cd pysim/sample
$ mkdir build && cd build
$ cmake ..
$ cmake --build .
```

Your folder should look like this
```bash
$ tree pysim/sample/ -L 2
pysim/sample/
├── CMakeLists.txt
├── build
│   ├── CMakeCache.txt
│   ├── CMakeFiles
│   ├── Makefile
│   ├── cmake_install.cmake
│   └── rect_area
├── rect_area.c
└── settings.py
```

If we inspect `pysim/sample/rect_area.c`, we'll notice two command line arguments:
* `--height`: height of a rectagle
* `--width`: width of a rectagle

We have been asked to calculate the area for all possible rectangles of sides less than 10, where
the height is an even number, and width is an odd number. We already have `pysim/sample/build/rect_area` that 
calculate areas for us. Let's configure PySim to to the work for us.

Take a look into `pysim/sample/settings.py` 

```python
# file pysim/sample/settings.py

# List of values for each parameter
HEIGHTS = [2, 4, 6, 8]
WIDTHS = [1, 3, 5, 7, 9]

# Possible values for each command line argument 
ARGS = {
    '--height': HEIGHTS,
    '--width': WIDTHS,
}

# Binary
EXECUTABLE = 'pysim/sample/build/rect_area'

# If True, pysim will capture all SIGINT interruptions and
# send them to pysim.core.signals.keyboard_interrupt.
CAPTURE_SIGINT = True

# Sample plugins 
PLUGINS = [
    'pysim.plugins.LogEvents',
    'pysim.plugins.SaveIntermediaryState',
    'pysim.plugins.GracefulKeyboardInterrupt',
]
```

There are four variables relevant to `pysim` defined here:

##### `ARGS`
`ARGS` is a dictionary containing all possible values a given parameter can have. For our example, --heights are even numbers below 10 and --width are odd numbers below 10

`pysim` will list all possible combinations for this values and create a `job` object. Each `job` contains information about the executable and parameters. To execute it, `pysim` lauches a subprocess to take care of that execution. 

##### `EXECUTABLE`
The path to the executable.
This is the **only mandatory** field in a `settings.py` file.

##### `CAPTURE_SIGINT`
Special flag that tels `pysim` to capture all Ctrl-C events. Internally, it notify all handlers registered to `pysim.core.signals.keyboard_interrupt` when SIGINT happens 

##### `PLUGINS`
Here is the nice feature about `pysim`. You may add new functionality by passing a plugin class here. Plugin classes are called only once. Its constructor is responsible for registering to any signal of interest to capture events throught the execution of `pysim`

At last, we tell `pysim` where to find our settings file and run it.


```
$ export PYSIM_SETTINGS=pysim.sample.pysim_settings
$ python3 -m pysim
Area(h=2, w=1) = 2
<Job id=0 status=COMPLETED>
Area(h=2, w=3) = 6
<Job id=1 status=COMPLETED>
Area(h=2, w=5) = 10
<Job id=2 status=COMPLETED>
Area(h=2, w=7) = 14
<Job id=3 status=COMPLETED>
...
Area(h=8, w=9) = 72
<Job id=19 status=COMPLETED>
```



