# BEAM Cryptocurrency implementing Mimblewimble - full node and wallet
# Reference implementation
# vim:tw=0:ts=2:sw=2:et:
#
# This is the rpm source spec for building a Beam Reference Desktop (or
# commandline) Wallet, and Full Node.
#
# Consumer facing...
# * BeamWallet (desktop)
# * beam-wallet (cli)
# * beam-node
# * beam-miner-client
# * beam-wallet-api
# * beam-explorer-node
#
# Specialized (not always built)...
# * beam-debuginfo
#
# Note about edits within the spec: Any comments beginning with #t0dd are
# associated to future work or experimental elements of this spec file and
# build.
#
# DISCLAIMER:
# This RPM spec file is a work in progress (the dash references here and there
# are because this was originally templated from my dashcore RPM specfile)
#
# Enjoy. -t0dd

# Package (RPM) name-version-release.
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]

Name: beam
Summary: Peer-to-peer digital currency implementing mimblewimble, a next generation confidentiality protocol

%define targetIsProduction 0

# ARCHIVE QUALIFIER - edit this if applies
# ie. if the dev team includes things like rc3 in the filename
%define archiveQualifier rc1
%define includeArchiveQualifier 0

# VERSION - edit this
%define vermajor 1.0
%define verminor 3976
Version: %{vermajor}.%{verminor}

# RELEASE - edit this
# package release, and potentially extrarel
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.4
%endif

# MINORBUMP - edit this
# (for very small or rapid iterations)
%define minorbump taw

#
# Build the release string - don't edit this
#

%define snapinfo testing
%if %{includeArchiveQualifier}
  %define snapinfo %{archiveQualifier}
  %if %{targetIsProduction}
    %undefine snapinfo
  %endif
%endif

# pkgrel will be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%define includeMinorbump 1
%if ! %{includeMinorbump}
  %undefine minorbump
%endif
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# beam source tarball file basename
# the archive name and directory tree can have some variances
# v1.0.3976.tar.gz
%define _archivename_alt1 v%{version}
# beam-1.0.3976.tar.gz
%define _archivename_alt2 %{name}-%{version}
# mainnet-release.tar.gz
%define _archivename_alt3 mainnet-release
# beam-mainnet-release.tar.gz
%define _archivename_alt4 %{name}-mainnet-release

# our selection for this build - edit this
%define _archivename %{_archivename_alt4}
%define _srccodetree %{_archivename_alt4}

%if %{includeArchiveQualifier}
  %define archivename %{_archivename}-%{archiveQualifier}
  %define srccodetree %{_srccodetree}-%{archiveQualifier}
%else
  %define archivename %{_archivename}
  %define srccodetree %{_srccodetree}
%endif

# Extracted source tree structure (extracted in .../BUILD)
#   srcroot               beam-1.0.3967
#      \_srccodetree        \_beam-mainnet-release
#      \_srccontribtree     \_beam-1.0.3967-contrib
%define srcroot %{name}-%{vermajor}
%define srccontribtree %{name}-%{vermajor}-contrib
# srccodetree defined earlier

# Note, that ...
# https://github.com/BeamMW/beam/archive/mainnet-release.tar.gz
# ...is the same as...
# https://github.com/BeamMW/beam/archive/mainnet-release/beam-mainnet-release.tar.gz
%if %{includeArchiveQualifier}
Source0: https://github.com/BeamMW/beam/archive/v%{version}-%{archiveQualifier}/%{archivename}.tar.gz
%else
Source0: https://github.com/BeamMW/beam/archive/v%{version}/%{archivename}.tar.gz
%endif
Source1: https://github.com/taw00/beam-rpm/blob/master/source/testing/SOURCES/%{srccontribtree}.tar.gz

# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
#
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
# ...flip-flop next two lines in order to disable (nil) or enable (1) debuginfo package build
%define debug_package 1
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_pie
%define _hardened_build 1

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing
# https://spdx.org/licenses/
License: Apache-2.0
URL: http://www.beam.mw/
# Note, for example, this will not build on ppc64le
ExclusiveArch: x86_64 i686 i386

