# MiniAODBphysics2018

## Intructions to run the examples.
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_5
cd CMSSW_10_2_5/src/
cmsenv
voms-proxy-init -voms cms -valid 192:00
git clone git@github.com:mobassirameen/BsPiPAT.git
scram b
cd myAnalyzers/BsPiPAT/test/
cmsRun BsPiRootupler.py
```



