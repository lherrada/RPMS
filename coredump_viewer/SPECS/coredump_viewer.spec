%define _topdir /home/lherrada/RPMS/coredump_viewer
%define _tmppath /home/lherrada/RPMS/coredump_viewer/tmp
%define name coredump_viewer
%define version 1.0
%define release 1

Name: %{name}
Version: %{version}
Release: 1%{?dist}
Summary: Package that collects coredumps and store it in a specific path for web view.
Group: Basic Tools
License: Herrada License
Source0: coredump_viewer-%{version}.tar.gz
Packager: Luis Herrada <lherrada@yahoo.com> 
Requires: gdb
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXXX)

%description
This package collects coredumps generated by running process and store it in a specific path.
Then, it generates a debug output using gdb tool. Finally coredump and debug output can be analized 
and downloaded by accessing http://hostname:8050/
The start of the web server (developed in python) is controlled by upstart (coredump.conf).

%prep
%setup -q

%build
%install
rm -rf %{buildroot}
#echo "|/bin/coredump1.py -e %e -t %t" > /proc/sys/kernel/core_pattern

install --directory $RPM_BUILD_ROOT/bin
install -m 0755 coredump1.py $RPM_BUILD_ROOT/bin
install -m 0755 core.sh $RPM_BUILD_ROOT/bin 

install --directory $RPM_BUILD_ROOT/etc
install --directory $RPM_BUILD_ROOT/etc/coredumps
install -m 0755 core.json $RPM_BUILD_ROOT/etc/coredumps

install --directory $RPM_BUILD_ROOT/var
install --directory $RPM_BUILD_ROOT/var/coredumps
install -m 0755 README.txt $RPM_BUILD_ROOT/var/coredumps

mkdir -p $RPM_BUILD_ROOT/var/service/coredumps/log
install -m 0755 run $RPM_BUILD_ROOT/var/service/coredumps/
install -m 0755 runlog $RPM_BUILD_ROOT/var/service/coredumps/log/run

mkdir -p $RPM_BUILD_ROOT/etc/init
install -m 0644 init/coredump.conf $RPM_BUILD_ROOT/etc/init

mkdir -p $RPM_BUILD_ROOT/service/
ln -sf /var/service/coredumps $RPM_BUILD_ROOT/service/coredumps

%clean
rm -rf %{buildroot}


%files
/bin/coredump1.py
/bin/core.sh
/etc/coredumps/core.json
/var/coredumps/README.txt
/var/service/coredumps/*
/service/coredumps
/etc/init/coredump.conf
