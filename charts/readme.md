
# helm 시작하기 문서 
https://helm.sh/ko/docs/chart_template_guide/getting_started/



```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-deployment
spec:
    replicas: 2
    selector:
        matchLabels:
            app: fastapi
    template:
        metadata:
            labels:
                app: fastapi
        spec:
            containers:
            - name: fastapi-container
              image: pyt:latest
              ports:
              - containerPort: 8000

```

gaelim@jeong-yohan-ui-macBook-Pro charts (feature/backend ✗)]$ helm install gealim fastapi
NAME: gealim
LAST DEPLOYED: Sat Oct  7 18:32:10 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None

➜ gaelim@jeong-yohan-ui-macBook-Pro  ~/Project/kmong  helm list
NAME  	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART        	APP VERSION
gealim	default  	1       	2023-10-07 18:32:10.062224 +0900 KST	deployed	fastapi-0.1.0	1.16.0     
➜ gaelim@jeong-yohan-ui-macBook-Pro  ~/Project/kmong  k get po
NAME                                READY   STATUS         RESTARTS   AGE
gealim-deployment-b6c6499fc-rkkpd   0/1     ErrImagePull   0          10s
gealim-deployment-b6c6499fc-tvl8w   0/1     ErrImagePull   0          10s


2023 10.07~ 10.08
image pull 에러가 나서 살펴보다 로컬호스트에 있는 이미지를 가져오지 못해 
:latest 태그 대신 :local을 써봤다. :latest는 자동으로 docker hub에 간다는 stack overflow 글을 봤기 때문이다.
하지만 되지 않아, 어쩔 수 없이 로컬에서 docker registry:2 를 설치하여 Private repository를 만들려고 하였는데, 
만드는 건 성공하였다. 
이 때 repository에 어떤 이미지가 있는지 몰라 docker registry frontend 이미지도 설치하여 사용해보려고 했는데, (이때 까지 되는 줄알았다. ) 
registry에 이미지를 푸시하려 하니 계속 안되어 인증 정보를 업데이트 ㅇ해줬어야하는데 살펴본게 많았다. 

https://setyourmindpark.github.io/2018/02/06/docker/docker-4/
https://docs.docker.com/registry/deploying/
https://medium.com/@ManagedKube/docker-registry-2-setup-with-tls-basic-auth-and-persistent-data-8b98a2a73eec
https://hub.docker.com/_/httpd

가까스로 docker login localhost:6000 (레지스트리에 로그인) 및 이미지 푸시도 성공하였으나,  
curl localhost:6000/v2/_catalog 로 어떤 이미지가 올라가있는지 확인하려니 Http to https 에러가 발생하여 .... 
다시 생각을 더듬어보니, helm, minikube 인데 왜 안될까 ... 

minikube docker-env 로 설정한 후 도커 이미지를 빌드해야한다는 걸 알았다 ... 세상에 
얼른 $eval (minikube docker-env) 를 한 후, docker build -t pyt:local -f Dockerfile.backend . 수행하니 이제서야 빌드되는게 달라졌다.
그 후 helm install gaelim fastapi ... 완료 
k port-forward [podname] localport:containerport 하니까 된다. 

끝

기록 하지 않으면 기억하지 못할 것 같아 기록한다.
