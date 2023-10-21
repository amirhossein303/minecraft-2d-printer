server:
	@echo "Building the minecraft server..."
	docker build . -t minecraft_printer
	@echo "Server just built, to run the server use: 'make run'"

run:
	@echo "Running the minecraft server..."
	docker run --publish="25565:25565" --publish="4711:4711" --rm --name "minecraft_printer" minecraft_printer

exec:
	@echo "executing /bin/bash on cotainer..."
	docker container exec -it minecraft_printer /bin/bash

kill:
	@echo "killing container..."
	docker container kill minecraft_printer

start:
	@echo "starting the container..."
	docker container start minecraft_printer

stop:
	@echo "stoping the container..."
	docker container stop minecraft_printer
