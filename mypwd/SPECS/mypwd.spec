%define _topdir /home/lherrada/rpms/mypwd
%define _tmppath /home/lherrada/rpms/mypwd/tmp
%define name mypwd 
%define version 0.1
%define release 1

Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: This is a customized version of command pwd 
Group: Basic Tools 
License: Herrada License
Source0: mypwd-0.1.tar.gz
Packager: Luis Herrada <lherrada@yahoo.com>
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXX)

%description
This command provides was created to understand the concept of i-node.
This code finds the current working directory by finding all i-node entries
in parent directory (..) and from that list, getting the i-node that corresponds to the
current working directory (.) . This process is repeated until we reach the i-node root (/).

%prep
%setup -q

%build
make all

%install
install --directory $RPM_BUILD_ROOT/bin
install -m 0744 mypwd $RPM_BUILD_ROOT/bin
#make install

%clean
rm -rf %{buildroot}

%files
/bin/mypwd
