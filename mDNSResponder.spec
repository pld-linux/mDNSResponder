
Summary:	Rendezvous on linux
#Summary(pl):	We need to extend those summaries
Name:		mDNSResponder
Version:	98
Release:	1
License:	APSL
Group:		Applications
Source0:	http://helios.et.put.poznan.pl/~jstachow/pub/%{name}-%{version}.tar.gz
# Source0-md5:	26ddb6f2ed2c451704d26e80da5fdcb9
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-llh.patch
URL:		http://developer.apple.com/darwin/projects/rendezvous
Provides:	libdns_sd.so
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rendezvous is a revolutionary networking technology that lets you
create an instant network of computers and devices without any
configuration. It allows the services and capabilities of each device
to be registered on the network, and allows these services to be
dynamically discoverable by other devices on the network. Rendezvous
enables this seamless networking and service discovery over the
standard and ubiquitous IP networking protocol.

%description -l pl
Rendezvous to technologia konfiguracji sieci oparta o otwarty standard
zwany Zeroconf. Pozwala ona komputerom oraz kompatybilnym urz±dzeniom
na automatyczne odnalezienie i skonfigurowanie siê w sieci lokalnej
oraz komunikacjê, bez pomocy administratora oraz us³ug typu DHCP czy
DNS (st±d te¿ pojawia siê okre¶lenie 'zero-configuration').

%package devel
Summary:	Header files and develpment documentation for mDNSResponder
Summary(pl):	Pliki nag³ówkowe i dokumetacja do mDNSResponder
Group:		Development/Libraries

%description devel
Header files and develpment documentation for mDNSResponder.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
cd mDNSPosix

%{__make} os=linux \
	CC="%{__cc}" \
	LD="%{__ld} -shared" \
	JDK="%{_libdir}/java" \
	%{?debug:DEBUG=1} \
	HAVE_IPV6=1 \
	CFLAGS_DEBUG="%{?debug:%{debugcflags} -DMDNS_DEBUGMSGS=1} %{!?debug:%{rpmcflags}} -DMDNS_DEBUGMSGS=0" \
	CFLAGS_USER="%{rpmcflags}" \
	STRIP="echo"
cd -

%install

rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_includedir},/etc/rc.d/init.d,%{_sbindir}} \
	$RPM_BUILD_ROOT{/%{_lib},%{_libdir},%{_mandir}/man{5,8}}

cd mDNSPosix

install ../mDNSShared/dns_sd.h $RPM_BUILD_ROOT%{_includedir}/dns_sd.h
install mdnsd.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/mdns
install nss_mdns.conf $RPM_BUILD_ROOT%{_sysconfdir}/nss_mdns.conf
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
%attr(754,root,root) /etc/rc.d/init.d/mdns
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nss_mdns.conf
%attr(755,root,root) %{_sbindir}/mdnsd
/%{_lib}/libnss_mdns.so.2
%attr(755,root,root) /%{_lib}/libnss_mdns-0.2.so
%attr(755,root,root) %{_libdir}/libdns_sd.so
%attr(755,root,root) %{_libdir}/libdns_sd.so.1
%{_mandir}/man5/nss_mdns.conf.*
%{_mandir}/man8/mdnsd.*
%{_mandir}/man8/libnss_mdns.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
