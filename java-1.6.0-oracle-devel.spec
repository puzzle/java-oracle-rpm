%global majorver 1.6.0
%global minorver 35
%global releasever 1
%global priority 16035
%global javaver %{majorver}.%{minorver}
%global shortname java-%{majorver}-oracle-devel
%global longname %{shortname}-%{javaver}
%global installdir %{_jvmdir}/java-%{majorver}-oracle.x86_64
%global jarinstalldir %{_jvmjardir}/java-%{majorver}-oracle.x86_64

%define debug_package %{nil}

# convert absolute to relative path
%define script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%define abs2rel %{__perl} -e %{script}

Name:	%{shortname}
Version: %{javaver}
Release: puzzle.%{releasever}%{?dist}
Epoch: 1
Summary: Oracle Java SE Development Kit
Group: Development/Languages
License: Oracle Corporation Binary Code License
URL: http://www.oracle.com/technetwork/java/javase/overview/index.html
Source0: jdk-6u%{minorver}-linux-x64.tar.gz
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
Provides: java-sdk-%{majorver}-oracle = %{epoch}:%{version}
Provides: java-sdk-%{majorver} = %{epoch}:%{version}
Provides: java-sdk-oracle = %{epoch}:%{version}
Provides: java-sdk = %{epoch}:%{majorver}
Provides: java-%{majorver}-devel = %{epoch}:%{version}
Provides: java-devel-oracle = %{epoch}:%{version}
Provides: java-devel = %{epoch}:%{majorver}

%if 0%{?el5}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

%description
Tools to develop Java programs.

%prep
%setup -q -n jdk%{majorver}_%{minorver}
# replace libodbc dependencies, fedora/redhat only provides libodbc(inst).so.n but no libodbc(inst).so
%global _use_internal_dependency_generator 0
%global requires_replace /bin/sh -c "%{__find_requires} | %{__sed} -e 's/libodbc.so/libodbc.so.2/;s/libodbcinst.so/libodbcinst.so.2/'"
%global __find_requires %{requires_replace}

%build
# nope

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{installdir}
cp -a * $RPM_BUILD_ROOT%{installdir}
install -d -m 755 $RPM_BUILD_ROOT%{jarinstalldir}
pushd $RPM_BUILD_ROOT%{jarinstalldir}
  RELATIVE=$(%{abs2rel} %{installdir}/jre/lib %{jarinstalldir})
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
  --slave %{_jvmdir}/jre jre %{installdir}/jre \
  --slave %{_jvmjardir}/jre jre_exports %{jarinstalldir} \
  --slave %{_bindir}/java_vm java_vm %{installdir}/jre/bin/java_vm \
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
  --slave %{_jvmjardir}/jre-oracle jre_oracle %{jarinstalldir}
alternatives \
  --install %{_jvmdir}/jre-%{majorver} jre_%{majorver} %{installdir} %{priority} \
  --slave %{_jvmjardir}/jre-%{majorver} jre_%{majorver} %{jarinstalldir}
