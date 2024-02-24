docker tag lazebot us-west1-docker.pkg.dev/lazebot/docker/lazebot
docker push us-west1-docker.pkg.dev/lazebot/docker/lazebot
kubectl rollout restart deployment lazebot