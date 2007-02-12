%define		mod_name	vhost_limit
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: vhost_limit limits
Summary(pl.UTF-8):   Moduł do apache: limity pasma dla serwerów wirtualnych
Name:		apache1-mod_%{mod_name}
Version:	0.4
Release:	3
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.nowhere-land.org/programs/mod_vhost_limit/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	bae36a7174e184804b91356ef67d0b5d
URL:		http://www.nowhere-land.org/programs/mod_vhost_limit/
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Requires:	crondaemon
Requires:	procps
Obsoletes:	apache-mod_vhost_limit <= 0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is the module for Apache Web Server to restrict the number of
simultaneous connections per a virtual host.

%description -l pl.UTF-8
Ten pakiet zawiera moduł dla serwera WWW Apache służący do
ograniczania liczby jednoczesnych połączeń dla serwerów wirtualnych.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 0.4-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc */*html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
