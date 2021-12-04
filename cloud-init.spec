%define debug_package %{nil}

Summary:	Cloud instance initialization tool
Name:		cloud-init
Version:	21.4
Release:	3
Source0:	https://github.com/canonical/cloud-init/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:		cloud-init-21.4-openmandriva.patch
License:	Dual GPLv3/Apache 2.0
BuildRequires:	python
BuildRequires:	python3dist(setuptools)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(libnm)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	python3dist(pyyaml)
BuildRequires:	python3dist(requests)
BuildRequires:	python3dist(configobj)
BuildRequires:	python3dist(jinja2)
BuildRequires:	python3dist(jsonschema)
BuildRequires:	python3dist(nose)
BuildRequires:	python3dist(pyserial)
BuildRequires:	python3dist(six)
BuildRequires:	python-distro

%description
Cloud instance initialization tool

%prep
%autosetup -p1

%build
python setup.py build

%install
python setup.py install --root=%{buildroot} --prefix=%{_prefix}

%files
%{_bindir}/*
%{_prefix}/lib/python*/site-packages/cloudinit
%{_prefix}/lib/python*/site-packages/cloud_init*.egg-info
/lib/systemd/system-generators/cloud-init-generator
/lib/systemd/system/cloud*.target
/lib/systemd/system/cloud*.service
/etc/systemd/system/sshd-keygen@.service.d
/lib/systemd/system/cloud-init-hotplugd.socket
%{_datadir}/bash-completion/completions/*
%{_sysconfdir}/cloud
%{_sysconfdir}/NetworkManager/dispatcher.d/hook-network-manager
%{_sysconfdir}/dhcp/dhclient-exit-hooks.d/hook-dhclient
%{_libexecdir}/cloud-init
%doc %{_docdir}/cloud-init
/lib/udev/rules.d/66-azure-ephemeral.rules
