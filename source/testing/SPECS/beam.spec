# BEAM Cryptocurrency implementing Mimblewimble - full node and wallet
# Reference implementation
# vim:tw=0:ts=2:sw=2:et:
#
# This is the rpm source spec for building a Beam Reference Desktop (or
# commandline) Wallet, and Full Node.
#
# Consumer facing...
# * WALLETs
#   - BeamWallet (desktop) -- rpm is beam-wallet-desktop
#   - beam-wallet (cli) -- rpm is beam-wallet-cli
#   - beam-wallet-api -- rpm is beam-wallet-api (sucked in with beam-wallet-desktop or beam-wallet-cli RPM)
# * NODEs
#   - beam-node -- rpm is beam-node
#   - beam-miner-client -- rpm is beam-node (for now)
#   - beam-explorer-node -- rpm is beam-node (for now)
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
%define codename agile-atom
Summary: Peer-to-peer digital currency implementing mimblewimble, a next generation confidentiality protocol

%define targetIsProduction 0

# ARCHIVE QUALIFIER - edit this if applies
# ie. if the dev team includes things like rc3 in the filename
%define archiveQualifier rc1
%define includeArchiveQualifier 0

# VERSION - edit this
%define vermajor 1.1
%define verminor 4202
Version: %{vermajor}.%{verminor}

# RELEASE - edit this
# package release, and potentially extrarel
%define _pkgrel 1
%if ! %{targetIsProduction}
  %define _pkgrel 0.1
%endif

# MINORBUMP - edit this
# builder's initials and often a numeral for very small or rapid iterations
# taw, taw0, taw1, etc.
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
# Whoever is doing the beam releases has no consistency...
# example: v1.1.4194.tar.gz
%define _archivename_alt1 v%{version}
# example: beam-1.1.4194.tar.gz
%define _archivename_alt2 %{name}-%{version}
# example: beam-agile-atom-1.1.4194.tar.gz
%define _archivename_alt3 %{name}-%{codename}-%{version}
# example: beam-agile-atom-4202.tar.gz
%define _archivename_alt4 %{name}-%{codename}-%{verminor}

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
#   srcroot               beam-{vermajor}
#      \_srccodetree        \_beam-{codename}-{verminor}
#      \_srccontribtree     \_beam-{vermajor}-contrib
%define srcroot %{name}-%{vermajor}
#%%define srccontribtree %%{name}-%{vermajor}-contrib
%define srccontribtree %{name}-1.0-contrib
# srccodetree defined earlier

# Note, that ...
# https://github.com/BeamMW/beam/archive/{codename}-{version}.tar.gz
# ...is the same as...
# https://github.com/BeamMW/beam/archive/{codename}-{version}/beam-{codename}-{version}.tar.gz
%if %{includeArchiveQualifier}
Source0: https://github.com/BeamMW/beam/archive/%{codename}-%{version}-%{archiveQualifier}/%{archivename}.tar.gz
%else
Source0: https://github.com/BeamMW/beam/archive/%{codename}-%{version}/%{archivename}.tar.gz
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


# beam-wallet-desktop
%package wallet-desktop
Summary: Peer-to-peer digital currency implementing mimblewimble, a next generation confidentiality protocol (desktop reference client)
# beam-wallet --> beam-wallet-desktop as of 1.0.3976-0.5
Provides: beam-wallet = 1.0.3976-0.5
Obsoletes: beam-wallet < 1.0.3976-0.5
Requires: beam-wallet-api = %{version}-%{release}
Requires: qt5-qtquickcontrols qt5-qtquickcontrols2
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
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

# beam-wallet-cli
%package wallet-cli
Summary: Peer-to-peer digital currency implementing mimblewimble, a next generation confidentiality protocol (commandline-interfacing reference client)
Requires: beam-wallet-api = %{version}-%{release}
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem
Requires(postun): firewalld-filesystem

# beam-wallet-api
%package wallet-api
Summary: Peer-to-peer digital currency implementing mimblewimble, a next generation confidentiality protocol (wallet API)

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



# beam src.rpm
%description
BEAM reference implementation. This is the source package for building
most of the Beam set of binary packages.  It will build
BeamWallet, and beam-{wallet,node,api,miner-client,debuginfo}.

BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol. 

Learn more at www.beam.mw


# beam-wallet-desktop
%description wallet-desktop
BEAM reference implementation. This package provides a user-friendly(er)
graphical wallet manager (BeamWallet) for personal use.

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


# beam-wallet-cli
%description wallet-cli
BEAM reference implementation. This package provides a powerful wallet for use
on the commandline (beam-wallet). For a more user-friendly experience, if you
need a desktop interface, install the beam-wallet RPM instead.

BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol. 

Learn more at www.beam.mw


# beam-wallet-api
%description wallet-api
BEAM reference implementation. This package provides a powerful wallet API
(application programming interface) that enables many programmable elements for
interfacing with a running beam wallet.

BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol. 

Learn more at www.beam.mw



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
# {_builddir}/beam-1.0.3976/beam-mainnet-release/
# ..or something like..
# {_builddir}/beam-1.0.3976/beam-testnet4-release/
%setup -q -T -D -a 0 -n %{srcroot}
# contributions
# {_builddir}/beam-1.0.3976/beam-1.0-contrib/
%setup -q -T -D -a 1 -n %{srcroot}
# patches
#cd %%{srccodetree}
#%%patch0 -p1
#cd ..


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
# /var/lib/beam/... - beamuser's $HOME directory
install -d -m750 -p %{buildroot}%{_sharedstatedir}/beam
## /etc/sysconfig/beam-node-scripts/
#install -d %%{buildroot}%%{_sysconfdir}/sysconfig/beam-node-scripts

# GUI wallet
# ...bins
cp %{srccodetree}/ui/BeamWallet %{buildroot}%{_bindir}/
install -m755  %{srccontribtree}/linux/desktop/BeamWallet.wrapper.sh %{buildroot}%{_bindir}/
ln -s %{_bindir}/BeamWallet.wrapper.sh %{buildroot}%{_bindir}/beam-wallet-desktop
# ...config and desktop xml stuff - the shipped config file becomes a "document"
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
ln -s %{_bindir}/beam-wallet %{buildroot}%{_bindir}/beam-wallet-cli
# ...the shipped config file becomes a "document"
install -D -m644 %{srccodetree}/wallet/beam-wallet.cfg %{srccodetree}/wallet/beam-wallet.cfg.template-cli
# API interface
cp %{srccodetree}/wallet/wallet-api %{buildroot}%{_bindir}/beam-wallet-api
# node
cp %{srccodetree}/beam/beam-node %{buildroot}%{_bindir}/
# ...the shipped config file becomes a "document"
install -D -m644 %{srccodetree}/beam/beam-node.cfg %{srccodetree}/beam/beam-node.cfg.template
# explorer node
cp %{srccodetree}/explorer/explorer-node %{buildroot}%{_bindir}/beam-explorer-node
# miner client
cp %{srccodetree}/pow/miner_client %{buildroot}%{_bindir}/beam-miner-client

## System services
#install -D -m600 -p %%{srccontribtree}/linux/systemd/etc-sysconfig_beam-node %%{buildroot}%%{_sysconfdir}/sysconfig/beam-node
#install -D -m755 -p %%{srccontribtree}/linux/systemd/etc-sysconfig-beam-node-scripts_beam-node.send-email.sh %%{buildroot}%%{_sysconfdir}/sysconfig/beam-node-scripts/beam-node.send-email.sh
#install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-systemd-system_beam-node.service %%{buildroot}%%{_unitdir}/beam-node.service
#install -D -m644 -p %%{srccontribtree}/linux/systemd/usr-lib-tmpfiles.d_beam-node.conf %%{buildroot}%%{_tmpfilesdir}/beam-node.conf

## Service definition files for firewalld for full and master nodes
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore.xml
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-testnet.xml
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-rpc.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-rpc.xml
#install -D -m644 -p %%{srccontribtree}/linux/firewalld/usr-lib-firewalld-services_dashcore-testnet-rpc.xml %%{buildroot}%%{_usr_lib}/firewalld/services/dashcore-testnet-rpc.xml



# beam-wallet-desktop
%post wallet-desktop
# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :
# firewalld only partially picks up changes to its services files without this
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

%postun wallet-desktop
# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :
# the macro'ed reload is not working for some reason
#%%firewalld_reload
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# beam-wallet-cli
%post wallet-cli
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

%postun wallet-cli
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true


# beam-node
%pre node
# This is for the case that you run BEAM as a service (systemctl start beam-node ?t0dd?)
# _sharedstatedir is /var/lib - /var/lib/beam is the $HOME for the beamuser user
getent group beamuser >/dev/null || groupadd -r beamuser
getent passwd beamuser >/dev/null || useradd -r -g beamuser -d %{_sharedstatedir}/beam -s /sbin/nologin -c "System user 'beamuser' to isolate BEAM execution" beamuser

# beam-node
%post node
#%%systemd_post beam-node.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# beam-node
%posttrans node
#/usr/bin/systemd-tmpfiles --create
#TODO: Replace above with %%tmpfiles_create_package macro
#TODO: https://github.com/systemd/systemd/blob/master/src/core/macros.systemd.in

