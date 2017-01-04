
## About

This app reports on Oracle databases.

Each Oracle server runs a cron job every 6 hours that registers its
current databases in to an LDAP directory. This app provides a tabular
report of that data. The app is read only, it does not provide any means
to modify the source records.

See https://wiki.apidb.org/index.php/lsnrsrvcimpt for details on how the
databases are registered and caveats involved.

## Development

The production LDAP directory that this app queries is behind a firewall
so you will need to set up VPN when doing development outside the fw.

## ToDo
