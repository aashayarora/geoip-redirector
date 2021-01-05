container:
	- kubectl delete -f k8s/geoip-http.yaml
	- kubectl create -f k8s/geoip-http.yaml

conf:
	- kubectl delete configmap geoip-app -n osg-services
	- kubectl create configmap geoip-app \
	  --from-file=FlaskApp/__init__.py \
	  --from-file=FlaskApp/geoip.wsgi \
	  --from-file=FlaskApp/geoip.conf -n osg-services

ing:
	- kubectl delete -f k8s/geoip-ing.yaml
	- kubectl create -f k8s/geoip-ing.yaml
