build:
	@docker build -t grats-back .

run: build
	@docker run -d -p 8000:8000 --name grats-back-container --env-file .env grats-back

stop:
	@docker stop grats-back-container || true
	@docker rm grats-back-container || true

restart: stop run
