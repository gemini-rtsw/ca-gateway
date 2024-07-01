%define _prefix /gem_base/epics/ioc
%define name ca-gateway
%define repository gemdev
%define debug_package %{nil}
%define arch %(uname -m)
%define checkout %(git log --pretty=format:'%h' -n 1) 


# These defines need to be adjusted to point to the git ref
# that is to be built

# vendor/upstream git project
%define vendor_project https://github.com/epics-extensions/ca-gateway.git
# vendor git ref (tag or commit hash). Please keep in sync with 'Version' below!
%define vendor_ref 6749981

#These global defines are added to prevent stripping
# symbols on vxWorks cross-compiled code
# Getting 'strip' to work is probably only needed for
# building a related debug sub-package
#
# But this prevents all the strip warnings
# mrippa 20120202
%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Summary: %{name} Package, a module for EPICS base
Name: %{name}
Version: 2.1.3.6749981
Release: 0%{?dist}
License: EPICS Open License
Group: Applications/Engineering
Source0: %{name}-%{version}.tar.gz
ExclusiveArch: %{arch}
Prefix: %{_prefix}
## You may specify dependencies here
BuildRequires: epics-base-devel re2c gemini-ade psmisc pcas-devel
Requires: epics-base pcas
## Switch dependency checking off
# AutoReqProv: no

%description
This is the module %{name}.

## If you want to have a devel-package to be generated uncomment the following:
%package devel
Summary: %{name}-devel Package
Group: Development/Gemini
Requires: %{name}
%description devel
This is the module %{name}.

%package doc
Summary: %{name}-doc Package
Group: Development/Gemini
Requires: %{name}
%description doc
This is the module %{name} containing the documentation.

%prep
%setup -q 

%build
# get vendor code
git clone %{vendor_project} vendor_project
cd vendor_project

# apply Gemini-specific configuration
cp ../configure/RELEASE configure/

# install 
make distclean uninstall
make

%install
# cd into the directory containing the vendor sources
cd vendor_project

export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r bin $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -p ../scripts/linux-x86_64/ca-gateway.sh $RPM_BUILD_ROOT/%{_prefix}/%{name}/bin/linux-x86_64/
cp -p ../scripts/linux-x86_64/ca-gateway-TCS.sh $RPM_BUILD_ROOT/%{_prefix}/%{name}/bin/linux-x86_64/
cp -r ../etc $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r lib $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r docs $RPM_BUILD_ROOT/%{_prefix}/%{name}
find $RPM_BUILD_ROOT/%{_prefix}/%{name} -name ".git" -exec rm -rf {} \;

%post
if [ ! -d /var/log/ca-gateway ]; then
    mkdir -p /var/log/ca-gateway
fi

source /etc/profile
# if upgrading, remove old systemd related files
if [ "$1" == "2" ]; then
	manage-procs remove -f %{name}
    
    # delete file copied in during installation
    rm -f /etc/systemd/system/procserv-%{name}.service
    rm -f /etc/systemd/system/procserv-%{name}-TCS.service

	manage-procs write-procs-cf
fi
# install systemd files
manage-procs add -f -C %{_prefix}/%{name}/bin/linux-x86_64 -e LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{_prefix}/%{name}/lib/linux-x86_64  -Uroot -Groot %{name} ca-gateway.sh
manage-procs add -f -C %{_prefix}/%{name}/bin/linux-x86_64 -e LD_LIBRARY_PATH=$LD_LIBRARY_PATH:%{_prefix}/%{name}/lib/linux-x86_64  -Uroot -Groot %{name} ca-gateway-TCS.sh

if [ ! -d /etc/conserver ]; then mkdir /etc/conserver ; fi; manage-procs write-procs-cf

systemctl daemon-reload

# disable autostarting of service at boot / container start
systemctl disable procserv-%{name}.service
systemctl disable procserv-%{name}-TCS.service
# copy the unit file from the unknown dir to the system's one
cp -f /etc/procServ.d/procserv-%{name}.service /etc/systemd/system/
cp -f /etc/procServ.d/procserv-%{name}-TCS.service /etc/systemd/system/

systemctl daemon-reload

systemctl restart conserver

%postun
if [ "$1" = "0" ]; then
	manage-procs remove -f %{name}
        
    # delete file copied in during installation
    rm -f /etc/systemd/system/procserv-%{name}.service
    rm -f /etc/systemd/system/procserv-%{name}-TCS.service
    
	manage-procs write-procs-cf
	rm -rf %{_prefix}/%{name}
	systemctl daemon-reload
	systemctl restart conserver
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
   /%{_prefix}/%{name}/bin
%config(noreplace)   /%{_prefix}/%{name}/etc/tcs-ip.conf

%files devel
%defattr(-,root,root)
   /%{_prefix}/%{name}/lib

%files doc
%defattr(-,root,root)
   /%{_prefix}/%{name}/docs

%changelog

