0.1.2
- bugfix: useOtherPC was not used, now if this is false, it actually does not run anything on the otherPC
- feature: so far, only the EEG stream was exported. Now we simply use all streams where sampling-rate is >0.0 (everything else is used as marker)

0.1.1
- changed test infrastructure. no longer creates config file in .config/lslautobids.
- added initial test for successful build
- Bugfix with paths not being build with join
