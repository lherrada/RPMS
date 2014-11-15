%define _topdir /home/lherrada/RPMS/daemontools
%define _tmppath /home/lherrada/RPMS/daemontools/tmp
%define debug_package %{nil}
%define destdir %buildroot
%define name daemontools
%define version 0.76
%global myhome /usr/local
%global pkg_docdir %{_docdir}/%{name}-%{version}
#Buildroot: %_tmppath/%{name}-%{version}-root
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-XXXXXXX)
License: Check with djb
Group: Utilities/System
Name: daemontools
Packager: Mate Wierdl <mw@csi.hu>
#Patch: %name-%version.errno.patch
Provides: daemontools
Release: 112memphis
#Source: http://cr.yp.to/%name/%name-%version.tar.gz
Source0: %name-%version.tar.gz
Summary: Various tools to start/stop/monitor daemons.
URL: http://cr.yp.to/%name.html
Version: 0.76

%description
   daemontools is a collection of tools for managing UNIX services.

   supervise monitors a service. It starts the service and restarts the
   service if it dies. Setting up a new service is easy: all supervise
   needs is a directory with a run script that runs the service.

   multilog saves error messages to one or more logs. It optionally
   timestamps each line and, for each log, includes or excludes lines
   matching specified patterns. It automatically rotates logs to limit
   the amount of disk space used. If the disk fills up, it pauses and
   tries again, without losing any data.

%prep
rm -rf %destdir
%setup -q -c -n %destdir/package
cd admin/%name-%version
#%patch -p1

%build

cd admin/%name-%version
mkdir -p %destdir%myhome/bin

sed -e 's}^parent.*}parent=/package/admin}' \
    -e 's} /command/} %destdir/command/}g' \
    -e 's}-p /command}-p %destdir/command}' \
    -e 's}ln -s %destdir/command/}ln -s /command/}' \
    -e 's} /usr/local/bin/} %destdir/usr/local/bin/}g' \
    -e 's}/usr/local}%myhome}g' \
    package/upgrade > package/upgrade'{new}' 

if [ "$?" != 0 ]; then
    exit 1
else
    mv package/upgrade'{new}' package/upgrade
    chmod 755 package/upgrade
fi

package/compile

COMPILER="Compiler: $(gcc -v 2>&1 | tail -1)"
HARDWARE="Hardware: $(uname -m)"
LIBRARY="Library: $(rpm -q glibc)"
OSVERSION="OSversion: $(uname -sr)"
PACKAGER="Packager: %packager"
REDHATRELEASE="RedHat release: $(cat /etc/redhat-release)"
RPMVERSION="rpm version: $(rpm -q rpm)"

echo "The %name rpm was created in the following environment:
" > README_rpm

echo "$COMPILER
$HARDWARE
$LIBRARY
$OSVERSION
$PACKAGER
$REDHATRELEASE
$RPMVERSION

The packager above has made a good-faith attempt to ensure
that the package behaves correctly.

Since this rpm applies a patch to the sources (to fix an
incompatibility in errno declaration), you cannot distribute it
publicly.
" >> README_rpm
 
mkdir -p %destdir/%pkg_docdir
mv package/README src/{CHANGES,TODO} README_rpm %destdir/%pkg_docdir
mkdir -p %destdir/service
mkdir -p $RPM_BUILD_ROOT/var/service

%install
cd admin/%name-%version
package/upgrade

rm compile/src

mkdir -p %destdir/etc/init
install -m 0644 package/svscan.conf %destdir/etc/init

%files
/package/admin/daemontools
/usr/local/bin/*
/package/admin/daemontools-0.76/*
/command/*
/usr/share/doc/daemontools-0.76/*
/service
/var/service
/etc/init/svscan.conf