# As recommended by...
# https://github.com/BeamMW/beam/wiki/How-to-build
BuildRequires: libtool make autoconf automake patch
BuildRequires: gcc-c++ >= 7.0 libstdc++-static
BuildRequires: cmake >= 3.11.0
BuildRequires: gettext
BuildRequires: openssl-devel boost-devel
# Other BuildRequires listed per package below

# tree, vim-enhanced, and less for mock build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils
%endif


# beam-wallet
%package wallet
Summary: Peer-to-peer digital currency implementing mimblewimble, a next generation confidentiality protocol (desktop reference client)
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires: qt5-qtquickcontrols qt5-qtquickcontrols2
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem
Requires(postun): firewalld-filesystem
# Required for installing desktop applications on linux
BuildRequires: libappstream-glib desktop-file-utils
#BuildRequires: qrencode-devel protobuf-devel
BuildRequires: qt5-qtbase-devel qt5-linguist qt5-qtsvg-devel
%if 0%{?fedora}
Requires:       qt5-qtwayland
BuildRequires:  qt5-qtwayland-devel
%endif


# beam-node
%package node
Summary: Peer-to-peer digital currency implementing mimblewimble, a next generation confidentiality protocol (reference node server)
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem
Requires(postun): firewalld-filesystem
# As per https://docs.fedoraproject.org/en-US/packaging-guidelines/Systemd/
#Requires(post): systemd
#Requires(preun): systemd
#Requires(postun): systemd
BuildRequires: systemd
%{?systemd_requires}
Requires(pre): shadow-utils
Requires(post): /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires(postun): /usr/sbin/semodule, /sbin/restorecon, /sbin/fixfiles
Requires: openssl-libs


## dashcore-libs
#%%package libs
#Summary: Peer-to-peer, payments-focused, fungible digital currency, protocol, and platform for payments and decentralized applications (consensus libraries)
#

## dashcore-devel
#%%package devel
#Summary: Peer-to-peer, payments-focused, fungible digital currency, protocol, and platform for payments and decentralized applications (dev libraries and headers)
#Requires: dashcore-libs = %%{version}-%%{release}


## dashcore-utils
#%%package utils
#Summary: Peer-to-peer, payments-focused, fungible digital currency, protocol, and platform for payments and decentralized applications (commandline utilities)

# beam src.rpm
%description
BEAM reference implementation. This is the source package for building
most of the Beam set of binary packages.  It will build
BeamWallet, and beam-{wallet,node,api,miner-client,debuginfo}.

BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol. 

Learn more at www.beam.mw


# beam-wallet
%description wallet
BEAM reference implementation. This package provides a user-friendly(er)
graphical wallet manager (beam-wallet) for personal use.

BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol. 

Learn more at www.beam.mw


# beam-node
%description node
BEAM reference implementation. This package provides beam-node, a peer-to-peer
node server. It is the command line installation without a graphical user
interface.

BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol. 

Learn more at www.beam.mw



## dashcore-libs
#%%description libs
#This package provides libdashconsensus, which is used by third party
#applications to verify scripts (and other functionality in the future).
#
#Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
#focus on serving as a superior means of payment. Dash offers a form of money
#that is portable, inexpensive, divisible and incredibly fast. It can be spent
#securely both online and in person with minimal transaction fees. Dash offers
#instant transactions (InstantSend), fungible transactions (PrivateSend), and,
#as a network, is self-governing and self-funding. This decentralized governance
#and budgeting system makes is the first ever successful decentralized
#autonomous organization (DAO). Dash is also a platform for innovative
#decentralized crypto-tech.
#
#Learn more at www.dash.org.
#
#
## dashcore-devel
#%%description devel
#This package provides the libraries and header files necessary to compile
#programs which use libdashconsensus.
#
#Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
#focus on serving as a superior means of payment. Dash offers a form of money
#that is portable, inexpensive, divisible and incredibly fast. It can be spent
#securely both online and in person with minimal transaction fees. Dash offers
#instant transactions (InstantSend), fungible transactions (PrivateSend), and,
#as a network, is self-governing and self-funding. This decentralized governance
#and budgeting system makes is the first ever successful decentralized
#autonomous organization (DAO). Dash is also a platform for innovative
#decentralized crypto-tech.
#
#Learn more at www.dash.org.
#
#
## dashcore-utils
#%%description utils
#Dash is Digital Cash
#
#This package provides dash-cli, a utility to communicate with and control a
#Dash server via its RPC protocol, and dash-tx, a utility to create custom
#Dash transactions.
#
#Dash (Digital Cash) is an open source peer-to-peer cryptocurrency with a strong
#focus on serving as a superior means of payment. Dash offers a form of money
#that is portable, inexpensive, divisible and incredibly fast. It can be spent
#securely both online and in person with minimal transaction fees. Dash offers
#instant transactions (InstantSend), fungible transactions (PrivateSend), and,
#as a network, is self-governing and self-funding. This decentralized governance
#and budgeting system makes is the first ever successful decentralized
#autonomous organization (DAO). Dash is also a platform for innovative
#decentralized crypto-tech.
#
#Learn more at www.dash.org.



