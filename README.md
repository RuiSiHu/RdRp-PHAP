# RdRp-PHAP
RdRp-PHAP is a machine learning tool designed to identify the zoonotic potential of unclassified viruses based on the given viral RdRp protein sequences.

# 1.Description
The RdRp (RNA-dependent RNA polymerase) protein is a pivotal enzyme in viral replication, facilitating RNA synthesis. Its high conservation throughout viral evolution underscores its indispensable role in viral survival. RdRp's conservation is instrumental in discerning zoonotic viruses, capable of interspecies transmission, from non-zoonotic ones confined to specific hosts. Variations in RdRp sequences provide critical insights for distinguishing these viruses, offering valuable molecular perspectives for prevention and treatment strategies.<br>
<p>
The predictive tool RdRp-PHAP was developed using a Stacking-based ensemble of seven machine learning classifiers (KNN, GBC, GNB, SVM, RF and LGBM), integrating hybrid features from deep representation learning (BERT and BiLSTM) and classic sequence features (DDE and DPC). RdRp-PHAP holds promise for advancing computational methodologies in virology. Based on sequence length analyses across three datasets (training, testing, and blind), we recommend its application for predicting protein sequences within the length range of 40 to 4000 residues.

# 2.Requirements
Users can download RdRp-PHAP to the local machine and build the environment using conda. <br>
For example:

    conda create -n env_name python=3.7

Please note that the Python version in this environment must be 3.7. Then, use pip install -r requirements.txt to install the corresponding versions of the tools.

    pip install -r requirements.txt

For users in China, it is recommended to use the following command to speed up the installation process.

    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
A list of requirements as following: 

    python==3.7
    biopython==1.81
    numpy==1.21.6
    pandas==1.3.5
    lightgbm==4.3.0
    rich==13.7.1
    joblib==1.3.2
    scikit-learn==1.0.2
    scipy==1.7.3
    tape-proteins==0.5
    torch==1.3.0

# 3.Running
***Note***: please download the '*BiLSTM_embed.model*' from [***here***](https://huggingface.co/huruisi/BiLSTM_embed/tree/main) or (https://huggingface.co/huruisi/BiLSTM_embed/tree/main) and place it in the root directory named "**Models**".

Change the working directory to RdRp-PHAP-main.py, then execute the following command:

    python3 RdRp-PHAP-main.py -i RdRp_test.fasta -o Prediction_results.csv
The default file of output is Prediction_results.csv.

**Where**:
    -i: specifies the input file in FASTA format
    -o: specifies the output file name, defaulting to 'Prediction_results.csv'

***Note***: please ensure that the input FASTA file contains no non-amino acid characters. If there are any, please use *convert2X.py* to convert them using the command:

    python3 convert2X.py -i input.fasta -o output.fasta
    
# 3.Results
The default output file is Prediction_results.csv, as shown in the figure below that it contains three columns. The first column is the sequence name, the second column is the predicted zoonotic infection potential, and the third column is the predicted probability.
![image](https://github.com/RuiSiHu/RdRp-PHAP/blob/main/IMG.png)

Please contact grishu0707(at)gmail.com.
