Name: tendrl-performance-monitoring
Version: 1.1
Release: 1%{?dist}
BuildArch: noarch
Summary: Module for Tendrl Performance Monitoring
Source0: %{name}-%{version}.tar.gz
License: LGPLv2+
URL: https://github.com/Tendrl/performance-monitoring

BuildRequires: python-gevent
BuildRequires: pytest
BuildRequires: systemd
BuildRequires: python-mock
#BuildRequires: python-etcd
BuildRequires: python-six
BuildRequires: python-urllib3

Requires: Flask-API
Requires: graphite-web
Requires: msgpack-python
Requires: python-flask
Requires: python-etcd
Requires: python-carbon
Requires: python-six
Requires: python-urllib3
Requires: python-whisper
Requires: pytz
Requires: PyYAML
Requires: tendrl-commons

%description
Python module for Tendrl Performance Monitoring

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
install -m  0755  --directory $RPM_BUILD_ROOT%{_var}/log/tendrl/performance-monitoring
install -m  0755  --directory $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/performance-monitoring
install -Dm 0644 tendrl-performance-monitoring.service $RPM_BUILD_ROOT%{_unitdir}/tendrl-performance-monitoring.service
install -Dm 0644 etc/tendrl/monitoring_defaults.yaml $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/monitoring_defaults.yaml
install -Dm 0644 etc/logging.yaml.timedrotation.sample $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/performance-monitoring_logging.yaml
install -Dm 0644 etc/tendrl/tendrl.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/tendrl/performance-monitoring/performance-monitoring.conf.yaml

%post
%systemd_post tendrl-performance-monitoring.service

%preun
%systemd_preun tendrl-performance-monitoring.service

%postun
%systemd_postun_with_restart tendrl-performance-monitoring.service

%check
py.test -v tendrl/performance_monitoring/tests || :

%files -f INSTALLED_FILES
%dir %{_var}/log/tendrl/performance-monitoring
%dir %{_sysconfdir}/tendrl/performance-monitoring
%{_sysconfdir}/tendrl/monitoring_defaults.yaml
%{_sysconfdir}/tendrl/performance-monitoring/performance-monitoring.conf.yaml
%{_sysconfdir}/tendrl/performance-monitoring_logging.yaml
%doc README.rst
%license LICENSE
%{_unitdir}/tendrl-performance-monitoring.service

%changelog
* Wed Jan 18 2017 Timothy Asir Jeyasingh <tjeyasin@redhat.com> - 0.0.1-1
- Initial build.
