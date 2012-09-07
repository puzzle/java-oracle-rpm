%global majorver 1.7.0
%global minorver 7
%global releasever 1
%global priority 17007
%global javaver %{majorver}.%{minorver}
%global shortname java-%{majorver}-oracle
%global longname %{shortname}-%{javaver}
%global installdir %{_jvmdir}/jre-%{majorver}-oracle.x86_64
%global jarinstalldir %{_jvmjardir}/jre-%{majorver}-oracle.x86_64

%define debug_package %{nil}

# convert absolute to relative path
%define script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%define abs2rel %{__perl} -e %{script}

Name:	%{shortname}
Version: %{javaver}
Release: puzzle.%{releasever}%{?dist}
Epoch: 1
Summary: Oracle Java SE Runtime Environment
Group: Development/Languages
License: Oracle Corporation Binary Code License
URL: http://www.oracle.com/technetwork/java/javase/overview/index.html
Source0: jre-7u%{minorver}-linux-x64.tar.gz
BuildArch: x86_64
BuildRequires: jpackage-utils
BuildRequires: perl
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives
Provides: jre-%{majorver}-oracle = %{epoch}:%{version}-%{release}
Provides: jre-oracle = %{epoch}:%{version}-%{release}
Provides: jre-%{majorver} = %{epoch}:%{version}-%{release}
Provides: java-%{majorver} = %{epoch}:%{version}-%{release}
Provides: jre = %{majorver}
Provides: java-oracle = %{epoch}:%{version}-%{release}
Provides: java = %{epoch}:%{majorver}
Provides: jndi = %{epoch}:%{version}
Provides: jndi-ldap = %{epoch}:%{version}
Provides: jndi-cos = %{epoch}:%{version}
Provides: jndi-rmi = %{epoch}:%{version}
Provides: jndi-dns = %{epoch}:%{version}
Provides: jaas = %{epoch}:%{version}
Provides: jsse = %{epoch}:%{version}
Provides: jce = %{epoch}:%{version}
Provides: jdbc-stdext = 3.0
Provides: java-sasl = %{epoch}:%{version}
Provides: java-fonts = %{epoch}:%{version}

%if 0%{?el5}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

%description
Environment to run Java programs.

%prep
%setup -q -n jre%{majorver}_0%{minorver}
# replace libodbc dependencies, fedora/redhat only provides libodbc(inst).so.n but no libodbc(inst).so
%global _use_internal_dependency_generator 0
%global requires_replace /bin/sh -c "%{__find_requires} | %{__sed} -e 's/libodbc.so/libodbc.so.2/;s/libodbcinst.so/libodbcinst.so.2/'"
%global __find_requires %{requires_replace}

%build
# nope

%install
rm -rf $RPM_BUILD_ROOT
# ldd dependencies of the following libraries can not be resolved in the distribution, so remove them
rm lib/amd64/fxavcodecplugin-52.so lib/amd64/fxavcodecplugin-53.so lib/amd64/fxplugins.so
install -d -m 755 $RPM_BUILD_ROOT%{installdir}
cp -a * $RPM_BUILD_ROOT%{installdir}
install -d -m 755 $RPM_BUILD_ROOT%{jarinstalldir}
pushd $RPM_BUILD_ROOT%{jarinstalldir}
  RELATIVE=$(%{abs2rel} %{installdir}/lib %{jarinstalldir})
  ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
  ln -sf $RELATIVE/jce.jar jce-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
  ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
  ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
  ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
  ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
  ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
  for jar in *-%{version}.jar; do
    ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{majorver}.jar|g")
    ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
  done
popd
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
find $RPM_BUILD_ROOT -type d | sed 's|'$RPM_BUILD_ROOT'|%dir |' >> files
find $RPM_BUILD_ROOT -type f -o -type l | sed 's|'$RPM_BUILD_ROOT'||' >> files

%files -f files

%post
alternatives \
  --install %{_bindir}/java java %{installdir}/bin/java %{priority} \
  --slave %{_jvmdir}/jre jre %{installdir} \
  --slave %{_jvmjardir}/jre jre_exports %{jarinstalldir} \
  --slave %{_bindir}/java_vm java_vm %{installdir}/bin/java_vm \
  --slave %{_bindir}/javaws javaws %{installdir}/bin/javaws \
  --slave %{_bindir}/jcontrol jcontrol %{installdir}/bin/jcontrol \
  --slave %{_bindir}/keytool keytool %{installdir}/bin/keytool \
  --slave %{_bindir}/orbd orbd %{installdir}/bin/orbd \
  --slave %{_bindir}/pack200 pack200 %{installdir}/bin/pack200 \
  --slave %{_bindir}/policytool policytool %{installdir}/bin/policytool \
  --slave %{_bindir}/rmid rmid %{installdir}/bin/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{installdir}/bin/rmiregistry \
  --slave %{_bindir}/servertool servertool %{installdir}/bin/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{installdir}/bin/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{installdir}/bin/unpack200 \
  --slave %{_mandir}/man1/java.1 java.1 %{installdir}/man/man1/java.1 \
  --slave %{_mandir}/man1/keytool.1 keytool.1 %{installdir}/man/man1/keytool.1 \
  --slave %{_mandir}/man1/orbd.1 orbd.1 %{installdir}/man/man1/orbd.1 \
  --slave %{_mandir}/man1/pack200.1 pack200.1 %{installdir}/man/man1/pack200.1 \
  --slave %{_mandir}/man1/policytool.1 policytool.1 %{installdir}/man/man1/policytool.1 \
  --slave %{_mandir}/man1/rmid.1 rmid.1 %{installdir}/man/man1/rmid.1 \
  --slave %{_mandir}/man1/rmiregistry.1 rmiregistry.1 %{installdir}/man/man1/rmiregistry.1 \
  --slave %{_mandir}/man1/servertool.1 servertool.1 %{installdir}/man/man1/servertool.1 \
  --slave %{_mandir}/man1/tnameserv.1 tnameserv.1 %{installdir}/man/man1/tnameserv.1 \
  --slave %{_mandir}/man1/unpack200.1 unpack200.1 %{installdir}/man/man1/unpack200.1
alternatives \
  --install %{_jvmdir}/jre-oracle jre_oracle %{installdir} %{priority} \
  --slave %{_jvmjardir}/jre-oracle jre_oracle_exports %{jarinstalldir}
alternatives \
  --install %{_jvmdir}/jre-%{majorver} jre_%{majorver} %{installdir} %{priority} \
  --slave %{_jvmjardir}/jre-%{majorver} jre_%{majorver}_exports %{jarinstalldir}
alternatives \
  --install %{_libdir}/mozilla/plugins/libjavaplugin.so libjavaplugin.so.x86_64 %{installdir}/lib/amd64/libnpjp2.so %{priority} \
  --slave %{_bindir}/javaws javaws %{installdir}/bin/javaws

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove java %{installdir}/bin/java
  alternatives --remove jre_oracle %{installdir}
  alternatives --remove jre_%{majorver} %{installdir}
  alternatives --remove libjavaplugin.so.x86_64 %{installdir}/lib/amd64/libnpjp2.so
fi

%changelog
* Tue Sep 04 2012 Anselm Strauss <strauss@puzzle.ch> - 1.7.0.7-puzzle.1
- Initial version, copied from 1.6.0.35-puzzle.1
- Removed javafx plugin libraries, can not resolve ldd deps
