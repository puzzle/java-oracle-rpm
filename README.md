# RPM for Oracle Java

## What is it?

* A simple RPM for Oracle Java
* Not compiled from sources, but using the binary download from Oracle as source for the RPM

## How to create the non-distributable source tarball?

* Download binary from Oracle
* Run binary
* Rename extracted folder to e.g. java-1.6.0-oracle-1.6.0.32-x64
* Create tarball: `tar czf java-1.6.0-oracle-1.6.0.32-x64.tgz java-1.6.0-oracle-1.6.0.32-x64`
* Versions and architecture must match RPM spec file
