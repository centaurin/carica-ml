# Carica ML

This repository contains:

- **Kaggle's** notebook that process and train the AI model
- A simple **Flask** server to import and use the model to evaluate the pictures.

## 1. CI/CD using Docker

This repository has a Dockerfile. Whenever a tag is pushed, a **GitHub Workflow** will be triggered to build and publish the docker image.

The image is then pulled by a Docker compose file and deployed automatically.

For futher details about the CI/CD, please refer to [Carica Kestra](https://github.com/centaurin/carica-kestra).

The model in this repository is trained on [Kaggle](kaggle.com). However, due to the time limitation and **Kaggle API** being not too user-friendly, I wasn't managed to automate the entire workflow by pulling the model automatically. As such, the notebook is saved by **Kaggle**, but the model is manually downloaded and uploaded.

## 2. The AI model

This **README** only provided basic information about the datasets and model. For further details, please refer to the [Python notebook](./indian-fruit.ipynb).

### 2.1 The dataset

This model is trained on the dataset [FruitNet dataset](https://www.kaggle.com/datasets/shashwatwork/fruitnet-indian-fruits-dataset-with-quality). This dataset is extracted from multiple videos of fruits, serving the purpose of classifying fruits and their freshness.

This kind of data is easy to create with sufficient time and effort. However, due to the time limit of the contest, the dataset is used as it is, with some preprocessing steps documented in the notebook.

### 2.2 Training and the resulting model

With limited time, data and computing power, it is impossible to fine-tune a model from the scratch. As such, we are using a pre-trained VGG16 model as a starting point. For the detailed training process, please refer to the [Python notebook](./indian-fruit.ipynb).

The resulting model achieve an average F1-score of 98. The model is then used to evaluate users' pictures.
