This application predicts highway-mpg of a vehicle based on its curb-weight.
[Automobile](https://archive.ics.uci.edu/dataset/10/automobile) dataset is used to train a super simple ML model.
Localstack is used to mimic AWS. 

Commands to train the model and upload it to localstack:
```
git clone https://github.com/gsenseless/mlOps_wrap
cd mlOps_wrap
docker compose up --force-recreate
```
Command to make a prediction:
```
docker compose run --service-ports predictor --curb_weight=1601
```
1601 can be changed to any number.
