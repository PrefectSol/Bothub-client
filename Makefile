hcreate:
	@python scripts/create_host.py $(filter-out $@,$(MAKECMDGOALS))

hdelete:
	@python scripts/delete_host.py $(filter-out $@,$(MAKECMDGOALS))

post:
	@python scripts/post_bot.py $(filter-out $@,$(MAKECMDGOALS))

view:
	@python scripts/view.py $(filter-out $@,$(MAKECMDGOALS))

auth:
	@python scripts/create_client.py $(filter-out $@,$(MAKECMDGOALS))

deauth:
	@python scripts/delete_client.py $(filter-out $@,$(MAKECMDGOALS))

clear:
	@python scripts/clear.py

%:
	@:
