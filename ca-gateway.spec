%define _prefix /gem_base/epics/support
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
cp -r lib $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r docs $RPM_BUILD_ROOT/%{_prefix}/%{name}
cp -r scripts $RPM_BUILD_ROOT/%{_prefix}/%{name}
find $RPM_BUILD_ROOT/%{_prefix}/%{name} -name ".git" -exec rm -rf {} \;

%postun
if [ "$1" = "0" ]; then
    rm -rf %{_prefix}/%{name}
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
   /%{_prefix}/%{name}/bin
   /%{_prefix}/%{name}/lib
   /%{_prefix}/%{name}/docs
   /%{_prefix}/%{name}/scripts

%files devel
%defattr(-,root,root)
   /%{_prefix}/%{name}/bin
   /%{_prefix}/%{name}/lib
   /%{_prefix}/%{name}/docs
   /%{_prefix}/%{name}/scripts

%changelog

