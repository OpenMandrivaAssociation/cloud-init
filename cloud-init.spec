%undefine _debugsource_packages
# Unfortunately tests fail inside of abf because
# they try to open sockets.
# Run the tests before throwing the package at
# abf though...
%bcond_with tests

Summary:	Cloud instance initialization tool
Name:		cloud-init
Version:	25.3
Release:	1
Source0:	https://github.com/canonical/cloud-init/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	https://src.fedoraproject.org/rpms/cloud-init/raw/rawhide/f/cloud-init-tmpfiles.conf
License:	Dual GPLv3/Apache 2.0
BuildSystem:	meson
BuildRequires:	python
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(libnm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	python%{pyver}dist(pyyaml)
BuildRequires:	python%{pyver}dist(requests)
BuildRequires:	python%{pyver}dist(configobj)
BuildRequires:	python%{pyver}dist(jinja2)
BuildRequires:	python%{pyver}dist(jsonschema)
BuildRequires:	python%{pyver}dist(nose)
BuildRequires:	python%{pyver}dist(pyserial)
BuildRequires:	python%{pyver}dist(six)
BuildRequires:	python%{pyver}dist(distro)
BuildRequires:	python%{pyver}dist(jsonpatch)
BuildRequires:	python%{pyver}dist(oauthlib)
BuildRequires:	python%{pyver}dist(pyserial)
BuildRequires:	python%{pyver}dist(netifaces)
%if %{with tests}
BuildRequires:	python%{pyver}dist(httpretty)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-mock)
BuildRequires:	python%{pyver}dist(responses)
%endif
# Yes, even when using NetworkManager.
# dhcp-client is used to locate the server
# containing the config.
Requires:	(dhcpcd or dhcp-client or udhcpc)
Requires:	hostname
Requires:	e2fsprogs
Requires:	iproute
Requires:	net-tools
Requires:	procps
Requires:	shadow
Requires:	util-linux
Requires:	xfsprogs
Requires:	gptfdisk
Requires:	openssl
Requires:	growpart
# Apparently missed by the dependency generator:
Requires:	python%{pyver}dist(distro)
Requires:	python%{pyver}dist(pyserial)
BuildArch:	noarch

%description
Cloud instance initialization tool.

%patchlist
cloud-init-CloudStack-fix-getting-data-server.patch

%prep -a
# Use unittest from the standard library. unittest2 is old and being
# retired in modern distros.
find tests/ -type f | xargs sed -i s/unittest2/unittest/
find tests/ -type f | xargs sed -i s/assertItemsEqual/assertCountEqual/

%install -a
mkdir -p %{buildroot}/run/cloud-init %{buildroot}%{_tmpfilesdir}
install -c -m 644 %{S:1} %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}%{_mandir}/man1
cp doc/man/cloud-{id,init,init-per}.1 %{buildroot}%{_mandir}/man1/

%if 1
# Let's debug this for now...
sed -i -e 's,/usr/bin/cloud-init,/usr/bin/cloud-init --debug,g' %{buildroot}%{_unitdir}/*.service
%endif

%if %{with tests}
%check
python -m pytest tests/unittests
%endif

%files
%{_bindir}/*
%{_prefix}/lib/python*/site-packages/cloudinit
#%{_prefix}/lib/python*/site-packages/cloud_init*.egg-info
%{_systemdgeneratordir}/cloud-init-generator
%{_unitdir}/cloud*.target
%{_unitdir}/cloud*.service
%{_unitdir}/cloud-init-hotplugd.socket
#dir %{_unitdir}/sshd-keygen@.service.d
#{_unitdir}/sshd-keygen@.service.d/disable-sshd-keygen-if-cloud-init-active.conf
%{_datadir}/bash-completion/completions/*
%{_sysconfdir}/cloud
%{_libexecdir}/cloud-init
%doc %{_docdir}/cloud-init
%{_udevrulesdir}/*.rules
%doc %{_mandir}/man1/*.1*
%{_tmpfilesdir}/%{name}.conf
