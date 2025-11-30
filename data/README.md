Aby pobrać dataset uruchom komende: 
```bash
curl -L -o data/fake-news-classification.zip \
  "https://www.kaggle.com/api/v1/datasets/download/saurabhshahane/fake-news-classification"
```
Nastepnie rozpakuj dataset

```bash
unzip -o data/fake-news-classification.zip -d data
```

Usun archiwum 

```bash
rm data/fake-news-classification.zip
```