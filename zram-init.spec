Summary:	A wrapper script for the zram linux kernel module
Name:		zram-init
Version:	13.3
Release:	2
License:	GPL v2
Group:		Applications
Source0:	https://github.com/vaeth/zram-init/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	957f391e485bc3327fafccc0b0e28fdb
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
URL:		https://github.com/vaeth/zram-init/
BuildRequires:	gettext-tools
BuildRequires:	rpmbuild(macros) >= 1.644
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units
Requires:	module-init-tools
Requires:	rc-scripts
Requires:	systemd-units
Requires:	util-linux
Suggests:	btrfs-progs
Suggests:	e2fsprogs
Suggests:	xfsprogs
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

%build
# the Makefile rewrites the shebang to whatever "command -v sh" finds
# MODIR_PLAIN is the locale path baked into the script; it defaults to
# $PREFIX/share/locale with PREFIX=/usr/local, so gettext would look in
# a directory the package never installs into
SHEBANG='#!%{__sh}' \
%{__make} \
	MODIR_PLAIN=%{_localedir}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

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

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%systemd_reload

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md
%attr(755,root,root) /sbin/zram-init
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/modprobe.d/zram.conf
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/%{name}.service
%{systemdunitdir}/zram_btrfs.service
%{systemdunitdir}/zram_swap.service
%{systemdunitdir}/zram_tmp.service
%{systemdunitdir}/zram_var_tmp.service
%{_mandir}/man8/zram-init.8*
%lang(de) %{_mandir}/de/man8/zram-init.8*

%files -n zsh-completion-zram-init
%defattr(644,root,root,755)
%{zsh_compdir}/_zram-init
