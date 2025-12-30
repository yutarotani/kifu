##################################################
########　　.bodの読み込み用関数　　　　　########
##################################################
#.bodファイルを必要データの配列に変換
def bod_tolist(filename,humen):
    f = open(filename, 'r')
    line = f.read().split('\n')
    
    #手数
    tesuu = line[-2].split('  ')[0].replace('手数＝','')
    
    #各持ち駒を文字列で抜き出し
    koute_mochigoma = line[0].replace('　','').replace('後手の持駒：','')
    sente_mochigoma = line[-3].replace('　','').replace('先手の持駒：','')
    
    dan = []
    for i in range(3,12):
        D = []
        d = line[i].replace('|','').replace('一','').replace('二','').replace('三','').replace('四','').replace('五','')\
        .replace('六','').replace('七','').replace('八','').replace('九','')
        D.append(d[0:2].replace(' ',''))
        D.append(d[2:4].replace(' ',''))
        D.append(d[4:6].replace(' ',''))
        D.append(d[6:8].replace(' ',''))
        D.append(d[8:10].replace(' ',''))
        D.append(d[10:12].replace(' ',''))
        D.append(d[12:14].replace(' ',''))
        D.append(d[14:16].replace(' ',''))
        D.append(d[16:18].replace(' ',''))
        dan.append(D)
    
    kazu = ['18','17','16','15','14','13','12','11','10','９','８','７','６','５','４','３','２']

    sente_mochigoma_1 = ''
    for i in range(len(sente_mochigoma)):
        if sente_mochigoma[i] in kazu:
            sente_mochigoma_1 += (sente_mochigoma[i+1]+sente_mochigoma[i])
        
        else:
            if sente_mochigoma[i] in sente_mochigoma_1:
                pass
            else:
                sente_mochigoma_1 += sente_mochigoma[i]
    
    sente_mochigoma = sente_mochigoma_1
    
    if sente_mochigoma == '':
         sente_mochigoma = 'なし'
    
    koute_mochigoma_1 = ''
    for i in range(len(koute_mochigoma)):
        if koute_mochigoma[i] in kazu:
            koute_mochigoma_1 += (koute_mochigoma[i+1] + koute_mochigoma[i])
        
        else:
            if koute_mochigoma[i] in koute_mochigoma_1:
                pass
            else:
                koute_mochigoma_1 += koute_mochigoma[i]
    
    koute_mochigoma = koute_mochigoma_1
    
    if koute_mochigoma == '':
        koute_mochigoma = 'なし'

    return [filename,dan,koute_mochigoma,sente_mochigoma,tesuu,humen]