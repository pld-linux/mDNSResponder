
Summary:	-
Summary(pl):	-
Name:		mDNSResponder
Version:	98
Release:	0.1
License:	- (enter GPL/GPL v2/LGPL/BSD/BSD-like/other license name here)
Vendor:		-
Group:		-
Source0:	http://helios.et.put.poznan.pl/~jstachow/pub/%{name}-%{version}.tar.gz
# Source0-md5:	26ddb6f2ed2c451704d26e80da5fdcb9
URL:		-
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%prep
%setup -q

%build

cd mDNSPosix

%{__make} os=linux

cd -

%install

install -d \
	$RPM_BUILD_ROOT{%{_includedir},/etc/rc.d/init.d,%{_sbindir}} \
	$RPM_BUILD_ROOT{/%{_lib},%{_libdir},%{_mandir}/man{5,8}}

cd mDNSPosix

install ../mDNSShared/dns_sd.h $RPM_BUILD_ROOT%{_includedir}/dns_sd.h
install mdnsd.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/mdns
install nss_mdns.conf $RPM_BUILD_ROOT/etc/nss_mdns.conf
install build/prod/mdnsd $RPM_BUILD_ROOT%{_sbindir}/mdnsd
install build/prod/libnss_mdns-0.2.so $RPM_BUILD_ROOT/%{_lib}/libnss_mdns-0.2.so
cd $RPM_BUILD_ROOT/%{_lib}
ln -s -f libbnss_mdns-0.2.so libnss_mdns.so.2
cd -
install build/prod/libdns_sd.so $RPM_BUILD_ROOT%{_libdir}/libdns_sd.so.1
cd $RPM_BUILD_ROOT%{_libdir}
ln -s -f libdns_sd.so.1 libdns_sd.so
cd -
install nss_mdns.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/nss_mdns.conf.5
install libnss_mdns.8 $RPM_BUILD_ROOT%{_mandir}/man8/libnss_mdns.8
install ../mDNSShared/mDNSResponder.8 $RPM_BUILD_ROOT%{_mandir}/man8/mdnsd.8

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.txt
%{_includedir}/dns_sd.h
%attr(0754,root,root) /etc/rc.d/init.d/mdns
%config(noreplace) %verify(not size mtime md5) /etc/nss_mdns.conf
%attr(0755,root,root) %{_sbindir}/mdnsd
/%{_lib}/libnss_mdns.so.2
%attr(0755,root,root) /%{_lib}/libnss_mdns-0.2.so
%{_libdir}/libdns_sd.so
%attr(0755,root,root) %{_libdir}/libdns_sd.so.1
%{_mandir}/man5/nss_mdns.conf.*
%{_mandir}/man8/mdnsd.*
%{_mandir}/man8/libnss_mdns.*
