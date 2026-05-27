# Jenkins ML pipeline

Лабораторная работа: автоматизация ML-проекта через Jenkins.

Проект включает:

- сбор данных из GitHub;
- подготовку датасета;
- обучение модели;
- сохранение модели в `pickle`/`joblib`;
- разворачивание модели в FastAPI-сервис;
- тестовое обращение к сервису.

## Структура

```text
.
├── Jenkinsfile             # декларативный Jenkins pipeline
├── download_data.py        # сбор данных
├── prepare_dataset.py      # очистка и train/test split
├── train_model.py          # обучение модели и сохранение артефактов
├── app.py                  # FastAPI-сервис модели
├── test_service.py         # тестовое обращение к модели
├── sample_request.json     # пример входных данных
├── requirements.txt
└── run_pipeline_local.sh   # локальный запуск без Jenkins
```

## Локальная проверка на Linux VM

```bash
cd Jenkins
bash run_pipeline_local.sh
```

После запуска сервис доступен:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

Тестовый запрос:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  --data @sample_request.json
```

## Jenkins

1. Создать Pipeline job.
2. В настройках выбрать Pipeline script from SCM или вставить содержимое `Jenkinsfile` в поле Pipeline script.
3. Запустить `Build Now`.
4. Проверить Console Output: этапы `Setup`, `Download Data`, `Prepare Dataset`, `Train Model`, `Deploy Service`, `Test Service` должны завершиться успешно.

## Артефакты

После успешного запуска появляются:

- `data/raw/cars_raw.csv`
- `data/processed/cars_clean.csv`
- `data/processed/train.csv`
- `data/processed/test.csv`
- `models/cars_price_model.pkl`
- `models/metrics.json`
- `service.log`

## Что показать в отчете

1. Jenkins job / Pipeline stages.
2. Console Output с успешным прохождением всех этапов.
3. Содержимое `Jenkinsfile`.
4. Скриншот артефактов модели (`models/cars_price_model.pkl`, `models/metrics.json`).
5. Запущенный FastAPI-сервис (`/docs` или `/health`).
6. Тестовое обращение к `/predict` и JSON-ответ с `predicted_price_euro`.
