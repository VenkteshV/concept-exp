pip install git+https://github.com/liaad/keep --timeout=10000
pip install git+https://github.com/boudinfl/pke --timeout=10000
pip install git+https://github.com/LIAAD/yake.git --timeout=10000
python -m nltk.downloader stopwords
python -m spacy download en
python -m spacy download en_core_web_lg

# uncomment build trec_eval not necessary as trec_eval executable is atatched with code and below command moves it to ur /usr/local/bin
# mkdir temp_
# cd temp_
# git clone https://github.com/usnistgov/trec_eval.git
# cd trec_eval
# # replace BIN variable which is path to binary where trec_eval should be installed
# bin_path=$(which pip | sed 's+/pip++g')
# sed -i "s+BIN = /usr/local/bin+BIN = $n+g" Makefile
# make install
# cd ../../
# rm -rf temp_


sudo cp trec_eval /usr/local/bin/
wget --load-cookies /tmp/cookies.txt "https://drive.google.com/u/0/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/u/0/uc?export=download&confirm=r8GA&id=0B6VhzidiLvjSOWdGM0tOX1lUNEk' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=0B6VhzidiLvjSOWdGM0tOX1lUNEk" -O torontobooks_unigrams.bin && rm -rf /tmp/cookies.txt

mv torontobooks_unigrams.bin embedding/

git clone https://github.com/epfml/sent2vec
cd sent2vec
git checkout f827d014a473aa22b2fef28d9e29211d50808d48
make
pip install cython
cd src
python setup.py build_ext
pip install .
cd ../../
rm sent2vec
# install requirements file
pip install -r requirements.txt

cd evaluation
unzip en_kp_list.zip
cd ..
# download models
mkdir data
cd data
wget http://www.ccc.ipt.pt/~ricardo/keep/standalone/data.zip
unzip data.zip
rm data.zip

mkdir Datasets
cd Datasets
wget https://github.com/LIAAD/KeywordExtractor-Datasets/raw/master/datasets/SemEval2017.zip
unzip SemEval2017.zip
rm SemEval2017.zip

wget https://github.com/LIAAD/KeywordExtractor-Datasets/raw/master/datasets/SemEval2010.zip
unzip SemEval2010.zip
rm SemEval2010.zip

wget https://github.com/LIAAD/KeywordExtractor-Datasets/raw/master/datasets/Inspec.zip
unzip Inspec.zip
rm Inspec.zip
cd ../../
unzip KhanAcad.zip
mv KhanAcad data/Datasets/

python train_lda.py
mv KhanAcad_lda.gz data/Models/Unsupervised/lda/
