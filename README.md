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

If you want to to use the Lexicon DNS API support:

    sudo yum install python34 python34-pip
    pip3 install --user dns-lexicon

### Hetzner Cloud

You will need an account at: https://console.hetzner.cloud

Additionally you will need the `hcloud` command line tool: https://github.com/hetznercloud/cli/releases

Register your account with `hcloud context create …`. Also see: https://github.com/hetznercloud/cli#getting-started

### Local configuration

You will need to create a file called `config` in this directory. You may use
the file `config.example` as a basis for this.

### DNS integeration

See: [dns/README.md](dns/README.md)

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

    persistentvolume "pv-18" created
    persistentvolume "pv-19" created
    persistentvolume "pv-20" created

After that the machine will be rebooted one last time.

## Accessing OKD

Once the setup is complete you can access the instance using either the
Web Console or the `oc` command line tool on port 8443. Using the credentials
`developer` / `developer` (note: it might be wise to change them!)

## About the environment

By default a user `developer` will be created, which has the password `developer` set
as a default. You can change this in the configuration.

Optionally you can create an `admin` user, which has cluster admin privileges assigned.
By default this user will not be created, but you can enable the creating by specifying a
password for the admin user in the variable `ADMIN_PASSWORD`, in the configuration.

This setup will also create a few PVs, backed by the local storage and attached by using NFS.

The hostname will be printed out by the `create` command. You can access the
server using the Web UI or the API using the URL `https://<dns-name>:8443`


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
