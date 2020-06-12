Summary:	A wrapper script for the zram linux kernel module
Name:		zram-init
Version:	10.3
Release:	1
License:	GPL v2
Group:		Applications
Source0:	https://github.com/vaeth/zram-init/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	a455a4407394239b42f8fd2c0dc67b37
URL:		https://github.com/vaeth/zram-init/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a small helper script to setup a zram device as swap or as a
ramdisk.

%package -n zsh-completion-zram-init
Summary:	ZSH completion for zram-init command line
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh

%description -n zsh-completion-zram-init
ZSH completion for zram-init command line.

%prep
%setup -q

%{__sed} -i -e '1s,/usr/bin/env sh,%{__sh},' sbin/zram-init.in

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT/sbin \
	MODPROBED=TRUE \
	MODPROBEDIR=$RPM_BUILD_ROOT/etc/modprobe.d \
	MANPAGE=TRUE \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	GETTEXT=TRUE \
	MODIR=$RPM_BUILD_ROOT%{_localedir} \
	ZSH_COMPLETION=TRUE \
	COMP_ZSHDIR=$RPM_BUILD_ROOT%{zsh_compdir} \
	SYSTEMD=TRUE \
	SYSTEMDDIR=$RPM_BUILD_ROOT%{systemdunitdir} \
	OPENRC=FALSE

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_reload

%postun
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) /sbin/zram-init
/etc/modprobe.d/zram.conf
%{systemdunitdir}/zram_btrfs.service
%{systemdunitdir}/zram_swap.service
%{systemdunitdir}/zram_tmp.service
%{systemdunitdir}/zram_var_tmp.service
%{_mandir}/man8/zram-init.8*

%files -n zsh-completion-zram-init
%defattr(644,root,root,755)
%{zsh_compdir}/_zram-init
