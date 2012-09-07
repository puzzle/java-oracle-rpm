#!/bin/sh -e

chroot=$1
dist=$2
version=$3
release=$4
releaseDevel=$5

cd `dirname $0`

mock -r $chroot --buildsrpm --spec java-1.7.0-oracle.spec --sources ~/rpmbuild/SOURCES
cp -v /var/lib/mock/$chroot/result/java-1.7.0-oracle-$version-puzzle.$release.$dist.src.rpm ~/rpmbuild/SRPMS
mock -r $chroot --rebuild ~/rpmbuild/SRPMS/java-1.7.0-oracle-$version-puzzle.$release.$dist.src.rpm
cp -v /var/lib/mock/$chroot/result/java-1.7.0-oracle-$version-puzzle.$release.$dist.x86_64.rpm ~/rpmbuild/RPMS

mock -r $chroot --buildsrpm --spec java-1.7.0-oracle-devel.spec --sources ~/rpmbuild/SOURCES
cp -v /var/lib/mock/$chroot/result/java-1.7.0-oracle-devel-$version-puzzle.$releaseDevel.$dist.src.rpm ~/rpmbuild/SRPMS
mock -r $chroot --rebuild ~/rpmbuild/SRPMS/java-1.7.0-oracle-devel-$version-puzzle.$releaseDevel.$dist.src.rpm
cp -v /var/lib/mock/$chroot/result/java-1.7.0-oracle-devel-$version-puzzle.$releaseDevel.$dist.x86_64.rpm ~/rpmbuild/RPMS
