# DNS setup

By default this setup can run with `nip.io` and doesn't require any specific DNS setup.

However, sometimes it may be fun to have a proper DNS name, or when you want to have a publicly
trusted wilcard certificate using Let's Encrypt, then you will need a proper DNS setup.

In a nutshell, you will need to DNS records. Resolving `your.cluster.cloud` and `*.your.cluster.cloud`,
both pointing to the public IP of the server instance.

The easiest thing to do is to create two "A" records, assuming that your IP address is `1.2.3.4`:

      your.cluster.cloud    A   1.2.3.4
    *.your.cluster.cloud    A   1.2.3.4

This will direct the OpenShift Web UI, the API and all the service routes to the correct server instance.

This setup can do this automatically after the new instance has been created. It will use the public
IP, and call the `set_dns_record.lexicon` script if the `BASE_DOMAIN` variable is set in the configuration.

## Lexicon DNS API

This script uses the [lexicon DNS API](https://github.com/AnalogJ/lexicon). Which also requires you to:

1. Install Lexicon – using e.g. `pip install dns-lexicon`
1. Set the `PROVIDER` variable to the proper lexicon provider
1. Set any `LEXICON_<PROVIDER>_*` variables in the config file as well

## Other DNS APIs

If your DNS setup isn't covered by Lexicon, then you always create your own DNS API, or fall back
the "manual" provider.

You can switch the DNS provider of this script by setting the variable `DNS_MODE` in the configuration. Use
`DNS_MODE=manual` to switch to manual processing. The script which gets called will
be `set_dns_record.$DNS_MODE`, so if you provide your own script, you will of course need to provide this script
as well.