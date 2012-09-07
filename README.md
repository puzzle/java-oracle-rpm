# RPM for Oracle Java

## What is it?

* A simple RPM for Oracle Java
* Not compiled from sources, but using the binary download from Oracle as source for the RPM
* Only x86\_64 is supported, I could not run the 32bit binaries from Oracle on 64bit, sorry ...

## jre/jdk/devel packages

* In RedHat tradition there is a java-\<version\>-\<origin\> RPM that contains the JRE and is complemented by the -devel package that contains additional JDK data and depends on the JRE package. However, this is not how Oracle distributes Java. The Oracle JDK includes the JRE. You can install both at the same time, but you do not have to. So for Oracle the devel package does not require the JRE package.

## Howto 

* Download binary tarball from Oracle, like jdk-7u7-linux-x64.tar.gz, to ~/rpmbuild/SOURCES
* Install mock, add your user to the mock group
* Start the build, e.g. with the included mockbuild script: `./mockbuild.sh fedora-17-x86_64 fc17 1.7.0.7 1 1`
