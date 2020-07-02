This repository is heavily derived and insipred from https://github.com/AnzorGozalishvili/unsupervised_keyword_extraction and is given proper credits in paper. We impement the proposed algorithm using this setup and reuse existing code for other bselines with modifications to pre processing alone.

UI file upload component is adapted from https://github.com/LukasMarx/react-file-upload

# unsupervised_keyword_extraction
Using BERT pre-trained model embeddings for [EmbedRank](https://github.com/swisscom/ai-research-keyphrase-extraction) for unsupervised keyword extraction.


###  Create environment
create conda environment with python 3.7 version
```bash
conda create -n unsupervised_keyword_extraction -y python=3.7 ipython
```

Activate environment
```bash
conda activate unsupervised_keyword_extraction
```

Install requirements it will prompt for password as a command for moving trec_eval to usr/local/bin requires sudo
Most setup for running the project is covered here, those that are not covered are listed below with prefix "Mandatory step"
```bash
sh install_dependencies.sh

export LD_LIBRARY_PATH=/home/venktesh/anaconda3/envs/unsupervised_keyword_extraction/lib

```
The above script install dependencies downloads datasets 
and trains LDA on datasets.

# Installation for running EmbedRank

Kindly install java (openjdk8-jre) for running stanford tagger.
## Local Installation

1. Mandatory step -  Download full Stanford CoreNLP Tagger version 3.8.0.
http://nlp.stanford.edu/software/stanford-corenlp-full-2018-02-27.zip (needed to reproduce EmbedRank's original paper results)




2.  Mandatory step - Launch Stanford Core NLP tagger
    * Open a new terminal
    * Go to the stanford-core-nlp-full directory
    * Run the server `java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -preload tokenize,ssplit,pos -status_port 9000 -port 9000 -timeout 15000 & `

3.Not Mandatory -  Trec_eval is used for performance evaluation and attached with code run command. This has been done in install_dependencies.sh but requires password input when running install_dependencies.sh please run below command only if it throws error.
   sudo cp trec_eval /usr/local/bin/ for the same.

4. Note: KhanAcad.zip is the dataset attached as part of code itself to enable easy automation. it is unzipped and moved to appropriate directory through script in install_dependencies.sh.

5. Not mandatory - This step has been automated in install_dependencies.sh, but if it doesn't work kindly follow the below steps
to run EmbedRank. Not the below are dependencies only for embedrank. Rest of the variants of embedrank can be run without sent2vec
 Install sent2vec from 
https://github.com/epfml/sent2vec
    * Clone/Download the directory
    * go to sent2vec directory
    * git checkout f827d014a473aa22b2fef28d9e29211d50808d48
    * make
    * pip install cython
    * inside the src folder 
        * ``python setup.py build_ext``
        * ``pip install . ``
        * (In OSX) If the setup.py throws an **error** (ignore warnings), open setup.py and add '-stdlib=libc++' in the compile_opts list.        
    * Download a pre-trained model (see readme of Sent2Vec repo). The experiments were carried out with torontobooks_unigrams.bin .

### FOr  Evaluation
please run install_dependencies.sh before running this and also bring up standford nlp tagger
You can evaluate any  model on many different datasets using script below. See [here](run_evaluation.py) for more details. 
```bash
python -m run_evaluation
```
At any point of running the evaluation you can look into data/Keywords/NameOfAlgorithm/NameOfDataSet/ to see the 
keyphrase or concepts extracted for each document
For instance if you are running EmbedRank on SemEval2017 dataset
you can look into 
data/Keywords/EmbedRank/SemEval2017/

After evaluation finishes you can see the metrics in console and in csv format where file name is of form "results-{DatasetName}.csv"
The previous results arrived at after conducting experiments can be seen in Previous_results folder

### For visualizing fine grained concepts tagged to khan academy video transcripts
run  python concept_extracton_demo.py
you must be able to see a file named "results-khanacad.html"
in the directory.Open it in browser of choice to see concepts extracted.
Substitute any tex in the code to get fine grained concepts tagged to it.

###Notebooks:
The set of experiments to decide the embeddings method to use is present as a notebook under directory notebooks and includes umap visualizations and metrics calculated which shows a clear advantage of our novel representation mechanism.

unzip initial_research_data.csv.zip uploaded as data in portal in notebooks directory before running notebook  . It contains both data and notebooks . The zip file is part of directory.

## References

https://github.com/liaad/keep

https://github.com/LIAAD/KeywordExtractor-Datasets

https://spacy.io/usage/linguistic-features

https://github.com/usnistgov/trec_eval
https://github.com/AnzorGozalishvili/unsupervised_keyword_extraction
(https://github.com/swisscom/ai-research-keyphrase-extraction)
