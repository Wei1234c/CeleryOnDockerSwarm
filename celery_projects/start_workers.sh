# ./start_workers.sh

echo "Starting Celery cluster containers _________________________________________________"

eval $(docker-machine env --swarm master01)

PROJECT=$1  # project 名稱
WORKER_START_ID=$2  # worker container 編號 第一個
WORKER_LAST_ID=$3  # worker container 編號 最後一個
CONCURRENCY=$4  # 每個 worker 可以有幾個 subprocesses

for (( i=${WORKER_START_ID}; i<=${WORKER_LAST_ID}; i=i+1 ))
do
  docker run -d --name=${PROJECT}_celery${i} --hostname=${PROJECT}_celery${i} --net=mynet --volume=/data/celery_projects:/celery_projects wei1234c/celery_armv7 /bin/sh -c "cd /celery_projects && celery -A ${PROJECT} worker -n worker${i}.%h --concurrency=${CONCURRENCY} --loglevel=INFO"
done

