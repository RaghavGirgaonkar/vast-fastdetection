# Changes to ```vaster```

## General Changes
### Scripts
- Modified slurm scripts to include email notications for start and end of jobs. Can be specified in the ```config.yml``` file.
- Modified ```config.yml``` file to include paths to singularity images and scripts to load casa and conda.
- Added node-specifying option to ```submit_slurm_jobs``` utlity. For eg, ```submit_slurm_jobs 50230 -b 0 --nodes=execute-2002 --steps FIXDATA MODELING IMGFAST SELCAND``` 
  will run the intensive steps FIXDATA and MODELING on that node in the HPC cluster.

### Modeling
- Tweaked wsclean parameters: ```-channels-out 4 -fit-spectral-pol 2 -auto-threshold 0.3 -auto-mask 3```, yeilds better modeling of frequency dependent features by fitting two taylor terms
  similar to ```nterms=2``` in CASA using 4 subbanded images. Summary of all tests and tweaks can be found here: [wsclean_modeling_tests](https://docs.google.com/document/d/1J0IZDvFOUKTGWUEXHAZbDbWNlJzxvIESttA5tdBH-ns/edit?usp=sharing)
- Added a phase selfcal option through a script ```casa_phase_selfcal.py``` between two wsclean runs.

### Container
- Create singularity container ```vaster_singularity.sif``` for vaster. It can run on linux systems. Modified scripts so that they use this container for the various steps. **Still under testing**.


## Mortimer-based changes
### Scripts 
- Removed ```#TIME``` from slurm file header (not needed on mortimer).
- Added load conda and casa lines in slurm batch file headers. 
- Modified slurm scripts to include email notications for start and end of jobs. Can be specified in the ```config.yml``` file.
- Modified ```config.yml``` file to include paths to singularity images and scripts to load casa and conda.

### Modeling 
- Created a branch which runs CASA modeling in parallel using ```mpicasa```, works but not tested extensively since change to wsclean was formalized.
- Tweaked wsclean parameters: ```-channels-out 4 -fit-spectral-pol 2 -auto-threshold 0.3 -auto-mask 3```, yeilds better modeling of frequency dependent features by fitting two taylor terms
  similar to ```nterms=2``` in CASA using 4 subbanded images.
- Added a phase selfcal option through a script ```casa_phase_selfcal.py``` between two wsclean runs.