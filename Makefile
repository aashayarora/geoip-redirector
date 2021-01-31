container:
	- kubectl delete -f http/k8s/geoip.yaml
	- kubectl create -f http/k8s/geoip.yaml
	- kubectl delete -f https/k8s/geoip.yaml
	- kubectl create -f https/k8s/geoip.yaml

httpconf:
	- kubectl delete configmap geoip-http -n osg-services
	- kubectl create configmap geoip-http \
	  --from-file=http/FlaskApp/__init__.py \
	  --from-file=http/FlaskApp/geoip.wsgi \
	  --from-file=http/FlaskApp/geoip.conf -n osg-services

httpsconf:
	- kubectl delete configmap geoip-https -n osg-services
	- kubectl create configmap geoip-https \
	  --from-file=https/FlaskApp/__init__.py \
	  --from-file=https/FlaskApp/geoip.wsgi \
	  --from-file=https/FlaskApp/geoip.conf -n osg-services

svc:
	- kubectl delete -f http/k8s/svc.yaml
	- kubectl create -f http/k8s/svc.yaml
	- kubectl delete -f https/k8s/svc.yaml
	- kubectl create -f https/k8s/svc.yaml

ing:
	- kubectl delete -f http/k8s/ing.yaml
	- kubectl create -f http/k8s/ing.yaml
	- kubectl delete -f https/k8s/ing.yaml
	- kubectl create -f https/k8s/ing.yaml
