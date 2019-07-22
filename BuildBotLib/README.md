# QmakeModule
For the module to work correctly, the project must support the following targets:
* test - run tests;
* deploy - deploy a project (collect dependencies in the distribution) use cqtdeployer;
* release - adding a new version to all supported sites,
or if there are none, add up everything in PWD/Release;