alternatives \
  --install %{_bindir}/javac javac %{installdir}/bin/javac %{priority} \
  --slave %{_jvmdir}/java java_sdk %{installdir} \
  --slave %{_jvmjardir}/java java_sdk_exports %{jarinstalldir} \
  --slave %{_bindir}/appletviewer appletviewer %{installdir}/bin/appletviewer \
  --slave %{_bindir}/apt apt %{installdir}/bin/apt \
  --slave %{_bindir}/extcheck extcheck %{installdir}/bin/extcheck \
  --slave %{_bindir}/HtmlConverter HtmlConverter %{installdir}/bin/HtmlConverter \
  --slave %{_bindir}/idlj idlj %{installdir}/bin/idlj \
  --slave %{_bindir}/jar jar %{installdir}/bin/jar \
  --slave %{_bindir}/jarsigner jarsigner %{installdir}/bin/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{installdir}/bin/javadoc \
  --slave %{_bindir}/javah javah %{installdir}/bin/javah \
  --slave %{_bindir}/javap javap %{installdir}/bin/javap \
  --slave %{_bindir}/jconsole jconsole %{installdir}/bin/jconsole \
  --slave %{_bindir}/jdb jdb %{installdir}/bin/jdb \
  --slave %{_bindir}/jhat jhat %{installdir}/bin/jhat \
  --slave %{_bindir}/jinfo jinfo %{installdir}/bin/jinfo \
  --slave %{_bindir}/jmap jmap %{installdir}/bin/jmap \
  --slave %{_bindir}/jps jps %{installdir}/bin/jps \
  --slave %{_bindir}/jrunscript jrunscript %{installdir}/bin/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{installdir}/bin/jsadebugd \
  --slave %{_bindir}/jstack jstack %{installdir}/bin/jstack \
  --slave %{_bindir}/jstat jstat %{installdir}/bin/jstat \
  --slave %{_bindir}/jstatd jstatd %{installdir}/bin/jstatd \
  --slave %{_bindir}/jvisualvm jvisualvm %{installdir}/bin/jvisualvm \
  --slave %{_bindir}/native2ascii native2ascii %{installdir}/bin/native2ascii \
  --slave %{_bindir}/rmic rmic %{installdir}/bin/rmic \
  --slave %{_bindir}/schemagen schemagen %{installdir}/bin/schemagen \
  --slave %{_bindir}/serialver serialver %{installdir}/bin/serialver \
  --slave %{_bindir}/wsgen wsgen %{installdir}/bin/wsgen \
  --slave %{_bindir}/wsimport wsimport %{installdir}/bin/wsimport \
  --slave %{_bindir}/xjc xjc %{installdir}/bin/xjc \
  --slave %{_mandir}/man1/appletviewer.1 appletviewer.1 %{installdir}/man/man1/appletviewer.1 \
  --slave %{_mandir}/man1/apt.1 apt.1 %{installdir}/man/man1/apt.1 \
  --slave %{_mandir}/man1/extcheck.1 extcheck.1 %{installdir}/man/man1/extcheck.1 \
  --slave %{_mandir}/man1/idlj.1 idlj.1 %{installdir}/man/man1/idlj.1 \
  --slave %{_mandir}/man1/jar.1 jar.1 %{installdir}/man/man1/jar.1 \
  --slave %{_mandir}/man1/jarsigner.1 jarsigner.1 %{installdir}/man/man1/jarsigner.1 \
  --slave %{_mandir}/man1/javac.1 javac.1 %{installdir}/man/man1/javac.1 \
  --slave %{_mandir}/man1/javadoc.1 javadoc.1 %{installdir}/man/man1/javadoc.1 \
  --slave %{_mandir}/man1/javah.1 javah.1 %{installdir}/man/man1/javah.1 \
  --slave %{_mandir}/man1/javap.1 javap.1 %{installdir}/man/man1/javap.1 \
  --slave %{_mandir}/man1/jconsole.1 jconsole.1 %{installdir}/man/man1/jconsole.1 \
  --slave %{_mandir}/man1/jdb.1 jdb.1 %{installdir}/man/man1/jdb.1 \
  --slave %{_mandir}/man1/jhat.1 jhat.1 %{installdir}/man/man1/jhat.1 \
  --slave %{_mandir}/man1/jinfo.1 jinfo.1 %{installdir}/man/man1/jinfo.1 \
  --slave %{_mandir}/man1/jmap.1 jmap.1 %{installdir}/man/man1/jmap.1 \
  --slave %{_mandir}/man1/jps.1 jps.1 %{installdir}/man/man1/jps.1 \
  --slave %{_mandir}/man1/jrunscript.1 jrunscript.1 %{installdir}/man/man1/jrunscript.1 \
  --slave %{_mandir}/man1/jsadebugd.1 jsadebugd.1 %{installdir}/man/man1/jsadebugd.1 \
  --slave %{_mandir}/man1/jstack.1 jstack.1 %{installdir}/man/man1/jstack.1 \
  --slave %{_mandir}/man1/jstat.1 jstat.1 %{installdir}/man/man1/jstat.1 \
  --slave %{_mandir}/man1/jstatd.1 jstatd.1 %{installdir}/man/man1/jstatd.1 \
  --slave %{_mandir}/man1/jvisualvm.1 jvisualvm.1 %{installdir}/man/man1/jvisualvm.1 \
  --slave %{_mandir}/man1/native2ascii.1 native2ascii.1 %{installdir}/man/man1/native2ascii.1 \
  --slave %{_mandir}/man1/rmic.1 rmic.1 %{installdir}/man/man1/rmic.1 \
  --slave %{_mandir}/man1/schemagen.1 schemagen.1 %{installdir}/man/man1/schemagen.1 \
  --slave %{_mandir}/man1/serialver.1 serialver.1 %{installdir}/man/man1/serialver.1 \
  --slave %{_mandir}/man1/wsgen.1 wsgen.1 %{installdir}/man/man1/wsgen.1 \
  --slave %{_mandir}/man1/wsimport.1 wsimport.1 %{installdir}/man/man1/wsimport.1 \
  --slave %{_mandir}/man1/xjc.1 xjc.1 %{installdir}/man/man1/xjc.1