%prep
# Prep section starts us in directory .../BUILD (aka {_builddir})

# Message if EL7 found
# (probably should check for other unsupported OSes as well)
%if 0%{?rhel} && 0%{?rhel} < 8
  %{error: "EL7 builds no longer supported due to outdated build tools (c++, cmake, etc)"}
  # exit doesn't do anything during build phase?
  exit 1
%endif

mkdir -p %{srcroot}
# beam
# {_builddir}/beam-1.0.3967/beam-mainnet-release/
# ..or something like..
# {_builddir}/beam-1.0.3967/beam-testnet4-release/
%setup -q -T -D -a 0 -n %{srcroot}
# contributions
# {_builddir}/beam-1.0.3967/beam-1.0-contrib/
%setup -q -T -D -a 1 -n %{srcroot}
# patches
#%%patch0 -p0


%build
# This section starts us in directory {_builddir}/{srcroot}
cd %{srccodetree}
cmake -DCMAKE_BUILD_TYPE=Release . && make -j4
cd ..



%check
# This section starts us in directory {_builddir}/{srcroot}
cd %{srccodetree}



%install
# This section starts us in directory {_builddir}/{srcroot}

#cd %%{srccodetree}
#make INSTALL="install -p" CP="cp -p" DESTDIR=%%{buildroot} install
#make install
#cd ..

# Cheatsheet for built-in RPM macros:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
#   _builddir = {_topdir}/BUILD
#   _buildrootdir = {_topdir}/BUILDROOT
#   buildroot = {_buildrootdir}/{name}-{version}-{release}.{_arch}
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix or _usr = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
# This is used to quiet rpmlint who can't seem to understand that /usr/lib is
# still used for certain things.
%define _rawlib lib
%define _usr_lib /usr/%{_rawlib}
# These three are already defined in newer versions of RPM, but not in el7
%if 0%{?rhel} && 0%{?rhel} < 8
  %define _tmpfilesdir %{_usr_lib}/tmpfiles.d
  %define _unitdir %{_usr_lib}/systemd/system
  %define _metainfodir %{_datadir}/metainfo
%endif

# Create directories
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_localstatedir}
install -d %{buildroot}%{_sharedstatedir}
install -d %{buildroot}%{_tmpfilesdir}
install -d %{buildroot}%{_unitdir}
install -d %{buildroot}%{_metainfodir}
install -d -m755 -p %{buildroot}%{_bindir}
install -d -m755 -p %{buildroot}%{_libdir}/pkgconfig
install -d -m755 -p %{buildroot}%{_includedir}

# Application as systemd service directory structure
# /etc/beam/
install -d -m750 -p %{buildroot}%{_sysconfdir}/beam
# /var/lib/beam/...
install -d -m750 -p %{buildroot}%{_sharedstatedir}/beam
# /var/log/beam/...
install -d -m700 %{buildroot}%{_localstatedir}/log/beam
# /etc/sysconfig/beam-node-scripts/
install -d %{buildroot}%{_sysconfdir}/sysconfig/beam-node-scripts

