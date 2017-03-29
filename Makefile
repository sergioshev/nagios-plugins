PLUGINS_FILES=\
  checkdate_zem800.py \
  check_authlog \
  check_bacula_db_size \
  check_cert_expire \
  check_disk_proxy \
  check_laridae_db_size \
  check_os_sem \
  check_raid \
  check_ups_itemp \
  check_dns_soa \
  check_disk_inodes

PLUGINS_DIR=/usr/lib/nagios/plugins

.PHONY: install
install:
	install -m 755 $(PLUGINS_FILES) $(PLUGINS_DIR)


.PHONY: uninstall
uninstall:
	rm -f $(foreach p, $(PLUGINS_FILES), $(PLUGINS_DIR)/$p)