# beam-node
%preun node
#%%systemd_preun beam-node.service

# beam-node
%postun node
#%%systemd_postun beam-node.service
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true



# beam-wallet-desktop
%files wallet-desktop
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%doc %{srccodetree}/ui/beam-wallet.cfg.template-desktop
%doc %{srccontribtree}/USAGE-WARNING.txt
%{_bindir}/BeamWallet
%{_bindir}/BeamWallet.wrapper.sh
%{_bindir}/beam-wallet-desktop
%{_datadir}/applications/BeamWallet.desktop
%{_metainfodir}/BeamWallet.appdata.xml
%{_datadir}/icons/*
#%%{_usr_lib}/firewalld/services/dashcore.xml
#%%{_usr_lib}/firewalld/services/dashcore-rpc.xml

# beam-wallet-cli
%files wallet-cli
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%doc %{srccodetree}/wallet/beam-wallet.cfg.template-cli
%doc %{srccontribtree}/USAGE-WARNING.txt
%{_bindir}/beam-wallet
%{_bindir}/beam-wallet-cli
%{_bindir}/beam-wallet-api
#%%{_usr_lib}/firewalld/services/dashcore.xml
#%%{_usr_lib}/firewalld/services/dashcore-rpc.xml

# beam-wallet-api
%files wallet-api
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%{_bindir}/beam-wallet-api


# beam-node
%files node
%defattr(-,root,root,-)
%license %{srccodetree}/LICENSE
%doc %{srccodetree}/beam/beam-node.cfg.template
%{_bindir}/beam-node
%{_bindir}/beam-miner-client
%{_bindir}/beam-explorer-node

# Application as systemd service directory structure
%defattr(-,beamuser,beamuser,-)
# /var/lib/beam/... - beamuser's $HOME dir
%dir %attr(750,beamuser,beamuser) %{_sharedstatedir}/beam
## /etc/sysconfig/beam-node-scripts/
#%%dir %%attr(755,beamuser,beamuser) %%{_sysconfdir}/sysconfig/beam-node-scripts
%defattr(-,root,root,-)

#%%config(noreplace) %%attr(600,root,root) %%{_sysconfdir}/sysconfig/beam-node
#%%attr(755,root,root) %%{_sysconfdir}/sysconfig/beam-node-scripts/beam-node.send-email.sh

#%%{_unitdir}/beam-node.service
#%%{_usr_lib}/firewalld/services/dashcore.xml
#%%{_usr_lib}/firewalld/services/dashcore-rpc.xml
#%%{_tmpfilesdir}/beam-node.conf


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
#
# Source snapshots...
#     https://github.com/BeamMW/beam/tags
#     https://github.com/BeamMW/beam/releases
#
# Beam git repos...
#   * https://github.com/BeamMW

%changelog
* Tue Jan 22 2019 Todd Warner <t0dd_at_protonmail.com> 1.1.4202-0.1.testing.taw
  - v1.1.4202 -- aka agile-atom-4202
  - beam team release team has no consistency.

* Thu Jan 17 2019 Todd Warner <t0dd_at_protonmail.com> 1.1.4194-0.1.testing.taw
  - codename-version: agile-atom-1.1.4194
  - team is adding codenames... just lovely</sarcasm>

* Fri Jan 11 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3976-0.7.testing.taw
  - Added beam-wallet-desktop and beam-wallet-cli symlinks to use as  
    alternative executables IMHO, "BeamWallet" as a command is just horrid  
    and "beam-wallet" as the commandline app executable just adds to the  
    inconsistency.

* Thu Jan 10 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3976-0.6.testing.taw
  - Added README.USAGE.WARNING.txt

* Mon Jan 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3976-0.5.testing.taw
  - MUCH cleanup
  - Split out beam-wallet-cli and beam-wallet-api packages
  - Renamed package: beam-wallet --> beam-wallet-desktop
  - Removed reference to /var/log/debug since we'll never probably use it
  - Removed reference to /etc/beam since we'll never probably use it

* Mon Jan 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3976-0.4.testing.taw
  - shipped beam-wallet.cfg and beam-node.cfg files are "templates" and  
    organized as docs
  - fixed license label. Apache-2.0 instead of ASL 2.0 -- there is  
    discrepancy in the RPM documentation

* Mon Jan 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3976-0.3.testing.taw
  - qt5-qtquickcontrols and qt5-qtquickcontrols2 added to Requires

* Mon Jan 07 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3976-0.2.testing.taw
  - Added desktop icons

* Sun Jan 06 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.3976-0.1.testing.taw
  - Initial build