# GUI wallet
# ...bins
#cp %%{srccodetree}/ui/BeamWallet %%{buildroot}%%{_bindir}/beam-wallet
cp %{srccodetree}/ui/BeamWallet %{buildroot}%{_bindir}/
install -m755  %{srccontribtree}/linux/desktop/BeamWallet.wrapper.sh %{buildroot}%{_bindir}/
# ...config and desktop xml stuff - the beam-team wants the beam-wallet-cfg in the /usr/bin/dir !?!
#install -D -m644 %%{srccodetree}/ui/beam-wallet.cfg %%{buildroot}%%{_bindir}/beam-wallet.cfg
#install -D -m644 %%{srccodetree}/ui/beam-wallet.cfg %%{buildroot}%%{_sharedstatedir}/beam/beam-wallet.cfg.template-desktop
# the config file is going to become a "document"
install -D -m644 %{srccodetree}/ui/beam-wallet.cfg %{srccodetree}/ui/beam-wallet.cfg.template-desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{srccontribtree}/linux/desktop/BeamWallet.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/BeamWallet.desktop
install -D -m644 -p %{srccontribtree}/linux/desktop/BeamWallet.appdata.xml %{buildroot}%{_metainfodir}/BeamWallet.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml
# ...icons and such
cd %{srccontribtree}/linux/desktop
install -D -m644 beam-hicolor-128.png      %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/beam.png
install -D -m644 beam-hicolor-16.png       %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/beam.png
install -D -m644 beam-hicolor-22.png       %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/beam.png
install -D -m644 beam-hicolor-24.png       %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/beam.png
install -D -m644 beam-hicolor-256.png      %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/beam.png
install -D -m644 beam-hicolor-32.png       %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/beam.png
install -D -m644 beam-hicolor-48.png       %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/beam.png
install -D -m644 beam-hicolor-scalable.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/beam.svg
# ...todo: HighContrast icons
#install -D -m644 beam-HighContrast-128.png      %%{buildroot}%%{_datadir}/icons/HighConstrast/128x128/apps/beam.png
#install -D -m644 beam-HighContrast-16.png       %%{buildroot}%%{_datadir}/icons/HighConstrast/16x16/apps/beam.png
#install -D -m644 beam-HighContrast-22.png       %%{buildroot}%%{_datadir}/icons/HighConstrast/22x22/apps/beam.png
#install -D -m644 beam-HighContrast-24.png       %%{buildroot}%%{_datadir}/icons/HighConstrast/24x24/apps/beam.png
#install -D -m644 beam-HighContrast-256.png      %%{buildroot}%%{_datadir}/icons/HighConstrast/256x256/apps/beam.png
#install -D -m644 beam-HighContrast-32.png       %%{buildroot}%%{_datadir}/icons/HighConstrast/32x32/apps/beam.png
#install -D -m644 beam-HighContrast-48.png       %%{buildroot}%%{_datadir}/icons/HighConstrast/48x48/apps/beam.png
#install -D -m644 beam-HighContrast-scalable.svg %%{buildroot}%%{_datadir}/icons/HighConstrast/scalable/apps/beam.svg
cd ../../..
# CLI wallet
cp %{srccodetree}/wallet/beam-wallet %{buildroot}%{_bindir}/
#install -D -m644 %%{srccodetree}/wallet/beam-wallet.cfg %%{buildroot}%%{_sharedstatedir}/beam/beam-wallet.cfg.template-cli
# the config file is going to become a "document"
install -D -m644 %{srccodetree}/wallet/beam-wallet.cfg %{srccodetree}/wallet/beam-wallet.cfg.template-cli
# API interface
cp %{srccodetree}/wallet/wallet-api %{buildroot}%{_bindir}/beam-wallet-api
# node
cp %{srccodetree}/beam/beam-node %{buildroot}%{_bindir}/
#install -D -m644 %%{srccodetree}/beam/beam-node.cfg %%{buildroot}%%{_bindir}/beam-node.cfg
#install -D -m644 %%{srccodetree}/beam/beam-node.cfg %%{buildroot}%%{_sharedstatedir}/beam/beam-node.cfg.template
# the config file is going to become a "document"
install -D -m644 %{srccodetree}/beam/beam-node.cfg %{srccodetree}/beam/beam-node.cfg.template
# explorer node
cp %{srccodetree}/explorer/explorer-node %{buildroot}%{_bindir}/beam-explorer-node
# miner client
cp %{srccodetree}/pow/miner_client %{buildroot}%{_bindir}/beam-miner-client

