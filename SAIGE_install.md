## SAIGE chrX

##conda create -n saige0.42 -c conda-forge -c bioconda -y r-base=4.0 r-saige=0.42 savvy=1.3.0

conda activate saige0.42

#use the following in scripts

library(SAIGE, lib.loc="~/anaconda3/envs/saige0.42/lib/R/library")

## SAIGE (latest)
conda create -n saige -c conda-forge -c bioconda "r-base>=4.0" r-saige

conda activate saige

OR

conda env create -f environment-RSAIGE.yml

conda activate RSAIGE

FLAGPATH=`which python | sed 's|/bin/python$||'`

export LDFLAGS="-L${FLAGPATH}/lib"

export CPPFLAGS="-I${FLAGPATH}/include"

devtools::install_github("leeshawn/MetaSKAT") #in R

src_branch=master

repo_src_url=https://github.com/weizhouUMICH/SAIGE

git clone --depth 1 -b $src_branch $repo_src_url

R CMD INSTALL --library=path_to_final_SAIGE_library SAIGE
  
