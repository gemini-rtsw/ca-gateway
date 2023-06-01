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

