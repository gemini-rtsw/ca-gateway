# Channel Access PV Gateway 

This is a wrapper project for the purpose of integrating upstream
CA Gateway [sources](https://github.com/epics-extensions/ca-gateway)
with Gemini-specific configuration and startup files.

It is advised for the installed product to check the TCS_IP configurations
in /gem_base/epics/ioc/ca-gateway/etc/tcs-ip.conf.

# Usage

The CA Gateway is put into a procserv instance and managed as systemd service.
The commands to manage `procserv-ca-gateway.service` are the typical ones
like
```
systemctl [stop|start|status] procserv-ca-gateway.service
```
or
```
journalctl -f -u procserv-ca-gateway.service
```

# Variations

## GN (Gemini North)
Gemini North has been using a new gateway configuration that does not require a second gateway for the TCS to talk to the older Epics instruments. Instead, we are using a softTCS with the `$TOP` set to `tcv` the accompanying service file, access file, and pvlist file are located in this repo at `etc/gn`. This new service file has not been added to the spec file yet so you will have to manually install it. Once we decide if we want to adopt this new gateway configuraion, then we can add it to be auto installed with the spec file at a later time.

The major difference in our service file is the way the `-cip` argument is used, it must contain the IP addresses of all the systems that are using the gateway, the `-cip` argument sets the environment variables EPICS_CA_AUTO_LIST=NO and EPICS_CA_ADDR_LIST
