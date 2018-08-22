# Fixing SElinux

Unfortunately Hetzner decided that SElinux is confusing to people, and decided to
deactivate it. However SElinux is a requirement, when using OpenShift/OKD and
so we need to re-enable it. This requires at least one reboot, better two.

So instead of directly calling into the `/okd/setup` script from the cloud-init
module, we need to first enable SElinux, reboot to re-label and then reboot to
have a fresh start. Then we can start the actual OKD installation.

For this a systemd unit is being used. It gets created and enabled during the
first boot. Then it tracks its state, using marker files and finally removes
itself from the system.

If the CentOS image would have SElinux enabled it would be sufficient to
directly call into `okd/setup` at the end of cloud-init.
