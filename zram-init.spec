Summary:	A wrapper script for the zram linux kernel module 
Name:		zram-init
Version:	9.1
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/vaeth/zram-init/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	518607108ddb54f2c4e35b9fc875c450
URL:		https://github.com/vaeth/zram-init/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a small helper script to setup a zram device as swap or as a
ramdisk.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env sh,%{__sh},' sbin/zram-init

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/modprobe.d
install -d $RPM_BUILD_ROOT/sbin
install -d $RPM_BUILD_ROOT%{systemdunitdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man8
install modprobe.d/zram.conf $RPM_BUILD_ROOT/etc/modprobe.d/zram-init.conf
install sbin/zram-init $RPM_BUILD_ROOT/sbin/
install systemd/system/* $RPM_BUILD_ROOT%{systemdunitdir}
install man/zram-init.8 $RPM_BUILD_ROOT%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) /sbin/zram-init
/etc/modprobe.d/zram-init.conf
%{systemdunitdir}/zram_btrfs.service
%{systemdunitdir}/zram_swap.service
%{systemdunitdir}/zram_tmp.service
%{systemdunitdir}/zram_var_tmp.service
%{_mandir}/man8/zram-init.8*
