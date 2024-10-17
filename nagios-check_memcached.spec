%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	MemCached health check for Nagios
Name:		nagios-check_memcached
Version:	1.1
Release:	8
License:	BSD
Group:		Networking/Other
URL:		https://zilbo.com/
Source0:	http://zilbo.com/plugins/check_memcached
Requires:	nagios
BuildArch:	noarch
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
EOF

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


%changelog
* Wed Nov 17 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1-7mdv2011.0
+ Revision: 598413
- duh!

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.1-6mdv2010.0
+ Revision: 440202
- rebuild

* Mon Dec 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.1-5mdv2009.1
+ Revision: 314637
- now a noarch package
- use a herein document for configuration
- reply on filetrigger for reloading nagios

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-4mdv2009.0
+ Revision: 239081
- rebuild

* Sun Jul 20 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-3mdv2009.0
+ Revision: 239079
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.1-2mdv2008.0
+ Revision: 13793
- use the new /etc/nagios/plugins.d scandir


* Wed Nov 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1-1mdv2007.0
+ Revision: 84573
- Import nagios-check_memcached

* Thu Aug 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1-1mdk
- initial Mandriva package