alternatives \
  --install %{_jvmdir}/java-oracle java_sdk_oracle %{installdir} %{priority} \
  --slave %{_jvmjardir}/java-oracle java_sdk_oracle_exports %{jarinstalldir}
alternatives \
  --install %{_jvmdir}/java-%{majorver} java_sdk_%{majorver} %{installdir} %{priority} \
  --slave %{_jvmjardir}/java-%{majorver} java_sdk_%{majorver}_exports %{jarinstalldir}
alternatives \
  --install %{_libdir}/mozilla/plugins/libjavaplugin.so libjavaplugin.so.x86_64 %{installdir}/jre/lib/amd64/libnpjp2.so %{priority} \
  --slave %{_bindir}/javaws javaws %{installdir}/bin/javaws \
  --slave %{_mandir}/man1/javaws.1 javaws.1 %{installdir}/man/man1/javaws.1

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove java %{installdir}/bin/java
  alternatives --remove jre_oracle %{installdir}
  alternatives --remove jre_%{majorver} %{installdir}
  alternatives --remove javac %{installdir}/bin/javac
  alternatives --remove java_sdk_oracle %{installdir}
  alternatives --remove java_sdk_%{majorver} %{installdir}
  alternatives --remove libjavaplugin.so.x86_64 %{installdir}/jre/lib/amd64/libnpjp2.so
fi

%changelog
* Tue Sep 04 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.35-puzzle.1
- New java release
- Changed tarball and build directory names to match Oracle scheme
- Using minor version in priority

* Thu Jul 26 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.7
- Fixed missing mozilla plugins directory for alternatives link

* Fri Jul 20 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.6
- Fixed java_vm alternative link
- Added java plugin alternative

* Fri Jun 22 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.5
- Fixed jar export links

* Fri Jun 22 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.4
- Added provides
- Added jar exports
- Added jre alternatives
- Changed alternatives priority to default
- Added epoch

* Tue Jun 19 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.3
- Set BuildRoot only for epel-5, causes problems with epel-6
- Disable find-debuginfo.sh

* Fri Jun 15 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.2
- Fix: must set BuildRoot for epel-5
- Requiring jpackage-utils for _jvmdir macro
- Added empty build section for clarity

* Fri Jun 14 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.33-puzzle.1
- Updated to Java Release 33

* Fri Jun 8 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-puzzle.3
- Fix: javac alternative should set /usr/lib/jvm/java link instead of /usr/lib/jvm/jdk

* Thu Jun 6 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-puzzle.2
- Fix: /usr/lib/jvm/jre link was missing
- Re-added libodbc fix, bug somehow reappeared
- Changed name from java-...-jdk to java-...-devel

* Thu May 31 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-puzzle.1
- A simple RPM for Oracle Java, not using sources but binary archive from Oracle
