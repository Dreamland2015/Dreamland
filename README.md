# Dreamland
That desert thing. 

The Flux Foundation 

Setup instructions:

Edit configs list of dicts in SetupDreamland.py.
Run SetupDreamland.

This will take the base pi image, update the apt sources.list, install
supervisor and config files for fadecandy, structure_input, and
structure_output, as well as return rc.local to original state.

Fadecandy is run from supervisor and reads config from /etc/fcserver.json.


