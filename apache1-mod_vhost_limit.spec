%define		mod_name	vhost_limit
%define 	apxs		/usr/sbin/apxs1
Summary:	Apache module: vhost_limit limits
Summary(pl):	Modu� do apache: limity pasma dla serwer�w wirtualnych
Name:		apache1-mod_%{mod_name}
Version:	0.4
Release:	1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.nowhere-land.org/programs/mod_vhost_limit/mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	bae36a7174e184804b91356ef67d0b5d
URL:		http://www.nowhere-land.org/programs/mod_vhost_limit/
BuildRequires:	apache1-devel
Requires(post,preun):	%{apxs}
Requires(post,preun):	grep
Requires(preun):	fileutils
Requires:	apache1
Requires:	crondaemon
Requires:	procps
Obsoletes:	apache-mod_%{mod_name} <= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define         _sysconfdir     /etc/apache

%description
This is the module for Apache Web Server to restrict the number of
simultaneous connections per a virtual host.

%description -l pl
Ten pakiet zawiera modu� dla serwera WWW Apache s�u��cy do
ograniczania liczby jednoczesnych po��cze� dla serwer�w wirtualnych.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/apache ]; then
	/etc/rc.d/init.d/apache restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/apache ]; then
		/etc/rc.d/init.d/apache restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc */*html
%attr(755,root,root) %{_pkglibdir}/*
