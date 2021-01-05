container:
	- kubectl delete -f k8s/geoip-http.yaml
	- kubectl create -f k8s/geoip-http.yaml

config:
	- kubectl delete configmap geoip-py -n osg-services
	- kubectl create configmap geoip-py --from-file=geoip.py -n osg-services

ing:
	- kubectl delete -f k8s/geoip-ing.yaml
	- kubectl create -f k8s/geoip-ing.yaml
