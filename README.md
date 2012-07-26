# RPM for Oracle Java

## What is it?

* A simple RPM for Oracle Java
* Not compiled from sources, but using the binary download from Oracle as source for the RPM
* Only x86\_64 is supported, I could not run the 32bit binaries from Oracle on 64bit, sorry ...

## jre/jdk/devel packages

* In RedHat tradition there is a java-\<version\>-\<origin\> RPM that contains the JRE and is complemented by the -devel package that contains additional JDK data and depends on the JRE package. However, this is not how Oracle distributes Java. The Oracle JDK includes the JRE. You can install both at the same time, but you do not have to. So for Oracle the devel package does not require the JRE package.

## How to create the non-distributable source tarball for building the RPM?

* Download binary tarball from Oracle
* Run binary
* Rename extracted folder, e.g. for JRE: java-1.6.0-oracle-1.6.0.32-x86\_64, for JDK: java-1.6.0-oracle-devel-1.6.0.32-x86\_64
* Create tarball: `tar czf java-1.6.0-oracle-1.6.0.32-x86_64.tgz java-1.6.0-oracle-1.6.0.32-x86_64`
* Versions, architecture and extension (devel) must match RPM spec file
