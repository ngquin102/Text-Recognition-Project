docker build -t quynh_app .
docker run -it --rm --net=host -P -d --name quynh_app_test quynh_app python a.py