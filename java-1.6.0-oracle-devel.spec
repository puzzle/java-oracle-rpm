%global majorver 1.6.0
%global minorver 32
%global releasever 2
%global priority 16200
%global javaver %{majorver}.%{minorver}
%global shortname java-%{majorver}-oracle-devel
%global longname %{shortname}-%{javaver}
# _jvmdir macro not working
%global jvmdir /usr/lib/jvm
%global installdir %{jvmdir}/java-%{majorver}-oracle.x86_64

Name:	%{shortname}
Version: %{javaver}
Release: puzzle.%{releasever}%{?dist}
Summary: Oracle Java SE Development Kit

Group: Development/Languages
License: Oracle Corporation Binary Code License
URL: http://www.oracle.com/technetwork/java/javase/overview/index.html
Source0: %{longname}-x86_64.tgz
BuildArch: x86_64
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives

%description
Tools to develop Java programs.

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
  --slave %{jvmdir}/jre jre %{installdir}/jre \
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
  --install %{_bindir}/javac javac %{installdir}/bin/javac %{priority} \
  --slave %{jvmdir}/jdk jdk %{installdir} \
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

%postun
if [ $1 -eq 0 ]
then
  alternatives --remove java %{installdir}/bin/java
  alternatives --remove javac %{installdir}/bin/javac
fi

%changelog
* Thu Jun 6 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-puzzle.2
- Fix: /usr/lib/jvm/jre link was missing
- Re-added libodbc fix, bug somehow reappeared
- Changed name from java-...-jdk to java-...-devel

* Thu May 31 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-puzzle.1
- A simple RPM for Oracle Java, not using sources but binary archive from Oracle
