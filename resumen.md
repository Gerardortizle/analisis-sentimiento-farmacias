# Resultados

| alias                   |   accuracy |   precision_macro |   recall_macro |   f1_macro |   f1_weighted |   recall_NEG |   recall_NEU |   recall_POS |   lat_p50_ms |   lat_p95_ms | cumple_umbrales   |
|:------------------------|-----------:|------------------:|---------------:|-----------:|--------------:|-------------:|-------------:|-------------:|-------------:|-------------:|:------------------|
| M1_RoBERTuito           |      0.8   |             0.785 |          0.829 |      0.797 |         0.804 |        0.953 |        0.789 |        0.744 |        9.639 |       17.765 | True              |
| M2_XLM-R_Twitter        |      0.82  |             0.803 |          0.842 |      0.817 |         0.822 |        0.922 |        0.829 |        0.775 |        9.962 |       13.62  | True              |
| M3_BERT_mult_5estrellas |      0.697 |             0.62  |          0.641 |      0.597 |         0.674 |        0.844 |        0.211 |        0.869 |        9.51  |       11.221 | False             |
| M4_DistilBERT_mult      |      0.61  |             0.513 |          0.513 |      0.486 |         0.587 |        0.531 |        0.145 |        0.862 |        5.157 |        5.705 | False             |

**Modelo recomendado:** M1_RoBERTuito
