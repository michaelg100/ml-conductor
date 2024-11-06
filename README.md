# MLConductor
## ML orchestration tool

![alt text](./logo.png)

## Create Python Environment For Development

### Install Pyenv or Python 3.12.0

Go to [pyenv](https://github.com/pyenv/pyenv)

Once installed you can install python 3.12.0

```
pyenv install 3.12.0

pyenv shell 3.12.0

# or set global for all terminal sessions

pyenv global 3.12.0
```

### Create virtual env for deps

```
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

## Run Unit Tests

```
python manage.py test
```

# Concept
Phase one (current)
- general tool for storing feature data, model metadata, calling models, and logging model responses
- not a goal to host a model, should be indiviudally served with something like TFX (for tensorflow)

Phase two
- kick off training jobs with workers and store off model files

Phase three
- CLI or API to go through typical flow, generate data -> model train -> model register + metrics -> deploy model


Data scientist could essentially upload a yaml for the process
```yaml
model_name: "my linear model"
features:
  - user_table:feature_a
  - user_table:feature_b
  - user_table:feature_c
feature_data_range:
  start: "2024-10-10"
  end: "2024-10-14"
log_params:
  - max_depth: 2
log_metrics:
  - mean_squared_error
training_data: "gcs://here.parquet"
join_key: "user_id"
target_column: "conversion_likelihood"
experiment_tag: "ads rerank"
model_training_script: "file.py"
```