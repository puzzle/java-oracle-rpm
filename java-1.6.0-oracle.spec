%global majorver 1.6.0
%global minorver 33
%global releasever 1
%global priority 16100
%global javaver %{majorver}.%{minorver}
%global shortname java-%{majorver}-oracle
%global longname %{shortname}-%{javaver}
# _jvmdir macro not working
%global jvmdir /usr/lib/jvm
%global installdir %{jvmdir}/jre-%{majorver}-oracle.x86_64

Name:	%{shortname}
Version: %{javaver}
Release: puzzle.%{releasever}%{?dist}
Summary: Oracle Java SE Runtime Environment

Group: Development/Languages
License: Oracle Corporation Binary Code License
URL: http://www.oracle.com/technetwork/java/javase/overview/index.html
Source0: %{longname}-x86_64.tgz
BuildArch: x86_64
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives

%description
Environment to run Java programs.

%prep
%setup -q -n %{longname}-x86_64
# replace libodbc dependencies, fedora/redhat only provides libodbc(inst).so.n but no libodbc(inst).so
%global _use_internal_dependency_generator 0
%global requires_replace /bin/sh -c "%{__find_requires} | %{__sed} -e 's/libodbc.so/libodbc.so.2/;s/libodbcinst.so/libodbcinst.so.2/'"
%global __find_requires %{requires_replace}


%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{installdir}
cp -a * $RPM_BUILD_ROOT%{installdir}
find $RPM_BUILD_ROOT%{installdir} -type d | sed 's|'$RPM_BUILD_ROOT'|%dir |' >> files
find $RPM_BUILD_ROOT%{installdir} -type f -o -type l | sed 's|'$RPM_BUILD_ROOT'||' >> files

%files -f files

%post
alternatives \
  --install %{_bindir}/java java %{installdir}/bin/java %{priority} \
  --slave %{jvmdir}/jre jre %{installdir} \
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

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove java %{installdir}/bin/java
fi

%changelog
* Thu Jun 14 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.1
- Updated to Java Release 33

* Thu Jun 6 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-puzzle.2
- Re-added libodbc fix, bug somehow reappeared
- Changed name from java-...-jre to java-...

* Thu May 31 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-puzzle.1
- A simple RPM for Oracle Java, not using sources but binary archive from Oracle
