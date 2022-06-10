VariantPicker.m decides which COV-2 variant is present for each qPCR run specified in runs.txt.
It looks at the measured flourescence in DATA.mat and calculates the strongest mutations in each 
run based off the slope of their flourescence curves.
It writes out the strongest mutation for each set of mutations (417, 452, 484, 501, and 614), \
and then which COV-2 variant that certain set of mutations is responsible for (see VariantPicker.m for how each variant is picked).
This is written to be run inside a MATLAB directory containing qPCR run files that have specific .MAT data files specific to Torus Biosystems protocol.