# Config
# Install default configuration file (from contrib)
%if %{targetIsProduction}
%define testnet 0
%else
%define testnet 1
%endif

## System services
#install -D -m600 -p %%{srccontribtree}/linux/systemd/etc-sysconfig_beam-node %%{buildroot}%%{_sysconfdir}/sysconfig/beam-node
#install -D -m755 -p %%{srccontribtree}/linux/systemd/etc-sysconfig-beam-node-scripts_beam-node.send-email.sh %%{buildroot}%%{_sysconfdir}/sysconfig/beam-node-scripts/beam-node.send-email.sh
#install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-systemd-system_beam-node.service %%{buildroot}%%{_unitdir}/beam-node.service
#install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-tmpfiles.d_beam-node.conf %%{buildroot}%%{_tmpfilesdir}/beam-node.conf

# Log files
# ...logrotate file rules
#install -D -m644 -p %%{srccontribtree}/linux/logrotate/etc-logrotate.d_beam %%{buildroot}/etc/logrotate.d/beam
# ...ghosted log files - need to exist in the installed buildroot
touch %{buildroot}%{_localstatedir}/log/beam/debug.log

## Service definition files for firewalld for full and master nodes
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore.xml
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-testnet.xml
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-rpc.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-rpc.xml
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet-rpc.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-testnet-rpc.xml



# beam-wallet
%post wallet
# firewalld only partially picks up changes to its services files without this
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :

%postun wallet
# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


# beam-node
%pre node
# This is for the case that you run BEAM as a service (systemctl start beam-node ?t0dd?)
# _sharedstatedir is /var/lib
getent group beamuser >/dev/null || groupadd -r beamuser
getent passwd beamuser >/dev/null || useradd -r -g beamuser -d %{_sharedstatedir}/beam -s /sbin/nologin -c "System user 'beamuser' to isolate BEAM execution" beamuser

# Notes:
#  _localstatedir is /var
#  _sharedstatedir is /var/lib
#  /var/lib/beam is the $HOME for the beamuser user

#t0dd: DEBUG IS DIFFERENT FOR BEAM (versus dash)
## Fix the debug.log directory structure if it is not aligned to /var/log/
## standards.
## If /var/lib/beam/debug.log is not a symlink, we need to fix that.
##    /var/lib/beam/debug.log -> /var/log/beam/debug.log
#%%define vlibb %%{_sharedstatedir}/beam
#%%define vlibb_dl %%{vlibb}/debug.log
#%%define vlogb %%{_localstatedir}/log/beam
#%%define vlogb_dl %%{vlogb}/debug.log
## If either debug.log in /var/lib/beam is not a symlink, we need to move
## files and then fix the symlinks Hopefully this doesn't break because
## beam may have debug.log open
#if [ -e %%{vlibb_dl} -a -f %%{vlibb_dl} -a ! -h %%{vlibb_dl} ]
#then
#   mv %%{vlibb_dl}* %%{vlogb}/
#   ln -s %%{vlogb_dl} %%{vlibb_dl}
#   chown beamuser:beamuser %%{vlibb_dl}
#   chown -R beamuser:beamuser %%{vlogb}
#   chmod 644 %%{vlogb_dl}*
#fi

exit 0


# beam-node
%post node
#%%systemd_post beam-node.service
# firewalld only partially picks up changes to its services files without this
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


# beam-node
%posttrans node
/usr/bin/systemd-tmpfiles --create
#TODO: Replace above with %%tmpfiles_create_package macro
#TODO: https://github.com/systemd/systemd/blob/master/src/core/macros.systemd.in


# beam-node
%preun node
#%%systemd_preun beam-node.service


# beam-node
%postun node
#%%systemd_postun beam-node.service
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true



