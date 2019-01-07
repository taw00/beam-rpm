# BEAM for Fedora Linux

_"BEAM is a next generation confidential cryptocurrency based on an elegant and
innovative Mimblewimble protocol."_

See also: <https://www.beam.mw/>,
<https://beam-docs.readthedocs.io/en/latest/>,
<https://github.com/BeamMW/beam>, and <https://github.com/BeamMW/beam/wiki>

This github repository is used to develop and maintain Beam natively built and
packaged for Fedora Linux (and perhaps someday, CentOS, and Red Hat Enterprise
Linux (currently RHEL and CentOS gcc libraries and cmake are simply too dated).

**Source:** RPM build trees (source only) can be found under the "source"
directory.

**Binary RPMs:** Maintained in COPR... and Coming soon.

## *"TL;DR ...I just want to install the Beam GUI Wallet!"*

Proper packaging and repositories make installation and future upgrades
trivial.

Assuming you are logging in as a normal user who has `sudo` priviledges.<br />
At the terminal command line...

```bash
# My system is Fedora...
sudo rpm --import https://keybase.io/toddwarner/key.asc
sudo dnf install -y https://raw.githubusercontent.com/taw00/beam-rpm/master/toddpkgs-beam-repo.fedora.testing.rpm
sudo dnf install -y beam-wallet --refresh
beam-wallet
```

...if using CentOS or RHEL

Too bad. RHEL and CentOS are not targetted builds at this time.

**Boom! Done!** You should now see a Beam Wallet graphical application
open up on your screen and a reference to it in your desktop menus.

READ THE DOCS! <https://beam-docs.readthedocs.io/en/latest/rtd_pages/user_desktop_wallet_guide.html>

&nbsp;

## Disclaimers!

[1] Please note that these builds have not been endorsed by the Beam Team. I
have a reputation though in building Dash RPMs for years and years that have
been blessed by that team. That being said, proceed with caution and as
always... Trust no one. At least, be suspicious of everyone. :)

[2] These packages have been successfully built and tested, but I lay no claim
that they are absolutely free of any bugs in the code, default configuration,
documented configuration, or in the builds or how those builds are
deployed/installed.

Users must assume the risks associated to both community built and
deployed packages and, of course, any cryptocurrency funds managed by this
software. I.e., These will probably work for you, but I can't be liable for any
loss of funds or damages associated to this software.

**Send comment and feedback** - <https://keybase.io/toddwarner>

Come say hello to me. I am t0dd or taw in various forums.

If you like my BEAM stuff, also check out my Dash builds
(<https://github.com/taw00/dashcore-rpm>), and my more experimental Zcash
builds (<https://github.com/taw00/zcash-rpm>). I am a fan of both endeavors.
Don't troll me. :)
