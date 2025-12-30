import re,collections,json
from tqdm import tqdm
import tkinter as tk
import tkinter.messagebox as messagebox

##################################################
########　　.kifの読み込み用関数　　　　　########
##################################################
#.kifファイルを必要データの配列に変換
def kif_tolist(filename,humen=''):
    ###########最初に設定しておくもの##################################
    trans1 = ['１', '２', '３', '４', '５', '６', '７', '８', '９']
    trans2 = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
    koma_moji = ['飛', '角', '金', '銀', '桂', '香', '歩']
    koma_kigo = ['r', 'b', 'g', 's', 'n', 'l', 'p']
    koma_kigo2 = [x.swapcase() for x in koma_kigo] + koma_kigo
    
    def make_sfen(retu):    
        for i in range(9, 0, -1):
            retu = retu.replace('0'*i, str(i))
        return retu
    #################################################################
    
    with open(filename, 'r') as f:
        kifu = f.read()
    
    kifu_1 = kifu.split('\n')
    tesuu = kifu_1[-1].replace('まで','').replace('手で後手の勝ち','')
    
    for x in range(9):
        kifu = kifu.replace(trans1[x], str(x+1))
        kifu = kifu.replace(trans2[x], str(x+1))
    
    kifu = kifu.replace('\u3000', '')
    
    sashite = [x.groups()[0] 
        for x in re.finditer('^\s*[0-9]+\s+(\S+).*$', 
        kifu, 
        flags=re.MULTILINE)]
    
    for x in range(1, len(sashite)):
        if ('同' in sashite[x]):
            sashite[x] = sashite[x].replace('同', sashite[x-1][:2])
    
    if ('投了' in sashite):
        sashite.remove('投了')
    
    #SFENリスト
    sfen = []
    
    #持ち駒
    mochigoma = []
    
    #局面データをlistに変換
    kyokumen = 'lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL'
    sfen.append(kyokumen + ' ' + 'b' + ' ' + '-' + ' ' + '1')
    for i in range(1, 10):
        kyokumen = kyokumen.replace(str(i), '0'*i)
    
    kyokumen = [list(x) for x in kyokumen.split('/')]
    
    #駒を動かす
    for i, each_sashite in enumerate(sashite):
        #駒を動かすときの処理
        if each_sashite[-1] != '打': 
            move = re.match('^(\d+)(\D+)\((\d+).*$', each_sashite).groups()
            after_x = 9 - int(move[0][0])
            after_y = int(move[0][1]) - 1 
            before_x = 9 - int(move[2][0])
            before_y = int(move[2][1]) - 1
            active_koma = kyokumen[before_y][before_x]
            #移動元は空きになる
            kyokumen[before_y][before_x] = '0'
            #「成」ならば「+」をつける
            if move[1][-1] == '成':
                active_koma = '+' + active_koma
            #移動先に駒があれば持ち駒とする
            #大文字、小文字は入れ替える必要がある
            if kyokumen[after_y][after_x] != '0':
                mochigoma.append(kyokumen[after_y][after_x][-1].swapcase())
            #移動先に駒をセットする
            kyokumen[after_y][after_x] = active_koma
        
        #駒を打つときの処理
        else: 
            after_x = 9 - int(each_sashite[0])
            after_y = int(each_sashite[1]) -1
            active_koma = koma_kigo[koma_moji.index(each_sashite[2])]
            if i % 2 == 0: #先手が駒を打つ
                active_koma = active_koma.upper()
            kyokumen[after_y][after_x] = active_koma
            mochigoma.remove(active_koma)
        
        #SFENリストに保存    
        mochigoma_dict = collections.Counter(''.join(mochigoma))
        sfen_mochigoma = ''
        for x in koma_kigo2:
            if mochigoma_dict[x] == 1:
                sfen_mochigoma += x
            elif mochigoma_dict[x] > 1:
                sfen_mochigoma += (str(mochigoma_dict[x]) + x)
        if sfen_mochigoma =='':
            sfen_mochigoma = '-'
        sfen.append('/'.join([make_sfen(''.join(x)) for x in kyokumen]) 
                + ' ' + ('w' if i % 2 == 0 else 'b')
                + ' ' + sfen_mochigoma 
                + ' ' + str(i + 2))
    

    #設定フォルダから盤面の駒・持ち駒の書き換えデータを引っ張る
    with open(r'設定\駒設定.txt','r') as r:
        for line in r:
            koma_convert = json.loads(line)
    
    with open(r'設定\持ち駒設定.txt','r') as r:
        for line in r:
            mochigoma_convert = json.loads(line)
    
    if humen == '':
        all_sfen = [x.strip() for x in sfen]
    
    else:
        humen = int(humen.replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４').replace('5','５')\
                  .replace('6','６').replace('7','７').replace('8','８').replace('9','９')) + 1
        
        all_sfen = []
        
        for N in range(humen):
            all_sfen.append(sfen[N])
    
    
    for line_num, sfen in tqdm(enumerate(all_sfen)):
        sfen_split = sfen.split(' ')
        kyokumen = sfen_split[0]
        teban = sfen_split[1]
        mochigoma = sfen_split[2]
        
        for i in range(1, 10):
            kyokumen = kyokumen.replace(str(i), '0' * i)
        
        for key, value in koma_convert.items():
            kyokumen = kyokumen.replace(key, value)
        
        each_lines = [('|' + each_line + '|') for each_line in kyokumen.split('/')]
        mochigoma_sente = []
        mochigoma_gote = []
        
        while len(mochigoma) > 0:
            if mochigoma == '-' or mochigoma == '':
                mochigoma = ''
            m_1 = re.match(r'([0-9]+)([a-z|A-Z])', mochigoma)
            
            if(m_1 != None):
                if(m_1.group().isupper()):
                    mochigoma_sente.append(''.join(m_1.groups()))#[::-1]))
                else:
                    mochigoma_gote.append(''.join(m_1.groups()))#[::-1]))
                mochigoma = mochigoma.replace(m_1.group(), '')
            
            else:
                pass
            m = re.match(r'[a-z|A-Z]', mochigoma)
            
            if(m != None):
                if(m.group().isupper()):
                    mochigoma_sente.append(m.group())
                else:
                    mochigoma_gote.append(m.group())
                mochigoma = mochigoma.replace(m.group(), '')
            
            else:
                pass
        
        sente_string = ''.join(mochigoma_sente)
        gote_string = ''.join(mochigoma_gote)
        
        for key, value in mochigoma_convert.items():
            sente_string = sente_string.replace(key, value)
            gote_string = gote_string.replace(key, value)
    
    kazu = ['18','17','16','15','14','13','12','11','10','９','８','７','６','５','４','３','２']
    
    sente_string_1 = ''
    for i in range(len(sente_string)):
        if sente_string[i] in kazu:
            sente_string_1 += (sente_string[i+1] + sente_string[i])
        else:
            if sente_string[i] in sente_string_1:
                pass
            else:
                sente_string_1 += sente_string[i]
    
    sente_string = sente_string_1
    
    if sente_string == '':
        sente_string = 'なし'
    
    gote_string_1 = ''
    for i in range(len(gote_string)):
        if gote_string[i] in kazu:
            gote_string_1 += (gote_string[i+1]+gote_string[i])
        
        else:
            if gote_string[i] in gote_string_1:
                pass
            else:
                gote_string_1 += gote_string[i]
    
    gote_string = gote_string_1
    
    if gote_string == '':
        gote_string = 'なし'
    
    dan = []
    for l in range(len(each_lines)):
        D = []
        d = each_lines[l].replace('|','')
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

    try:
        return [filename,dan,gote_string,sente_string,tesuu,humen - 1]
    except TypeError:
        tk.Tk().withdraw()
        messagebox.showinfo('エラー', '何手目かが入力されていません')
