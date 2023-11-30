%undefine _debugsource_packages
# Unfortunately tests fail inside of abf because
# they try to open sockets.
# Run the tests before throwing the package at
# abf though...
%bcond_with tests

Summary:	Cloud instance initialization tool
Name:		cloud-init
Version:	23.3.3
Release:	1
Source0:	https://github.com/canonical/cloud-init/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	https://src.fedoraproject.org/rpms/cloud-init/raw/rawhide/f/cloud-init-tmpfiles.conf
License:	Dual GPLv3/Apache 2.0
BuildRequires:	python
BuildRequires:	python3dist(setuptools)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(libnm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-rpm-macros
BuildRequires:	python3dist(pyyaml)
BuildRequires:	python3dist(requests)
BuildRequires:	python3dist(configobj)
BuildRequires:	python3dist(jinja2)
BuildRequires:	python3dist(jsonschema)
BuildRequires:	python3dist(nose)
BuildRequires:	python3dist(pyserial)
BuildRequires:	python3dist(six)
BuildRequires:	python3dist(distro)
BuildRequires:	python3dist(jsonpatch)
BuildRequires:	python3dist(oauthlib)
BuildRequires:	python3dist(pyserial)
BuildRequires:	python3dist(netifaces)
%if %{with tests}
BuildRequires:	python3dist(httpretty)
BuildRequires:	python3dist(pytest)
BuildRequires:	python3dist(pytest-mock)
BuildRequires:	python3dist(responses)
%endif
# Yes, even when using NetworkManager.
# dhcp-client is used to locate the server
# containing the config.
Requires:	dhcp-client
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
Requires:	python3dist(distro)
Requires:	python3dist(pyserial)

%description
Cloud instance initialization tool.

%prep
%autosetup -p1

# Use unittest from the standard library. unittest2 is old and being
# retired in modern distros.
find tests/ -type f | xargs sed -i s/unittest2/unittest/
find tests/ -type f | xargs sed -i s/assertItemsEqual/assertCountEqual/

%build
python setup.py build

%install
python setup.py install --root=%{buildroot} --prefix=%{_prefix}

mkdir -p %{buildroot}/run/cloud-init %{buildroot}%{_tmpfilesdir}
install -c -m 644 %{S:1} %{buildroot}%{_tmpfilesdir}/%{name}.conf

mkdir -p %{buildroot}%{_mandir}/man1
cp doc/man/cloud-{id,init,init-per}.1 %{buildroot}%{_mandir}/man1/

%if 0
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
%{_prefix}/lib/python*/site-packages/cloud_init*.egg-info
%{_systemdgeneratordir}/cloud-init-generator
%{_unitdir}/cloud*.target
%{_unitdir}/cloud*.service
%{_sysconfdir}/systemd/system/sshd-keygen@.service.d
%{_unitdir}/cloud-init-hotplugd.socket
%{_datadir}/bash-completion/completions/*
%{_sysconfdir}/cloud
%{_libexecdir}/cloud-init
%doc %{_docdir}/cloud-init
%{_udevrulesdir}/*.rules
%doc %{_mandir}/man1/*.1*
%{_tmpfilesdir}/%{name}.conf
