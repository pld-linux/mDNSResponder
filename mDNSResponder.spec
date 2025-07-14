Summary:	Rendezvous - DNS Service Discovery
Summary(pl.UTF-8):	Rendezvous - wykrywanie usług w oparciu o DNS
Name:		mDNSResponder
Version:	878.200.35
Release:	1
License:	Apache v2.0
Group:		Networking/Daemons
Source0:	https://opensource.apple.com/tarballs/mDNSResponder/%{name}-%{version}.tar.gz
# Source0-md5:	e773f290a7d29f1072247985d6add2ff
Source1:	mDNSResponder.init
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-soname.patch
Patch3:		%{name}-spell.patch
Patch4:		%{name}-bison.patch
URL:		https://developer.apple.com/bonjour/
BuildRequires:	bison
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rendezvous is a revolutionary networking technology that lets you
create an instant network of computers and devices without any
configuration. It allows the services and capabilities of each device
to be registered on the network, and allows these services to be
dynamically discoverable by other devices on the network. Rendezvous
enables this seamless networking and service discovery over the
standard and ubiquitous IP networking protocol.

%description -l pl.UTF-8
Rendezvous to technologia konfiguracji sieci oparta o otwarty standard
zwany Zeroconf. Pozwala ona komputerom oraz kompatybilnym urządzeniom
na automatyczne odnalezienie i skonfigurowanie się w sieci lokalnej
oraz komunikację, bez pomocy administratora oraz usług typu DHCP czy
DNS (stąd też pojawia się określenie 'zero-configuration').

%package libs
Summary:	mDNSResponder library
Summary(pl.UTF-8):	Biblioteka mDNSRespondera
Group:		Libraries
Provides:	mdns-bonjour
Obsoletes:	avahi-compat-libdns_sd
Conflicts:	mDNSResponder < 107-2

%description libs
mDNSResponder library.

%description libs -l pl.UTF-8
Biblioteka mDNSRespondera.

%package devel
Summary:	Header files for mDNSResponder
Summary(pl.UTF-8):	Pliki nagłówkowe do mDNSRespondera
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Provides:	mdns-bonjour-devel
Obsoletes:	avahi-compat-libdns_sd-devel

%description devel
Header files for mDNSResponder.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla mDNSRespondera.

%package tools
Summary:	Tools for mDNSResponder
Summary(pl.UTF-8):	Narzędzia do mDNSRespondera
Group:		Networking/Utilities
Requires:	%{name}-libs = %{version}-%{release}

%description tools
Tools for mDNSResponder.

%description tools -l pl.UTF-8
Narzędzia dla mDNSRespondera.

%package -n nss_mdns
Summary:	mDNSResponder NSS module
Summary(pl.UTF-8):	Moduł NSS korzystający z mDNSRespondera
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description -n nss_mdns
mDNSResponder NSS module.

%description -n nss_mdns -l pl.UTF-8
Moduł NSS korzystający z mDNSRespondera.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1
%patch -P4 -p1

%build
%{__make} -C mDNSPosix -j1 \
	os=linux \
	CC="%{__cc}" \
	CFLAGS_DEBUG="%{rpmcflags} -DMDNS_DEBUGMSGS=%{?debug:1}%{!?debug:0}" \
	CFLAGS_USER="%{rpmcflags}" \
	%{?debug:DEBUG=1} \
	HAVE_IPV6=1 \
	JDK="%{_libdir}/java" \
	OPTIONALTARG="dnsextd nss_mdns" \
	STRIP="echo"

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_includedir},/etc/rc.d/init.d,%{_sbindir}} \
	$RPM_BUILD_ROOT{/%{_lib},%{_libdir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT%{_bindir}

install mDNSShared/dns_sd.h $RPM_BUILD_ROOT%{_includedir}/dns_sd.h
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/mdns
install mDNSPosix/nss_mdns.conf $RPM_BUILD_ROOT%{_sysconfdir}/nss_mdns.conf
install mDNSPosix/build/prod/mdnsd $RPM_BUILD_ROOT%{_sbindir}/mdnsd
install mDNSPosix/build/prod/dnsextd $RPM_BUILD_ROOT%{_sbindir}/dnsextd
install mDNSPosix/build/prod/mDNS* $RPM_BUILD_ROOT%{_bindir}
install mDNSPosix/build/prod/libnss_mdns-0.2.so $RPM_BUILD_ROOT/%{_lib}/libnss_mdns-0.2.so
install mDNSPosix/build/prod/libdns_sd.so $RPM_BUILD_ROOT%{_libdir}/libdns_sd.so.1.0.0
ln -sf libdns_sd.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}/libdns_sd.so
install mDNSPosix/nss_mdns.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/nss_mdns.conf.5
install mDNSPosix/libnss_mdns.8 $RPM_BUILD_ROOT%{_mandir}/man8/libnss_mdns.8
install mDNSShared/mDNSResponder.8 $RPM_BUILD_ROOT%{_mandir}/man8/mdnsd.8
install mDNSShared/dnsextd.8 $RPM_BUILD_ROOT%{_mandir}/man8/dnsextd.8

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add mdns
%service mdns restart

%preun
if [ "$1" = "0" ]; then
	%service mdns stop
	/sbin/chkconfig --del mdns
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n nss_mdns -p /sbin/ldconfig
%postun	-n nss_mdns -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/mdns
%attr(755,root,root) %{_sbindir}/mdnsd
%attr(755,root,root) %{_sbindir}/dnsextd
%{_mandir}/man8/mdnsd.8*
%{_mandir}/man8/dnsextd.8*

%files libs
%defattr(644,root,root,755)
%doc LICENSE PrivateDNS.txt README.txt
%attr(755,root,root) %{_libdir}/libdns_sd.so.1.0.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdns_sd.so
%{_includedir}/dns_sd.h

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mDNSClientPosix
%attr(755,root,root) %{_bindir}/mDNSIdentify
%attr(755,root,root) %{_bindir}/mDNSNetMonitor
%attr(755,root,root) %{_bindir}/mDNSProxyResponderPosix
%attr(755,root,root) %{_bindir}/mDNSResponderPosix

%files -n nss_mdns
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nss_mdns.conf
%attr(755,root,root) /%{_lib}/libnss_mdns-0.2.so
%{_mandir}/man5/nss_mdns.conf.5*
%{_mandir}/man8/libnss_mdns.8*
