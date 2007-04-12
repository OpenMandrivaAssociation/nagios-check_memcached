%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	MemCached health check for Nagios
Name:		nagios-check_memcached
Version:	1.1
Release:	%mkrel 1
License:	BSD
Group:		Networking/Other
URL:		http://zilbo.com/
Source0:	http://zilbo.com/plugins/check_memcached.bz2
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
A plugin for nagios to check if memcached is up and running.

%prep

%setup -q -c -T
bzcat %{SOURCE0} > check_memcached

perl -pi -e "s|/opt|%{_libdir}|g" check_memcached

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 check_memcached %{buildroot}%{_libdir}/nagios/plugins/

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_memcached


