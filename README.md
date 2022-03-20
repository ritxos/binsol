## __Files Structure__
- ./solution.py : Contains the python implementation
- ./Dockerfile : Dockerfile to build docker image in order to run using docker 

## __Running solution as docker container__
__Requirements:__
- docker

__Steps to Run:__
```
docker build -t binsol .
docker run -p 8080:8080 --name binsol binsol
```
__Output:__
- After container is running output can be observed using:
 ``` 
docker logs binsol -f
```
- Exported metrics can be observed using:
```
curl http://localhost:8080/
```
## __Running solution as python program__
__Requirements:__
- python 3.9
- pip

__Steps to Run:__
```
pip install prometheus_client  binance-connector
python ./solution.py
```

__Output:__
- Program displays output on stdout
- Exported metrics can be observed using:
```
curl http://localhost:8080/
```