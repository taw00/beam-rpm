# BEAM for Fedora Linux

_"BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol."_

This github repository is used to develop and maintain packages that make
installing and updating Beam on Fedora Linux[1] native to the platform, more
consistent, less error-prone, and more complete. These builds are not officially
blessed by anyone but me, so be cautioned.

See also: <https://www.beam.mw/>,
<https://beam-docs.readthedocs.io/en/latest/>,
<https://github.com/BeamMW/beam>, and <https://github.com/BeamMW/beam/wiki>

**Source:** This github provides source RPM build trees and instruction only.

**Binaries:** Binary RPMs built from the source provided here are maintained
separately in COPR. Access to the Beam package repositories is provided by repo
RPM whose installation is demonstated below.

## *"TL;DR ...I just want to install the Beam GUI Wallet!"*

```bash
# My system is Fedora...
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/beam-rpm/master/toddpkgs-beam-repo.fedora.testing.rpm
sudo dnf install -y beam-wallet --refresh
BeamWallet.wrapper.sh
```

**Boom! Done!** You should now see a Beam Wallet graphical application
open up on your screen. Note that there is now also a reference to it in your
desktop menus (you don't have to run it from the commandline).


## *"TL;DR ...I just want to install the Beam Node!"*

```bash
# My system is Fedora...
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/beam-rpm/master/toddpkgs-beam-repo.fedora.testing.rpm
sudo dnf install -y beam-node --refresh
```

```bash
# Create a working directory...
mkdir beam-node-data
```

```bash
# Copy the configuration template from the docs to your local working directory...
cp /usr/share/doc/beam-node/beam-node.cfg.template ./beam-node-data/
cd beam-node-data
mv beam-node-cfg.template beam-node.cfg
```

Now, edit `beam-node.cfg` and set `peer=` to one of the peers listed here
<https://www.beam.mw/downloads> ("Mainnet IPs").

```bash
# Run the node...
beam-node
```

**READ THE DOCS!** <https://beam-docs.readthedocs.io/en/latest/rtd_pages/user_desktop_wallet_guide.html>

***Important confusion point in the docs:***  
Please note that if you configure a `.cfg` configuration file, the file is
expected to be located in whatever directory you are in when you run either the
wallet or the node (hence the node example above). If you run the wallet from
the desktop menus the _present working directory_ is your home directory. The
project documentation suggests that the configuration file needs to be located
where the binary executable is located, and this is incorrect. An issue has
been filed on this point: <https://github.com/BeamMW/beam-docs/issues/2>

&nbsp;

## Disclaimers!

**Disclaimer1:** Please note that these builds have not been endorsed by the
Beam Team. I have a reputation though from building (Dash
RPMs)[https://github.com/taw00/dashcore-rpm] for years and years that have been
semi-officially-blessed by that team. So take that for what it is worth. That
being said, proceed with caution and as always... Trust no one. At least be
suspicious of everyone. :)

**Disclaimer2:**  
These packages have been successfully built and tested, but I lay no claim
that they are absolutely free of any bugs in the code, default configuration,
documented configuration, or in the builds or how those builds are
deployed/installed.

Users must assume the risks associated to both community built and
deployed packages and, of course, any cryptocurrency funds managed by this
software. I.e., These will probably work for you, but I can't be liable for any
loss of funds or damages associated to this software.

&nbsp;

**Send comment and feedback** - <https://keybase.io/toddwarner>

Come say hello to me. I am t0dd or taw in various forums, chat platforms, etc.

If you like my BEAM stuff, also check out my Dash builds
(<https://github.com/taw00/dashcore-rpm>), and my more experimental Zcash
builds (<https://github.com/taw00/zcash-rpm>). I am a fan of both endeavors.
Don't troll me. :)

---
[1] _Note: Only Fedora is being targeted for builds at this time. CentOS and
RHEL (EL7) are simply too dated at this point. These packages can't be easily
build given the default gcc and cmake provided by EL7 platforms. Gotta wait for
EL8 coming sometime in 2019._
