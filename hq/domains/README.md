
## About

The Domains app is a report on internet domains that we are responsible
for. The report is simple table with links to Whois records.

The expiration dates are taken from Whois records so do not require manual management.

The Whois records are updated regularly (e.g. daily cron). Sometimes the
Whois server queries fail so you may see some records that older than
the last update cycle. You can wait for the next cycle or manually
update them via the `update` link on the whois record page.

Domains are added to the app database via https://hq.apidb.org/admin/domains/domain/

Registrar and Registrant are manually managed rather than scrapped from
whois records because the whois records are not always the best
(e.g. domains at Namecheap are listed as registrar:eNom in whois).


## ToDo

#### Sortable domain table


#### Improve on whois update task scheduling

RQ-scheduler is used to queue tasks to update Whois records on a regular
basis. We need to keep the process asynchronous because the update
process can be slow and hitting the whois servers too frequently can
result in them blocking us.

The problem is that the tasks are loaded by AppConfig.ready() and
ready() is invoked anytime `python manage.py` is run. Also,
adding/removing domains from the database currently requires running
`python manage.py` to update the scheduler. Also, stopping the app does
not remove tasks from the scheduler (that's not too bad but it deviates
from the idea of shutting down the app for maintenance also stops the
associated tasks).

To summarize:

  - don't do scheduling in AppConfig.ready()
    - probably do it in the startup shell script.
  - unschedule tasks when app is stopped
  - do add/remove from scheduler when adding/removing domains from the database

#### Color highlight soon to expire domains

In the domain table, visibly highlight rows for domains that are close
to expiration (say, yellow for 1-2 months (gives time to ensure $$ is in
the auto-renew account or to remind external registrants), red for < 1
month).

