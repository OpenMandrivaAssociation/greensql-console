%define _requires_exceptions pear(/usr/share/smarty/Smarty.class.php)

%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	Manages a GreenSQL Database Firewall
Name:		greensql-console
Version:	0.5.0
Release:	%mkrel 3
License:	GPLv2
Group:		System/Servers
URL:		http://www.greensql.net/
Source0:	http://www.greensql.net/public/releases/%{name}-%{version}.tar.gz
Patch0:		greensql-console-mdv_conf.diff
Requires(post): rpm-helper
Requires(postun): rpm-helper
Requires:	apache-mod_php php-mysql
Requires:	php-smarty >= 2.3.0
BuildRequires:	apache-base >= 2.0.54
Suggests:	greensql-fw
Suggests:	mysql
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The greensql-console package is web management tool used to manage GreenSQL
Database Firewall.

%prep

%setup -q -n green-%{version}
%patch0 -p1

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}
install -d %{buildroot}/var/lib/%{name}/smarty/templates_c

cp -aRf * %{buildroot}/var/www/%{name}/

mv %{buildroot}/var/www/%{name}/config.php %{buildroot}%{_sysconfdir}/%{name}/config.php

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    Order Deny,Allow
    Deny from All
    Allow from 127.0.0.1
    ErrorDocument 403 "Access denied per %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf"
</Directory>
EOF

# cleanup
rm -rf %{buildroot}/var/www/%{name}/configs
rm -rf %{buildroot}/var/www/%{name}/libs
#rm -rf %{buildroot}/var/www/%{name}/templates
rm -rf %{buildroot}/var/www/%{name}/templates_c

%post
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc license.txt readme.txt
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0700,apache,apache) %dir %{_sysconfdir}/%{name}
%attr(0640,apache,apache) %config(noreplace) %{_sysconfdir}/%{name}/config.php
/var/www/%{name}
%attr(0700,apache,apache) %dir /var/lib/%{name}
%attr(0700,apache,apache) %dir /var/lib/%{name}/smarty
%attr(0700,apache,apache) %dir /var/lib/%{name}/smarty/templates_c
