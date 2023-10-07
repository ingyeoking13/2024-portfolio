
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