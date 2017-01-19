Name: tendrl-node-monitoring
Version: 1.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Module for Tendrl Performance Monitoring
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/performance-monitoring/tree/master/node_monitoring

BuildRequires: pytest
BuildRequires: systemd
BuildRequires: python-mock

Requires: ansible
Requires: collectd
Requires: collectd-ping
Requires: Jinja2
Requires: tendrl-commons

%description
Python module for Tendrl Node Monitoring

%prep
%setup

# Remove bundled egg-info
rm -rf %{name}.egg-info

%build
%{__python} setup.py build

# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install -m  0755  --directory $RPM_BUILD_ROOT%{_sysconfdir}/collectd_template
install -m  0755  --directory $RPM_BUILD_ROOT/usr/lib64/collectd
install -Dm 0655 tendrl/node_monitoring/commands/config_manager.py $RPM_BUILD_ROOT/usr/bin/config_manager
install -Dm 0655 tendrl/node_monitoring/templates/*.jinja $RPM_BUILD_ROOT%{_sysconfdir}/collectd_template/.
install -Dm 0655 tendrl/node_monitoring/plugins/* $RPM_BUILD_ROOT/usr/lib64/collectd/.

%files -f INSTALLED_FILES
%dir %{_sysconfdir}/collectd_template
%dir /usr/lib64/collectd/
%{_sysconfdir}/collectd_template/
/usr/lib64/collectd/
/usr/bin/config_manager

%changelog
* Thu Jan 19 2017 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 1.1-1
- Initial build.
