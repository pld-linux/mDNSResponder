# TODO: We need to extend those summaries
Summary:	Rendezvous on Linux
Summary(pl):	Rendezvous pod Linuksem
Name:		mDNSResponder
Version:	98
Release:	1
License:	APSL
Group:		Applications
Source0:	http://helios.et.put.poznan.pl/~jstachow/pub/%{name}-%{version}.tar.gz
# Source0-md5:	26ddb6f2ed2c451704d26e80da5fdcb9
Patch0:		%{name}-cflags.patch
Patch1:		%{name}-llh.patch
Patch2:		%{name}-soname.patch
URL:		http://developer.apple.com/darwin/projects/rendezvous/
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
Summary:	Header files for mDNSResponder
Summary(pl):	Pliki nag³ówkowe do mDNSRespondera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for mDNSResponder.

%description devel -l pl
Pliki nag³ówkowe dla mDNSRespondera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__make} -C mDNSPosix os=linux \
	CC="%{__cc}" \
	JDK="%{_libdir}/java" \
	%{?debug:DEBUG=1} \
	HAVE_IPV6=1 \
	CFLAGS_DEBUG="%{rpmcflags} -DMDNS_DEBUGMSGS=%{?debug:1}%{!?debug:0}" \
	CFLAGS_USER="%{rpmcflags}" \
	STRIP="echo"

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_includedir},/etc/rc.d/init.d,%{_sbindir}} \
	$RPM_BUILD_ROOT{/%{_lib},%{_libdir},%{_mandir}/man{5,8}}

install mDNSShared/dns_sd.h $RPM_BUILD_ROOT%{_includedir}/dns_sd.h
install mDNSPosix/mdnsd.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/mdns
install mDNSPosix/nss_mdns.conf $RPM_BUILD_ROOT%{_sysconfdir}/nss_mdns.conf
install mDNSPosix/build/prod/mdnsd $RPM_BUILD_ROOT%{_sbindir}/mdnsd
install mDNSPosix/build/prod/libnss_mdns-0.2.so $RPM_BUILD_ROOT/%{_lib}/libnss_mdns-0.2.so
install mDNSPosix/build/prod/libdns_sd.so $RPM_BUILD_ROOT%{_libdir}/libdns_sd.so.1
ln -sf libdns_sd.so.1 $RPM_BUILD_ROOT%{_libdir}/libdns_sd.so
install mDNSPosix/nss_mdns.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/nss_mdns.conf.5
install mDNSPosix/libnss_mdns.8 $RPM_BUILD_ROOT%{_mandir}/man8/libnss_mdns.8
install mDNSShared/mDNSResponder.8 $RPM_BUILD_ROOT%{_mandir}/man8/mdnsd.8

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
%attr(755,root,root) /%{_lib}/libnss_mdns-0.2.so
%attr(755,root,root) %{_libdir}/libdns_sd.so.1
%{_mandir}/man5/nss_mdns.conf.5*
%{_mandir}/man8/mdnsd.8*
%{_mandir}/man8/libnss_mdns.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdns_sd.so
%{_includedir}/*.h
