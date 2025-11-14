# Solar Variability Capstone Project

- __Authors__: Nathan Besch, Laura Hayes, Caitríona M. Jackman

This is the codebase for my capstone project on Solar Wind Variability using [in-situ data from Nasa's Parker Solar Probe (PSP) and Advanced Composition Explorer (ACE) as well as ESA's Solar Orbiter (SO)]( https://cdaweb.gsfc.nasa.gov/sp_phys/data/).

## Installation Steps (recommended)

__Requirements__: git, Python 3.13.7, environment management system for Python (conda, pyenv...)

Clone the repository in your desired directory:

```
git clone https://github.com/BlueNeptune11/sun_capstone.git
```
We recommend creating a new Python 3.13.7 environment using your preferred tool. Go to the root of the repo and install the required project packages in your newly created environment:
```
pip install --upgrade pip
pip install -r requirements.txt
```

## Contents

This repositroy includes:

-Exploratory Notebook showing MAG-RTN and Plasma data comparisons for a short time frame, between Solar Orbiter, Parker Solar Probe and ACE.
-Plot showing SOLO/PSP data coverage w.r.t. solar cycle using sunspot number.
-Notebook detailing how to obtain datasets using SunPy and CDAWeb.
-Notebook analysing fitting of radial relationship power laws (SOLO/PSP data).
-Notebook detailing histogram analysis of different solar wind quantities with case study for edge cases (SOLO/PSP/ACE).
-Notebook looking at a case study for spacecraft alignment (SOLO/PSP).
-Python script for data specific functions.
-Python script for fitting specific functions.