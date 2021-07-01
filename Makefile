delete-http:
	- kubectl delete -k ./http/
create-http:
	- kubectl apply -k ./http/
delete-https:
	- kubectl delete -k ./https/
create-https:
	- kubectl apply -k ./https/
