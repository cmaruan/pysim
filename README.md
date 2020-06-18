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
Assume the following tree structure for a current project
```
cool-image-codec/
├── bin
│   └── codec
├── images
│   └── fig1.png
│   └── fig2.png
│   └── fig3.png
└── simulations
    └── pysim_settings.py
```

The binary `codec` accepts two comand line arguments:
* `--image`: path to an image to commpress
* `--quality`: quality of compression. Value between 0 and 100.

Assume we want to run for each image a different set of qualities. To do achieve that, we edit `pysim_settings.py` as such:

```python

# List of values for each parameter
IMAGE_LIST = ['fig1.png', 'fig2.png', 'fig3.png', ]
QUALITY_LIST = [10, 35, 50, 75]

# Arguments
ARGS = {
    '--image': IMAGE_LIST,
    '--quality': QUALITY_LIST,
}

# Binary
EXECUTABLE = 'bin/codec'
```

From there, `pysim` will create a list of jobs from every possible combination of `IMAGE_LIST` and  `QUALITY_LIST`

First, we should let pysim know where the settings file is saved. Then, simply call the module.

```
$ export PYSIM_SETTINGS=simulations.pysim_settings
$ python3 -m pysim
```

Please note that the path to the settings module should be relative to where you will call `pysim`. 

