#
# Conditional build:
%bcond_without	tests		# build without tests

%define		rel		2
%define		gitrev	e2a8186
%define		php_name	php%{?php_suffix}
%define		modname	v8js
Summary:	V8 Javascript Engine for PHP
Name:		%{php_name}-pecl-%{modname}
Version:	0.1.5
Release:	%{rel}.%{gitrev}
License:	MIT
Group:		Development/Languages/PHP
Source0:	https://github.com/preillyme/v8js/archive/%{gitrev}/%{modname}-%{version}-%{gitrev}.tar.gz
# Source0-md5:	9faf1b76b2af2ab88102dc123a2a0bf1
URL:		http://pecl.php.net/package/v8js
BuildRequires:	%{php_name}-devel >= 4:5.3.3
BuildRequires:	rpmbuild(macros) >= 1.666
BuildRequires:	v8-devel >= 3.21.12
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension embeds the Google's V8 Javascript Engine into PHP.

%prep
%setup -qc
mv %{modname}-*/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README.md LICENSE CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
