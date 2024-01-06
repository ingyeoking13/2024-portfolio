# 2023-portfolio

## system requirements

os: macos
python
- 3.11.6 (should be 3.11.6, above version won't work - dependencies ray)
docker
- redis  
- mysql  
- nginx (for reverse proxy)   
minikube, helm

## 회원가입 및 인증

기능 - 회원가입, 로그인, 로그아웃  
요구사항 - docker(mysql, nginx)   
구현사항 - refresh_token, access_token, jwt

## 처리율 제한 장치

기능 - 처리율 제한 장치
요구사항 - docker(redis), ray(python 3.11.6)
구현사항 - token bucket algorithm

## minikube-start

docker daemon을 활성화 한 후 
```
minikube start

😄  Darwin 13.4.1 의 minikube v1.28.0
🆕  이제 1.25.3 버전의 쿠버네티스를 사용할 수 있습니다. 업그레이드를 원하신다면 다음과 같이 지정하세요: --kubernetes-version=v1.25.3
✨  기존 프로필에 기반하여 docker 드라이버를 사용하는 중
👍  minikube 클러스터의 minikube 컨트롤 플레인 노드를 시작하는 중
🚜  베이스 이미지를 다운받는 중 ...
🔄  Restarting existing docker container for "minikube" ...
🐳  쿠버네티스 v1.23.3 을 Docker 20.10.12 런타임으로 설치하는 중
    ▪ kubelet.housekeeping-interval=5m
🔎  Kubernetes 구성 요소를 확인...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
    ▪ Using image docker.io/kubernetesui/dashboard:v2.7.0
    ▪ Using image docker.io/kubernetesui/metrics-scraper:v1.0.8
🎉  minikube 1.31.2 이 사용가능합니다! 다음 경로에서 다운받으세요: https://github.com/kubernetes/minikube/releases/tag/v1.31.2
💡  해당 알림을 비활성화하려면 다음 명령어를 실행하세요. 'minikube config set WantUpdateNotification false'
💡  Some dashboard features require the metrics-server addon. To enable all features please run:

	minikube addons enable metrics-server	


🌟  애드온 활성화 : storage-provisioner, default-storageclass, dashboard
🏄  끝났습니다! kubectl이 "minikube" 클러스터와 "default" 네임스페이스를 기본적으로 사용하도록 구성되었습니다.
```

minikube 환경변수 등록 
```
eval $(minikube docker-env)
```

도커 이미지 등록 
```
docker build -t fastapi:local -f Dockerfile.backend . 
```

chart로 이동 후 헬름 install  
```
cd charts
helm install webserver fastapi

NAME: webserver
LAST DEPLOYED: Wed Oct 11 17:59:56 2023
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

```
helm list

NAME     	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART        	APP VERSION
webserver	default  	1       	2023-10-11 17:59:56.549788 +0900 KST	deployed	fastapi-0.1.0	1.16.0    

k get po

NAME                                    READY   STATUS    RESTARTS   AGE
webserver-deployment-5795967c76-j92lt   1/1     Running   0          12s
webserver-deployment-5795967c76-m449f   1/1     Running   0          12s

k port-forward webserver-deployment-5795967c76-j92lt 8000:8000

Forwarding from 127.0.0.1:8000 -> 8000
Forwarding from [::1]:8000 -> 8000

curl localhost:8000

{"message":"안녕"}%            
```





