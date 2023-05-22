#!/bin/sh

/gem_base/bin/gateway -pvlist /gem_base/etc/rtconfig/cagateway/GATEWAY.pvlist \
                      -access /gem_base/etc/rtconfig/cagateway/GATEWAY.access \
                      -log /var/log/ca-gateway/tcsgateway.log \
                      -prefix tcsgate -archive -no_cache -debug 1 \
                      -cip ${CA_IP} -report /var/log/ca-gateway/gateway.txt -prefix gateway

