# List of values for each parameter
HEIGHTS = [2, 4, 6, 8]
WIDTHS = [3, 5, 7, 9]

ARGS = {
    '--height': HEIGHTS,
    '--width': WIDTHS,
}


# Binary
EXECUTABLE = 'pysim/sample/build/rect_area'

# If True, pysim will capture all SIGINT interruptions and
# send them to pysim.core.signals.keyboard_interrupt.
# CAPTURE_SIGINT = True

# Sample plugins 
PLUGINS = [
    'pysim.plugins.LogEvents',
    'pysim.plugins.SaveIntermediaryState',
    'pysim.plugins.GracefulKeyboardInterrupt',
]