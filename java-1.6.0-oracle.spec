%global version_major 1.6.0
%global version_minor 32
%global version %{version_major}.%{version_minor}
%global name java-%{version_major}-oracle
%global fullname %{name}-%{version}
%global installdir /usr/lib/jvm/%{fullname}
%global arch x64


Name:	%{name}
Version: %{version}
Release: 1puzzle
Summary: Oracle Java SE Runtime Environment

Group: Development/Languages
License: Oracle Corporation Binary Code License
URL: http://www.oracle.com/technetwork/java/javase/overview/index.html
Source0: %{fullname}-%{arch}.tgz

BuildArch: x86_64

%description
Environment to run Java programs.

%prep
%setup -q -n %{fullname}-%{arch}

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT%{installdir}

%files
%defattr(-,root,root,-)
%dir %{installdir}

%post
# alternatives ...

%changelog
* Thu May 31 2012 Anselm Strauss <strauss@puzzle.ch> - 1.6.0.32-1puzzle
- A simple and basic RPM for Oracle Java, written from scratch