# beam-wallet
%files wallet
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%doc %{srccodetree}/ui/beam-wallet.cfg.template-desktop
%doc %{srccodetree}/wallet/beam-wallet.cfg.template-cli
%{_bindir}/BeamWallet
%{_bindir}/BeamWallet.wrapper.sh
%{_bindir}/beam-wallet
%{_bindir}/beam-wallet-api
%{_datadir}/applications/BeamWallet.desktop
%{_metainfodir}/BeamWallet.appdata.xml
%{_datadir}/icons/*
#%%{_usr_lib}/firewalld/services/dashcore.xml
#%%{_usr_lib}/firewalld/services/dashcore-rpc.xml


# beam-node
%files node
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%doc %{srccodetree}/beam/beam-node.cfg.template

# Application as systemd service directory structure
%defattr(-,beamuser,beamuser,-)
# /etc/beam/
%dir %attr(750,beamuser,beamuser) %{_sysconfdir}/beam
# /var/lib/beam/...
%dir %attr(750,beamuser,beamuser) %{_sharedstatedir}/beam
# /var/log/beam/...
%dir %attr(700,beamuser,beamuser) %{_localstatedir}/log/beam
# /etc/sysconfig/beam-node-scripts/
%dir %attr(755,beamuser,beamuser) %{_sysconfdir}/sysconfig/beam-node-scripts
%defattr(-,root,root,-)

#%%config(noreplace) %%attr(600,root,root) %%{_sysconfdir}/sysconfig/beam-node
#%%attr(755,root,root) %%{_sysconfdir}/sysconfig/beam-node-scripts/beam-node.send-email.sh

# The logs
#%%attr(644,root,root) /etc/logrotate.d/dashcore
# ...log files - they don't initially exist, but we still own them
%ghost %{_localstatedir}/log/beam/debug.log
%defattr(-,root,root,-)

#%%{_unitdir}/beam-node.service
#%%{_usr_lib}/firewalld/services/dashcore.xml
#%%{_usr_lib}/firewalld/services/dashcore-rpc.xml
%{_bindir}/beam-node
%{_bindir}/beam-miner-client
%{_bindir}/beam-explorer-node
#%%{_tmpfilesdir}/beam-node.conf



## dashcore-libs
#%%files libs
#%%defattr(-,root,root,-)
#%%license %%{srccodetree}/COPYING
#%%{_libdir}/*


## dashcore-devel
#%%files devel
#%%defattr(-,root,root,-)
#%%license %%{srccodetree}/COPYING
#%%{_includedir}/*
#%%{_libdir}/*


## dashcore-utils
#%%files utils
#%%defattr(-,root,root,-)
#%%license %%{srccodetree}/COPYING
#%%{_bindir}/dash-cli
#%%{_bindir}/dash-tx


# Beam Information
#
# Beam...
#   * Project website: https://www.beam.mw/
#   * Mainnet launch: https://medium.com/beam-mw/mimblewimble-mainnet-release-notes-8766e49e241d
#   * Project documentation: https://beam-docs.readthedocs.io/en/latest/
#   * Project wiki: https://github.com/BeamMW/beam/wiki
#   * Developer documentation: 
#
# Beam on Fedora/CentOS/RHEL...
#   * Git Repo: https://github.com/taw00/beam-rpm
#   * Documentation: 
#
# The last major testnet effort...
#   * Announcement: 
#   * Documentation:  
#     
#
# Source snapshots...
#     https://github.com/BeamMW/beam/tags
#     https://github.com/BeamMW/beam/releases
#
# Beam git repos...
#   * https://github.com/BeamMW/beam

%changelog
* Mon Jan 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3967-0.4.testing.taw
  - made shipped beam-wallet.cfg and beam-node.cfg files "templates" and  
    organized as docs
  - fixed license label. Apache-2.0 instead of ASL 2.0 -- there is  
    discrepancy in the RPM documentation

* Mon Jan 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3967-0.3.testing.taw
  - qt5-qtquickcontrols and qt5-qtquickcontrols2 added to Requires

* Mon Jan 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3967-0.2.testing.taw
  - Added desktop icons

* Sun Jan 06 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3967-0.1.testing.taw
  - Initial build
