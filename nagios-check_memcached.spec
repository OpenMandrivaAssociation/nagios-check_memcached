%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	MemCached health check for Nagios
Name:		nagios-check_memcached
Version:	1.1
Release:	%mkrel 6
License:	BSD
Group:		Networking/Other
URL:		http://zilbo.com/
Source0:	http://zilbo.com/plugins/check_memcached
Source1:	check_memcached.cfg
Requires:	nagios
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
A plugin for nagios to check if memcached is up and running.

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/nagios/plugins
install -m 755 %{SOURCE0} %{buildroot}%{_datadir}/nagios/plugins/

perl -pi -e 's|/opt|%{_datadir}|' \
    %{buildroot}%{_datadir}/nagios/plugins/check_memcached

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_memcached.cfg <<'EOF'
define command {
	command_name    check_memcached
	command_line    %{_datadir}/nagios/plugins/check_memcached -H $HOSTADDRESS$ -p $ARG1$ -k $ARG2$ -t $ARG3$
}

%if %mdkversion < 200900
%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_memcached.cfg
%{_datadir}/nagios/plugins/check_memcached
