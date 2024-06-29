run:
	docker run -it -d --env-file .env --restart=unless-stopped --name llama_bot llama_bot_image
stop:
	docker stop easy_refer
attach:
	docker attach easy_refer
dell:
	docker rm easy_refer