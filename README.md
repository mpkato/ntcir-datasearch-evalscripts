Evaluation Scripts for NTCIR-15 Data Search
===========================================


Pooling: `pooling.py`
-------

This script takes run files to pool the top k documents per query and output query-document pairs.

```
usage: pooling.py [-h] k input_filepaths [input_filepaths ...]

Pooling top k documents per query.

positional arguments:
  k                Depth for pooling. Only the top k documents per query are
                   used.
  input_filepaths  Run files
```

e.g. 
```
% python pooling.py 10 ./runs/KASYS-E-1 ./runs/KASYS-E-2 > pooled_documents_cutoff10.tsv
```
where `KASYS-E-1` and `KASYS-E-2` are run files.

The result should look like:
```
% head ../ntcir15_extra_submissions/pooled_documents_cutoff10.tsv
DS1-E-1001	783c4ba2-3d04-471b-98a9-0551a26247ad
DS1-E-1001	2f48d647-57b3-4f59-a52d-240987a92ae7
DS1-E-1001	34499157-5232-4a8a-8e5b-a21923ddd75b
DS1-E-1001	381afe44-3e5a-4c81-96aa-b00758622399
DS1-E-1001	d926f18a-f7fa-4272-a066-6960f463d2c0
DS1-E-1001	28efe440-e247-43ca-bbfd-ca8341bd38e6
DS1-E-1001	2fe75099-dbcc-4839-a8cb-0084410939da
DS1-E-1001	9a4a0366-f85b-4136-aa7a-d83c66498364
DS1-E-1001	4c0b326f-0a8a-4769-8c28-5d3efc00903f
DS1-E-1001	a1d9f3ae-7880-46f4-9ec9-0b690f5c1011
```



Evaluation of Japanese Runs
-------

The evaluation of Japanese runs consists of the four steps:
- Create a CSV file for Lancers
- Set up a Lancers task
- Upload the CSV file to Lancers and approve/reject workers' results
- Parse the workers' results to obtain qrels


### Create a CSV file: `create_lancers_task.py`

This script generates a CSV file for Lancers based on pooled results and gold standard data.

```
usage: create_lancers_task.py [-h]
                              input_filepath topic_filepath
                              gold_standard_filepath output_filepath

positional arguments:
  input_filepath        TSV file including query-document pairs
  topic_filepath        TSV file including the description for each query
  gold_standard_filepath
                        TSV file including query-document pairs for which the
                        inter-rater agreement is high
  output_filepath
```

`input_filepath` is the result of `pooling.py`. `topic_filepath` is `data_search_e_topics.tsv`,
and `gold_standard_filepath` is `data_search_j_gold_standard.tsv`.
The gold standard file includes query document pairs for which almost perfect agreement was achieved in the past relevance judgments. "Good" workers are expected to judge these query documents pairs correctly.

e.g.
```
% python create_lancers_task.py pooled_documents_cutoff10.tsv data_search_j_topics.tsv data_search_j_gold_standard.tsv data_search_j_rel_judge.csv
```

### Set up a Lancers task

See `README.lancders.md` and `lancers-template.html`.


### Obtain worker's results

Please upload the CSV file and wait for workers' results.
You can approve or reject workers' results at Lancers.
In NTCIR-15 Data Search, we rejected those who worked on three or more tasks,
and failed to correctly answer the gold standard questions for more than 1/3 of tasks.
An answer is considered "wrong" if the answer is 0 and the ground truth is 2,
or the answer is 1 or 2 and the ground truth is 0.
Note that a task consists of 10 questions.
The first question in a task is always a gold standard question,
and its answer is in `known` field of the CSV file.


### Parse the workers' results: `parse_lancers_result.py`

Please download from Lancers a CSV file that contains workers' results.
This file can be parsed by `parse_lancers_result.py`:

```
usage: parse_lancers_result.py [-h] input_filepaths [input_filepaths ...]

Parse a CSV file downloaded from Lancers.

positional arguments:
  input_filepaths  Files downloaded from Lancers
```

The output is whitespace-separated values of the query ID, dataset ID, and scores.
Since some query-document pairs were evaluated more than the others (as every task consists of 9 query-document pairs, some must appear more than once), only the first k scores were used in NTCIR-15 Data Search.

`compute_median.py` can be useful to obtain the median of scores given by multiple assessors:

```
usage: compute_median.py [-h] input_filepath

Compute the relevance grade.

positional arguments:
  input_filepath  File including scores for each query-document pairs
```


e.g.
```
% python parse_lancers_result.py lancers_task_download_data_xxxxxx.csv > qrel_scores.txt
% python compute_median.py qrel_scores.txt > qrels.txt
```


Evaluation of English Runs
-------

The evaluation of English runs consists of the four steps:
- Create a CSV file for Amazon Mechanical Turk (AMT)
- Set up a AMT task
- Upload the CSV file to AMT and approve/reject workers' results
- Parse the workers' results to obtain qrels


### Create a CSV file: `create_amt_task.py`

This script generates a CSV file for AMT based on pooled results and gold standard data.

```
usage: create_amt_task.py [-h]
                          input_filepath topic_filepath
                          gold_standard_filepath output_filepath

positional arguments:
  input_filepath        TSV file including query-document pairs
  topic_filepath        TSV file including the description for each query
  gold_standard_filepath
                        TSV file including query-document pairs for which the
                        inter-rater agreement is high
  output_filepath
```

All the arguments are the same as those for `create_lancers_task.py`.


e.g.
```
% python create_amt_task.py pooled_documents_cutoff10.tsv data_search_e_topics.tsv data_search_e_gold_standard.tsv data_search_e_rel_judge.csv
```

### Set up an AMT task

See `README.AMT.md` and `AMT-template.html`.
Note that we are hosting crawled webpages of data.gov at Amazon S3 temporarily.
They can be found at `https://ntcir-datasearch-en.s3-ap-northeast-1.amazonaws.com/{ID}.html`.
For example, `https://ntcir-datasearch-en.s3-ap-northeast-1.amazonaws.com/34499157-5232-4a8a-8e5b-a21923ddd75b.html`.

### Obtain worker's results

Please upload the CSV file and wait for workers' results.
You can approve or reject workers' results at AMT.
In NTCIR-15 Data Search, we rejected workers by the same criterion as that in Lancers.
Additionally, we rejected those who worked on three or more tasks,
and the average work time ("WorkTimeInSeconds" field) is less than 100 seconds.

### Parse the workers' results: `parse_amt_result.py`

Please download from AMT a CSV file that contains workers' results.
This file can be parsed by `parse_amt_result.py`:

```
usage: parse_amt_result.py [-h] input_filepaths [input_filepaths ...]

Parse a CSV file downloaded from AMT.

positional arguments:
  input_filepaths  Files downloaded from Lancers
```

e.g.
```
% python parse_amt_result.py Batch_xxxxxxx_batch_results > qrel_scores.txt
% python compute_median.py qrel_scores.txt > qrels.txt
```