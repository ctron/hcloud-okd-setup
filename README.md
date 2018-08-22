# OKD setup for Hetzner Cloud

This folder takes care of setting up a new machine with OKD and performs all
the necessary configuration. The idea is to be able to create a bunch of
OKD clusters, with proper TLS and DNS support, running on a public infrastructure.

**Note:** This module uses Git submodules. Either clone with `--recursive` or run `git submodule update --init --recursive` after cloning.

## Prepare yourself

This setup requires a few things before you can start.

### Software

You will need CentOS/RHEL, and a few tools installed:

    sudo yum install gettext

If you wanto to use the Plesk DNS support:

    sudo yum install python34 python34-pip
    pip3 install --user xmltodict

### Hetzner Cloud

You will need an account at: https://console.hetzner.cloud

Additionally you will need the `hcloud` command line tool: https://github.com/hetznercloud/cli/releases

Register your account with `hcloud context create …`. Also see: https://github.com/hetznercloud/cli#getting-started

### Local configuration

You will need to create a file called `config` in this directory. You may use
the file `config.example` as a basis for this.

### TLS with Let's encrypt

See: [letsencrypt/README.md](letsencrypt/README.md) 

## Creating a new instance

After you done all the preparations you can simple create a new instance by calling

    ./create foo-bar

And the setup will begin to create your new OKD instance. You can log in to the
machine using.

It takes around 10-15 minutes until the installation is ready. You can check
the progress in the file `/var/log/okd-setup.log`. The setup if complete if
the last line shows:

    

And the machine rebooted one last time.

## The process

This is what will happen when you create a new machine:

* Create a new server instance, upload the `cloud-config.yaml` file in the process
* Register the newly assigned IP with the DNS
* When the machine boots:
  * Run first boot cloud init
    * Install a bunch of packages
    * Set SElinux to "permissive"
    * Create the "run-on-boot" service
    * Reboot
  * The machine will reboot, the "run-on-boot" service will be executed:
    * SElinux will relabel the filesystem
    * SElinux will be switched to enforcing
    * Reboot
  * Again the "run-on-boot" script will be called
    * Disable the "run-on-boot" service
    * Run `/okd/setup`
    * Delete the "run-on-boot" service
    * Reboot

The SElinux steps are necessary as Hetzner has SElinux disabled by default,
however SElinux is required by OKD. Also see [fix-selinux/README.md](fix-selinux/README.md).

## Accessing OKD

Once the setup is complete you can access the instance using either the
Web Console or the `oc` command line tool on port 8443. Using the credentials
`developer` / `developer` (note: it might be wise to change them!)

The hostname depends on whether you used a full DNS setup or used the backup
using `nip.io`. In the latter case, your URL will be something like
`http://1.2.3.4.nip.ip`, if your instance IP was `1.2.3.4`.

If you have a full DNS setup, then you will have the instance available at:

    https://<INSTANCE_NAME>.<SUB_DOMAIN_PART>.<BASE_DOMAIN>:8443/

Assuming `INSTANCE_NAME=cluster01`, `SUB_DOMAIN_PART=amazing`,
`BASE_DOMAIN=iot-playground.org`, then the full domain name would be:

    https://cluster01.amazing.iot-playground.org:8443
