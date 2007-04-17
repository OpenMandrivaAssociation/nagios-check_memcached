%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	MemCached health check for Nagios
Name:		nagios-check_memcached
Version:	1.1
Release:	%mkrel 2
License:	BSD
Group:		Networking/Other
URL:		http://zilbo.com/
Source0:	http://zilbo.com/plugins/check_memcached
Source1:	check_memcached.cfg
Requires:	nagios
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
A plugin for nagios to check if memcached is up and running.

%prep

%setup -q -c -T

cp %{SOURCE0} check_memcached
cp %{SOURCE1} check_memcached.cfg

perl -pi -e "s|/opt|%{_libdir}|g" check_memcached
perl -pi -e "s|_LIBDIR_|%{_libdir}|g" *.cfg

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 check_memcached %{buildroot}%{_libdir}/nagios/plugins/
install -m0644 *.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/

%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_memcached.cfg
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_memcached
