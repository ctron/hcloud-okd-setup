# Let's encrypt this setup

This setup makes use of [Let's encrypt](https://letsencrypt.org/) to secure the
whole setup using trusted certificates.

**Note:** If you think Let's encrypt is awesome, then please consider donating:
          https://letsencrypt.org/donate/

## Some details

This setup will re-use the same wildcard certificate for all cluster instances.
The domain is `iot-playground.org` and the DNS base name is `amazing.iot-playground.org`.
Each cluster will have its own name, e.g. `cluster01`, and so the full cluster
DNS name will be `cluster01.amazing.iot-playground.org`, with a service name
(e.g. `messaging` of `enmasse`) of `messaging-enmasse.cluster01.amazing.iot-playground.org`.

Unfortunately a single wildcard certificate for `*.amazing.iot-playground.org`
is not sufficient. For covering e.g. `messaging-enmasse.cluster01.amazing.iot-playground.org`
if would require a double wildcard for `*.*.amazing.iot-playground.org`,
however that is not supported.

What works instead is to register a certificate with alternate names, which may
include wildcards. So there is a request for a single certificate of:
`cluster01.amazing.iot-playground.`, `*.cluster01.amazing.iot-playground.`,
`cluster02.amazing.iot-playground.`, `*.cluster01.amazing.iot-playground.`, …

What still is required, is to point DNS A records towards the
specific server instance of that cluster (e.g. having `1.2.3.4` as IP):

    cluster01.amazing.iot-playground.org        A    1.2.3.4
    *.cluster01.amazing.iot-playground.org      A    1.2.3.4

The bootstrap scripts of the servers will fetch the private key from a secret
location, during the setup process. This location is provided during the
creation of the server instance and not checked in to this repository.

## 90 days limit

This will of course only work for 90 days. Let's encrypt certificates are only
valid for 90 days, and have to be renewed before that. The renew process
normally is automated, but I do have two issues, in this case, with the
automation of the process. First of all, I don't have an API to my DNS which is
supported by any of the Let's encrypt (ACME) clients. However the renewal
process requires to add TXT records to the DNS setup during the process to
verify you are in control of the DNS domain. Second, after the certificate has
been renewed, it must be rolled out to OKD instances. And this requires
re-running all the Ansible playbooks.

On the other hand, having a single, 90 day certificate works fine for this
tutorial ;-)

## Do this at home

I can't provide an out-of-the-box setup including TLS+DNS, as this depends
on what DNS provider you have and which domain structure you want to use.

I did use my own domain `iot-playground.org` and went for a sub-domain of
that: `amazing.iot-playground.org`. As I am using Plesk to administer that
domain, I need to fall back to some howngrown scripts for talking to the
Plesk API.

If you want to enable TLS with this setup, you need to do the following:

* Own/register a domain – You may use a sub-domain as well. It is helpful if
  you can remotely access the DNS service using some kind of API supported
  by "acme.sh"
* Create a wildcard certificate for this using e.g. [acme.sh](https://github.com/Neilpang/acme.sh):
      ./acme.sh --issue -d "cluster01.amazing.iot-playground.org" -d '*.cluster01.amazing.iot-playground.org' --dns dns_plesk
* Copy the creates key, certificate and fullchain files to some secret location,
  e.g. `https://foo.bar/6bc2bf48-a1f7-11e8-996a-c85b762e5a2c` ... The files must
  be named `server.key`, `server.cer`, `fullchain.cer`. So altogether you
  need the following three URLs:
    * https://foo.bar/6bc2bf48-a1f7-11e8-996a-c85b762e5a2c/server.key
    * https://foo.bar/6bc2bf48-a1f7-11e8-996a-c85b762e5a2c/server.cer
    * https://foo.bar/6bc2bf48-a1f7-11e8-996a-c85b762e5a2c/fullchain.cer
  Of course you need to be careful not to expose the URLs by some kind of
  directory index, …
* Then run the `create` script. And immediately after running the script,
  create the DNS A records, pointing the DNS names towards the newly created IP
  address. You need two DNS A records, one for the main sub-sub-domain and one
  for the wildcard entry. e.g `cluster01.amazing.iot-playground.org` and
  `*.cluster01.amazing.iot-playground.org`.
  
  If you are using Plesk like me, the `DNS_MODE` may be set to `plesk` and
  you can let the script to the rest.
