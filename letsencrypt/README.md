# Let's encrypt this setup

This setup makes use of [Let's encrypt](https://letsencrypt.org/) to secure the
whole setup using trusted certificates.

**Note:** If you think Let's encrypt is awesome, then please consider donating:
          https://letsencrypt.org/donate/

This setup will re-use the same wildcard certificate for all cluster instances.
The domain is `iot-playground.org` and the DNS base name is `amazing.iot-playground.org`.
Each cluster will have its own name, e.g. `cluster01`, and so the full cluster
DNS name will be `cluster01.amazing.iot-playground.org`, with a service name
(e.g. `messaging` of `enmasse`) of `messaging-enmasse.cluster01.amazing.iot-playground.org`.

So a single wildcard certificate for `*.amazing.iot-playground.org` is
sufficient. And the only thing required, is to point DNS A records towards the
specific server instance of that cluster (e.g. having `1.2.3.4` as IP):

    cluster01.amazing.iot-playground.org        A    1.2.3.4
    *.cluster01.amazing.iot-playground.org      A    1.2.3.4

The setup scripts will fetch the private key from a secret location, during the
setup process. This location is provided during the creation of the server
instance and not checked in to this repository.

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

I can't provide and out-of-the-box setup for that, as you . So here are the steps you
need to do in order to get TLS working:

* Own/register a domain – I have `iot-playground.org` and will use the
  sub-domain `amazing.iot-playground.org` for this purpose.
* Create a wildcard certificate for this using e.g. [acme.sh](https://github.com/Neilpang/acme.sh):
      ./acme.sh --issue -d "amazing.iot-playground.org" -d '*.amazing.iot-playground.org' --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please
  Then enter the DNS TXT records into your DNS setup, and continue with:
      ./acme.sh --issue -d "amazing.iot-playground.org" -d '*.amazing.iot-playground.org' --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please  --renew
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
