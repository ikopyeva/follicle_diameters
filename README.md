follicle_diameters
==============================

ChE 696 project to compare ovarian follicle growth in 3 dimensional hydrogel
culture, with different extracellular matrix sequestering peptides. Follicles
are notoriously hard to culture due to their extreme sensitivity.
Incorporating these peptides into the poly(ethylene glycol) matrix will ideally
promote growth and reconstruction of the extracellular components of thfollicle.
For example, these are the peptides included in the data folder.

HBP = heparin binding peptide
BMB = basement membrane binder peptide
RGD = adhesion peptide

Data is collected every two days for 12 days via Leica microscope and diameter is measured with
ImageJ and compiled into csv file.

Follicle_diameters takes these CSV files and checks whether or not 
the follicles died on a certain day (evidenced by unchanging values or
changing by approximately 1 um which can be attributed to measurement human
error). It then deletes the repetitive data from dead follicles. It calculates the
average and standard deviation of follicle diameter of the peptide trial for each day
and plots this. It also plots the survival curve of follicles with each
condition.

Python packages used:
sys
argparse
matplotlib.pyplot
os
pandas
pathlib

### Copyright

Copyright (c) 2018, ikopyeva


#### Acknowledgements
 
Project based on the 
[Computational Chemistry Python Cookiecutter](https://github.com/choderalab/cookiecutter-python-comp-chem)
