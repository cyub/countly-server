Name:       countly
Version:    16.12.2
Release:    2%{?dist}

License:    Modified AGPLv3
Group:	    Applications/Internet
URL:        https://github.com/countly/countly-server
Vendor:     Countly
Source0:    countly.tar.gz
Source1:    countly.init
Packager:   Sergey Alembekov (sa@count.ly)
Summary:    Countly mobile, web and desktop analytics & marketing platform.

Requires:   nodejs >= 6
Requires(post): /sbin/chkconfig, /usr/sbin/useradd
Requires(preun): /sbin/chkconfig, /sbin/service
Requires(postun): /sbin/service
Provides: countly
#BuildRequires:  nodejs

#%if 0%{?fedora} >= 19
#ExclusiveArch: %{nodejs_arches}
#%else
ExclusiveArch: %{ix86} x86_64 %{arm}
#%endif

%description
Countly is an open source, enterprise-grade mobile analytics platform.
It has analytics, marketing, crash & error reporting (web+mobile) and
other features. Countly collects data from mobile phones, tablets,
Apple Watch and other internet-connected devices, and visualizes this
information to analyze mobile application usage and end-user behavior.
This package includes complete Countly Community Edition.

%prep
%setup -q -c countly

%build
export CXXFLAGS="%{optflags}"
cp frontend/express/public/javascripts/countly/countly.config.sample.js frontend/express/public/javascripts/countly/countly.config.js
cp api/config.sample.js api/config.js
cp frontend/express/config.sample.js frontend/express/config.js
cp plugins/plugins.default.json plugins/plugins.json
source /opt/rh/devtoolset-2/enable
npm install
pushd plugins/push/api/parts/apn
/usr/lib/node_modules/npm/bin/node-gyp-bin/node-gyp rebuild
popd
node bin/scripts/install_plugins
node_modules/grunt-cli/bin/grunt dist-all

%install
mkdir -p %{buildroot}/opt/countly
cp -r * %{buildroot}/opt/countly/
mkdir -p %{buildroot}%{_initddir}
cp %{SOURCE1} %{buildroot}%{_initddir}/countly

%post
/sbin/chkconfig --add countly

%files
%attr(755, root, root) %{_initddir}/countly
/opt/countly
%config /opt/countly/frontend/express/config.js
%config /opt/countly/api/config.js
%config /opt/countly/frontend/express/public/javascripts/countly/countly.config.js
%config /opt/countly/plugins/plugins.json

%changelog
* Mon Feb 13 2017 Sergey Alembekov <rt@aspirinka.net> - 16.12.2-2
- cosmetic fixes

* Fri Jan 20 2017 Sergey Alembekov <rt@aspirinka.net> - 16.12.2
- new release

* Tue Jan 17 2017 Sergey Alembekov <rt@aspirinka.net> - 16.12.1
- initial build