#!/bin/bash
masses=(220 240 260 280 300 350 400)
folder=${CMSSW_BASE}/src/AZh/combine/HIG-18-023/datacards
cd ${folder}
for mass in ${masses[@]}
do
    combineCards.py MMTT/Aconstr_HsvFit90/AZH${mass}/SR.card.txt MMMT/Aconstr_HsvFit90/AZH${mass}/SR.card.txt MMET/Aconstr_HsvFit90/AZH${mass}/SR.card.txt MMEM/Aconstr_HsvFit90/AZH${mass}/SR.card.txt EETT/Aconstr_HsvFit90/AZH${mass}/SR.card.txt EEMT/Aconstr_HsvFit90/AZH${mass}/SR.card.txt EEET/Aconstr_HsvFit90/AZH${mass}/SR.card.txt EEEM/Aconstr_HsvFit90/AZH${mass}/SR.card.txt > AZH${mass}.txt
done
cd -
