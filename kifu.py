##################################################
########　　必要ライブラリの読み込み　　　########
##################################################
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import re,collections,json
from tqdm import tqdm


##################################################
########　　.bodの読み込み用関数　　　　　########
##################################################
#.bodファイルを必要データの配列に変換
def bod_tolist(filename,humen):
    f = open(filename, 'r')
    line=f.read().split('\n')
    #手数
    tesuu=line[-2].split('  ')[0].replace('手数＝','')
    #各持ち駒を文字列で抜き出し
    koute_mochigoma=line[0].replace('　','').replace('後手の持駒：','')
    sente_mochigoma=line[-3].replace('　','').replace('先手の持駒：','')
    dan=[]
    for i in range(3,12):
        D=[]
        d=line[i].replace('|','').replace('一','').replace('二','').replace('三','').replace('四','').replace('五','')\
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
        
    kazu=['18','17','16','15','14','13','12','11','10','９','８','７','６','５','４','３','２']

    sente_mochigoma_1=''
    for i in range(len(sente_mochigoma)):
        if sente_mochigoma[i] in kazu:
            sente_mochigoma_1+=(sente_mochigoma[i+1]+sente_mochigoma[i])
        else:
            if sente_mochigoma[i] in sente_mochigoma_1:
                pass
            else:
                sente_mochigoma_1+=sente_mochigoma[i]
    sente_mochigoma=sente_mochigoma_1
    
    if sente_mochigoma=='':
         sente_mochigoma='なし'
    
    koute_mochigoma_1=''
    for i in range(len(koute_mochigoma)):
        if koute_mochigoma[i] in kazu:
            koute_mochigoma_1+=(koute_mochigoma[i+1]+koute_mochigoma[i])
        else:
            if koute_mochigoma[i] in koute_mochigoma_1:
                pass
            else:
                koute_mochigoma_1+=koute_mochigoma[i]
    koute_mochigoma=koute_mochigoma_1
    
    if koute_mochigoma=='':
        koute_mochigoma='なし'
    return [filename,dan,koute_mochigoma,sente_mochigoma,tesuu,humen]


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
    kifu_1=kifu.split('\n')
    tesuu=kifu_1[-1].replace('まで','').replace('手で後手の勝ち','')
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
        if each_sashite[-1] != '打': #駒を動かすときの処理
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
        else: #駒を打つときの処理
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
            koma_convert=json.loads(line)
    with open(r'設定\持ち駒設定.txt','r') as r:
        for line in r:
            mochigoma_convert=json.loads(line)
    
    if humen=='':
        all_sfen = [x.strip() for x in sfen]
    else:
        humen=int(humen.replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４').replace('5','５')\
                  .replace('6','６').replace('7','７').replace('8','８').replace('9','９'))+1
        all_sfen = []
        for N in range(humen):
            all_sfen.append(sfen[N])
    for line_num, sfen in tqdm(enumerate(all_sfen)):
        sfen_split = sfen.split(' ')
        kyokumen = sfen_split[0]
        teban = sfen_split[1]
        mochigoma = sfen_split[2]
        for i in range(1, 10):
            kyokumen = kyokumen.replace(str(i), '0'*i)
        for key, value in koma_convert.items():
            kyokumen = kyokumen.replace(key, value)
        each_lines = [('|' + each_line + '|') for each_line in kyokumen.split('/')]
        mochigoma_sente = []
        mochigoma_gote = []
        while len(mochigoma)>0:
            if mochigoma=='-' or mochigoma=='':
                mochigoma=''
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
    
    kazu=['18','17','16','15','14','13','12','11','10','９','８','７','６','５','４','３','２']
    
    sente_string_1=''
    for i in range(len(sente_string)):
        if sente_string[i] in kazu:
            sente_string_1+=(sente_string[i+1]+sente_string[i])
        else:
            if sente_string[i] in sente_string_1:
                pass
            else:
                sente_string_1+=sente_string[i]
    sente_string=sente_string_1
    
    if sente_string=='':
        sente_string='なし'
    
    gote_string_1=''
    for i in range(len(gote_string)):
        if gote_string[i] in kazu:
            gote_string_1+=(gote_string[i+1]+gote_string[i])
        else:
            if gote_string[i] in gote_string_1:
                pass
            else:
                gote_string_1+=gote_string[i]
    gote_string=gote_string_1
    
    if gote_string=='':
        gote_string='なし'
    
    dan=[]
    for l in range(len(each_lines)):
        D=[]
        d=each_lines[l].replace('|','')
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
    return [filename,dan,gote_string,sente_string,tesuu,humen-1]


#######################################################
########　通常の盤面グラフィック作成用関数　　#########
########　pdfでグラフの描画データを出力   　　#########
########　保存先は「図面データ」　　　　　　　#########
#######################################################
#bod_tolist,kif_tolist関数からグラフを作成
def list_tograph(filename,
                 dan,
                 koute_mochigoma,
                 sente_mochigoma,
                 tesuu,
                 humenn=5,
                 sisizu='☗５五歩',
                 sente_name='民友',
                 koute_name='太郎'
                ):
    '''
    def list_tograph(filename,dan,koute_mochigoma,sente_mochigoma,
                 tesuu,humenn=5,sisizu='☗５五歩',sente_name='民友',koute_name='太郎'):
    ※要求する変数
    filename:対象のファイル名（絶対パス）
    koute_mochigoma:後手の持ち駒
    sente_mochigoma:先手の持ち駒
    tesuu:手数
    humenn:第何譜の数字
    sisizu：指指図の指し手
    sente_name:先手の名前
    koute_name:後手の名前
    
    '''
    #基準数を設定
    #len(sente_mochigoma)+len(sente_name)+2：先手持ち駒数＋先手氏名＋駒文字＋空白
    #len(koute_mochigoma)+len(koute_name)+2：後手持ち駒数＋後手氏名＋駒文字＋空白
    #↑を比べて文字数が多い方の文字数を基準数として設定
    if len(koute_mochigoma)+len(koute_name)+2 > len(sente_mochigoma)+len(sente_name)+2:
        kijyun=len(koute_mochigoma)+len(koute_name)+2
    elif len(koute_mochigoma)+len(koute_name)+2 == len(sente_mochigoma)+len(sente_name)+2:
        kijyun=len(koute_mochigoma)+len(koute_name)+2
    else:
        kijyun=len(sente_mochigoma)+len(sente_name)+2
    
    #グラフ全体の比率、位置、持ち駒のフォントなどの設定
    #上記で設定した基準数に合わせて図の比率rectと持ち駒の印字開始座標とフォント数を設定
    #ここでは基準数が８をと等しいか、それ以上かそれ以下かによってグラフ全体の描画に関わる設定を行う
    if kijyun<8:
        fontsize=8 #持ち駒のフォントサイズ
        step=0.5 #持ち駒文字の座標差分
        sente_start=5.24 #先手持ち駒の描画開始ｙ座標
        koute_start=5.76 #後手持ち駒の描画開始ｙ座標
        rect=[0.08,0.08,0.85,0.76] #描画全体の位置、比率の設定
        tate=10.35 #盤面縦番号（一、二、三）のｘ座標設定
        yoko=10.25 #盤面横番号（１、２、３）のｙ座標設定
    elif kijyun==8:
        fontsize=8
        step=0.5
        sente_start=5.24
        koute_start=5.76
        rect=[0.08,0.08,0.85,0.76]
        tate=10.35
        yoko=10.25
    elif kijyun>8:
        fontsize=7.8
        step=0.5
        sente_start=5.24
        koute_start=5.76
        rect=[0.096,0.08,0.85,0.76]
        tate=10.3
        yoko=10.25
    
    #グラフ全体の設定
    #描画全体のフォント設定
    plt.rcParams['font.family'] = 'MS Mincho'
    plt.rcParams['font.size'] = 7
    #書き出すPDFファイル名の設定
    #書き出し先は「図面データ」のフォルダ
    filename_2=filename.split('/')
    pdf=PdfPages('図面データ/'+filename_2[-1].replace('.bod','').replace('.kif','')+".pdf")
    #グラフの体裁設定
    fig = plt.figure() 
    fig = plt.figure(figsize=(2.17, 2.36))
    ax = fig.add_axes(rect)
    ax.set_xlim(1,10)
    ax.set_ylim(1,10)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    
    #将棋盤形式にするためのグラフ描画
    #罫線
    for i in range(1,11):
        ax.hlines(y=i, xmin=1, xmax=10,color='k',lw=0.5)
        ax.vlines(x=i, ymin=1, ymax=10,color='k',lw=0.5)
    #横番号
    ax.text(1.5, yoko, '９', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(2.5, yoko, '８', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(3.5, yoko, '７', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(4.5, yoko, '６', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(5.5, yoko, '５', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(6.5, yoko, '４', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(7.5, yoko, '３', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(8.5, yoko, '２', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(9.5, yoko, '１', ha='center',va='center',rotation=0,fontsize=8)
    #縦番号
    ax.text(tate, 9.5, '一', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 8.5, '二', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 7.5, '三', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 6.5, '四', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 5.5, '五', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 4.5, '六', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 3.5, '七', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 2.5, '八', ha='center',va='center',rotation=0,fontsize=8)
    ax.text(tate, 1.5, '九', ha='center',va='center',rotation=0,fontsize=8)
    #盤上の点
    ax.scatter(4,7,color='k',s=2)
    ax.scatter(7,7,color='k',s=2)
    ax.scatter(4,4,color='k',s=2)
    ax.scatter(7,4,color='k',s=2)
    
    #持ち駒の描画
    #持ち駒の文字列を「☗佐藤　飛金二銀桂香歩三」のような形に整形する
    sente_mochigoma='☗'+str(sente_name)+' '+sente_mochigoma
    koute_mochigoma='☖'+str(koute_name)+' '+koute_mochigoma
    
    #先手持ち駒の描画
    senteX=0.7 #先手持ち駒の１列目ｘ座標
    senteY=sente_start #先手持ち駒の描画開始ｙ座標の設定
    #sente_mochigomaの文字数分描画をする
    for sen in range(len(sente_mochigoma)):
        #sente_mochigomaの８文字目までの場合
        if sen<8:
            #（senteX、senteY）の座標に持ち駒を描写する
            #フォントは「family='MS Gothic'」の部分でMSゴシックを設定
            #フォントサイズは「fontsize=fontsize」基準数に応じて設定した持ち駒のフォントサイズを設定
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            #基準数に応じて設定した持ち駒文字の座標差分をsenteYから引く
            senteY-=step 
        #sente_mochigomaの８文字の場合
        elif sen==8:
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            #senteYの値を駒文字の開始位置まで戻す
            #例：「☗佐藤　飛金二銀桂香歩三」であれば「飛」の位置に再設定する
            senteY=sente_start-(len(sente_name)+2)*step
        #sente_mochigomaの８文字以降の場合
        elif sen>8:
            #senteXの値を持ち駒の２列目のｘ座標に再設定
            senteX=0.22
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            #基準数に応じて設定した持ち駒文字の座標差分をsenteYから引く
            senteY-=step
    
    #後手持ち駒の描写
    kouteX=0.7         #後手持ち駒の１列目ｘ座標
    kouteY=koute_start #後手持ち駒の描画開始ｙ座標の設定
    #koute_mochigomaの文字数分描画をする
    for kou in range(len(koute_mochigoma)):
        #koute_mochigomaの８文字目までの場合
        if kou<8:
            #（kouteX、kouteY）の座標に持ち駒を描写する
            #フォントは「family='MS Gothic'」の部分でMSゴシックを設定
            #フォントサイズは「fontsize=fontsize」基準数に応じて設定した持ち駒のフォントサイズを設定
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            #基準数に応じて設定した持ち駒文字の座標差分をkouteYから引く
            kouteY+=step
        #koute_mochigomaの８文字以降の場合
        elif kou==8:
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            #kouteYの値を駒文字の開始位置まで戻す
            #例：「☗佐藤　飛金二銀桂香歩三」であれば「飛」の位置に再設定する
            kouteY=koute_start+(len(koute_name)+2)*step
        elif kou>8:
            #kouteXの値を持ち駒の２列目のｘ座標に再設定
            kouteX=0.22
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            #基準数に応じて設定した持ち駒文字の座標差分をkouteYから引く
            kouteY+=step
    
    
    #盤面への駒配置
    y=9.5 #後手側一の列の駒ｙ座標
    
    #読み込んだ変数danを１段ずつ見る処理
    #変数danの例
    #[['v香', 'v桂', 'v銀', 'v金', 'v玉', 'v金', 'v銀', 'v桂', 'v香'],
    #['・', '・', 'v飛', '・', '・', '・', '・', 'v角', '・'],
    #['歩', '歩', '歩', '歩', '歩', '歩', '歩', '歩', '歩'],
    #['・', '・', '・', '・', '・', '・', '・', '・', '・'],
    #['・', '・', '・', '・', '・', '・', '・', '・', '・'],
    #['・', '・', '・', '・', '・', '・', '・', '・', '・'],
    #['と', 'と', 'と', 'と', 'と', 'と', 'と', 'と', 'と'],
    #['・', '馬', '・', '・', '・', '・', '・', '龍', '・'],
    #['杏', '圭', '全', '金', '玉', '金', '全', '圭', '杏']]
    for k in range(len(dan)):
        #描画に必要な設定を行う
        #danの１段に含まれる文字列を順番に見て盤上に駒を描画する
        for i in range(len(dan[k])):
            #danの駒文字が「v」を含む場合
            if dan[k][i][0]=='v':
                #盤面に実際に描写する文字を設定
                #たとえば「v玉」となって入る場合2文字目を実際に盤面に描写する文字は「玉」
                moji=str(dan[k][i][1])
                #回転の角度を設定する
                #ここでは文字列に「ｖ」が含まれるため180度回転
                rot=180
                style='bold'
            #danの駒文字が「・」の場合
            elif dan[k][i][0]=='・':
                #mojiの中身を「''」として実際には描画を飛ばすようにする
                moji=str(dan[k][i]).replace('・','')
                rot=0
                style='medium'
            #その他はそのまま変数に格納
            else:
                moji=str(dan[k][i])
                rot=0
                style='medium'
            
            #グラフへの描画
            #実際にテキストをグラフへ描画する
            #フォントは「family='HGSeikaishotaiPRO'」としており「HG正楷書体-PRO」を使用
            
            #例外：成香車
            if dan[k][i][0]=='v' and dan[k][i][1]=='杏':
                #民友のスタイル
                #ax.text(i+1.5,y,'成', ha='center',va='top',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'香', ha='center',va='bottom',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #読売のスタイル
                #ナリの部分は「family='MS Gothic'」としており、MSゴシックを使用
                ax.text(i+1.5,y+0.1,'香', ha='center',va='center',rotation=rot,fontsize='12.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='5',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='杏':
                #民友のスタイル
                #ax.text(i+1.5,y,'香', ha='center',va='top',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'成', ha='center',va='bottom',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #読売のスタイル
                #ナリの部分は「family='MS Gothic'」としており、MSゴシックを使用
                ax.text(i+1.5,y-0.1,'香', ha='center',va='center',rotation=rot,fontsize='12.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='5',fontweight=1000,family='MS Gothic')
            
            #例外：成桂馬
            elif dan[k][i][0]=='v' and dan[k][i][1]=='圭':
                #民友のスタイル
                #ax.text(i+1.5,y,'成', ha='center',va='top',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'桂', ha='center',va='bottom',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #読売のスタイル
                #ナリの部分は「family='MS Gothic'」としており、MSゴシックを使用
                ax.text(i+1.5,y+0.15,'桂', ha='center',va='center',rotation=rot,fontsize='12.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='5',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='圭':
                #民友のスタイル
                #ax.text(i+1.5,y,'桂', ha='center',va='top',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'成', ha='center',va='bottom',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #読売のスタイル
                #ナリの部分は「family='MS Gothic'」としており、MSゴシックを使用
                ax.text(i+1.5,y-0.15,'桂', ha='center',va='center',rotation=rot,fontsize='12.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='5',fontweight=1000,family='MS Gothic')
            
            #例外：成銀
            elif dan[k][i][0]=='v' and dan[k][i][1]=='全':
                #民友のスタイル
                #ax.text(i+1.5,y,'成', ha='center',va='top',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'銀', ha='center',va='bottom',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #読売のスタイル
                #ナリの部分は「family='MS Gothic'」としており、MSゴシックを使用
                ax.text(i+1.5,y+0.15,'銀', ha='center',va='center',rotation=rot,fontsize='12.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='5',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='全':
                #民友のスタイル
                #ax.text(i+1.5,y,'銀', ha='center',va='top',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'成', ha='center',va='bottom',rotation=rot,fontsize='7.25',fontweight=1000,family='HGSeikaishotaiPRO')
                #読売のスタイル
                #ナリの部分は「family='MS Gothic'」としており、MSゴシックを使用
                ax.text(i+1.5,y-0.15,'銀', ha='center',va='center',rotation=rot,fontsize='12.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='5',fontweight=1000,family='MS Gothic')
            
            #例外：香、龍、歩、馬、角
            #これらはフォントの都合上、縦が枠からは飛び出してしまうので、例外としてｙ座標を調整して描画する
            #後手側の駒の場合
            elif dan[k][i][0]=='v' and dan[k][i][1]!='香':
                if dan[k][i][0]=='v' and dan[k][i][1]=='龍':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='歩':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='馬':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='角':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                else:
                    ax.text(i+1.5,y+0.1,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
            #先手側の駒の場合
            elif dan[k][i][0]!='v' and dan[k][i][0]!='香':
                if dan[k][i][0]!='v' and dan[k][i][0]=='龍':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='歩':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='馬':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='角':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
                else:
                    ax.text(i+1.5,y-0.1,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
            
            #それ以外の駒の描写
            else:
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='HGSeikaishotaiPRO')
        #次の繰り返し処理を行う前に段数を一つ下げるためにｙから１を引く
        y-=1 
    
    #手数の描画
    #読み込んできたtesuuの半角数字を全角文字に変換して描画
    #フォントは「family='MS Gothic'」としておりＭＳゴシック
    ax.text(5.5,0.6,'(指し手'+str(tesuu).replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４')\
            .replace('5','５').replace('6','６').replace('7','７').replace('8','８').replace('9','９')+'手)',
            ha='center',
            va='center',
            fontsize=7.5,
            family='MS Gothic')
    
    #【第●譜】の文字列設定
    #読み込んできたhumenの半角数字を全角文字に変換して描画
    t1='【第'+str(humenn).replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４')\
    .replace('5','５').replace('6','６').replace('7','７').replace('8','８').replace('9','９')+'譜】'
    
    #（指始図は○○○まで）の文字列設定
    #読み込んできたhumenの半角数字を全角文字に変換して描画
    t2='（指始図は'+str(sisizu).replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４')\
    .replace('5','５').replace('6','６').replace('7','７').replace('8','８').replace('9','９')+'まで）'
    
    #【第●譜】の描画
    #フォントは「family='MS Gothic'」としておりＭＳゴシック
    ax.text(5.5,11.35,t1, ha='center',va='center',fontsize=7.5,family='MS Gothic',fontweight='bold')
    #（指始図は○○○まで）の文字列設定
    #フォントは「family='MS Gothic'」としておりＭＳゴシック
    ax.text(5.5,10.79,t2, ha='center',va='center',family='MS Gothic')
    
    #描画したグラフの保存処理
    #「図面データ」のフォルダに保存
    pdf.savefig(fig)
    #終了処理
    pdf.close()
    

#######################################################
########　指了図盤面グラフィック作成用関数　　#########
########　pdfでグラフの描画データを出力   　　#########
########　保存先は「図面データ」　　　　　　　#########
#######################################################
#bod_tolist,kif_tolist関数からグラフを作成
def list_tograph_toryo(filename,
                 dan,
                 koute_mochigoma,
                 sente_mochigoma,
                 tesuu,
                 humenn=5,
                 sisizu='☗５五歩',
                 sente_name='民友',
                 koute_name='太郎'
                ):
    '''
    def list_tograph_toryo(filename,dan,koute_mochigoma,sente_mochigoma,
                 tesuu,humenn=5,sisizu='☗５五歩',sente_name='民友',koute_name='太郎'):
    ※要求する変数
    filename:対象のファイル
    dan     :盤面のリスト
    koute_mochigoma:後手の持ち駒
    sente_mochigoma:先手の持ち駒
    tesuu:手数
    humenn:第何譜の数字
    sisizu：指指図の指し手
    sente_name:先手の名前
    koute_name:後手の名前
    
    '''
    #先手後手の持ち駒の文字数を比較して基準の数を設定
    if len(koute_mochigoma)+len(koute_name)+2 > len(sente_mochigoma)+len(sente_name)+2:
        kijyun=len(koute_mochigoma)+len(koute_name)+2
    elif len(koute_mochigoma)+len(koute_name)+2 == len(sente_mochigoma)+len(sente_name)+2:
        kijyun=len(koute_mochigoma)+len(koute_name)+2
    else:
        kijyun=len(sente_mochigoma)+len(sente_name)+2
    #基準に合わせて図の比率rectと持ち駒の印字開始座標とフォント数を設定
    if kijyun<8:
        fontsize=6.3
        step=0.55
        sente_start=5.22
        koute_start=5.78
        rect=[0.09,0.075,0.83,0.84]
        tate=10.34
        yoko=10.35
    elif kijyun==8:
        fontsize=6.3
        step=0.55
        sente_start=5.22
        koute_start=5.78
        rect=[0.09,0.075,0.83,0.84]
        tate=10.34
        yoko=10.35
    elif kijyun>8:
        fontsize=6.3
        step=0.55
        sente_start=5.22
        koute_start=5.78
        rect=[0.11,0.075,0.83,0.84]
        tate=10.34
        yoko=10.35
    #全体のフォント設定
    plt.rcParams['font.family'] = 'MS Mincho'
    plt.rcParams['font.size'] = 7
    #ファイル名の設定
    #ファイル名の設定
    filename_2=filename.split('/')
    pdf=PdfPages('図面データ/指了図_'+filename_2[-1].replace('.bod','').replace('.kif','')+".pdf")
    #グラフの体裁設定
    fig = plt.figure() 
    fig = plt.figure(figsize=(1.68608333, 1.600830556))
    ax = fig.add_axes(rect)
    ax.set_xlim(1,10)
    ax.set_ylim(1,10)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    #罫線
    for i in range(1,11):
        ax.hlines(y=i, xmin=1, xmax=10,color='k',lw=0.4)
        ax.vlines(x=i, ymin=1, ymax=10,color='k',lw=0.4)
    #横番号
    ax.text(1.5, yoko, '９', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(2.5, yoko, '８', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(3.5, yoko, '７', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(4.5, yoko, '６', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(5.5, yoko, '５', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(6.5, yoko, '４', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(7.5, yoko, '３', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(8.5, yoko, '２', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(9.5, yoko, '１', ha='center',va='center',rotation=0,fontsize=7)
    #縦番号
    ax.text(tate, 9.5, '一', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 8.5, '二', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 7.5, '三', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 6.5, '四', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 5.5, '五', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 4.5, '六', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 3.5, '七', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 2.5, '八', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(tate, 1.5, '九', ha='center',va='center',rotation=0,fontsize=7)
    #盤上の点
    ax.scatter(4,7,color='k',s=1.5)
    ax.scatter(7,7,color='k',s=1.5)
    ax.scatter(4,4,color='k',s=1.5)
    ax.scatter(7,4,color='k',s=1.5)
    #持ち駒
    sente_mochigoma='☗'+str(sente_name)+' '+sente_mochigoma
    koute_mochigoma='☖'+str(koute_name)+' '+koute_mochigoma
    #先手持ち駒の描画
    senteX=0.65
    senteY=sente_start#5.3
    for sen in range(len(sente_mochigoma)):
        if sen<8:
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            senteY-=step
        elif sen==8:
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            senteY=sente_start-(len(sente_name)+2)*step
        elif sen>8:
            senteX=0.1
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            senteY-=step#0.4       
    #後手持ち駒の描写
    kouteX=0.65
    kouteY=koute_start#5.7
    for kou in range(len(koute_mochigoma)):
        if kou<8:
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            kouteY+=step#0.4
        elif kou==8:
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            kouteY=koute_start+(len(koute_name)+2)*step
        elif kou>8:
            kouteX=0.1
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            kouteY+=step#0.4
    #駒配置
    y=9.5
    for k in range(len(dan)):
        for i in range(len(dan[k])):
            if dan[k][i][0]=='v':
                moji=str(dan[k][i][1])
                rot=180
                style='bold'
            elif dan[k][i][0]=='・':
                moji=str(dan[k][i]).replace('・','')
                rot=0
                style='medium'
            else:
                moji=str(dan[k][i])
                rot=0
                style='medium'
            if dan[k][i][0]=='v' and dan[k][i][1]=='杏':
                #ax.text(i+1.5,y,'成', ha='center',va='top',rotation=rot,fontsize='5.5',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'香', ha='center',va='bottom',rotation=rot,fontsize='5.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.1,'香', ha='center',va='center',rotation=rot,fontsize='9.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3.8',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='杏':
                #ax.text(i+1.5,y,'香', ha='center',va='top',rotation=rot,fontsize='5.5',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y,'成', ha='center',va='bottom',rotation=rot,fontsize='5.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.1,'香', ha='center',va='center',rotation=rot,fontsize='9.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3.8',fontweight=1000,family='MS Gothic')
                
            elif dan[k][i][0]=='v' and dan[k][i][1]=='圭':
                ax.text(i+1.5,y+0.15,'桂', ha='center',va='center',rotation=rot,fontsize='9.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3.8',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='圭':
                ax.text(i+1.5,y-0.15,'桂', ha='center',va='center',rotation=rot,fontsize='9.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3.8',fontweight=1000,family='MS Gothic')
            
            elif dan[k][i][0]=='v' and dan[k][i][1]=='全':
                ax.text(i+1.5,y+0.15,'銀', ha='center',va='center',rotation=rot,fontsize='9.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3.8',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='全':
                ax.text(i+1.5,y-0.15,'銀', ha='center',va='center',rotation=rot,fontsize='9.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3.8',fontweight=1000,family='MS Gothic')
            
            elif dan[k][i][0]=='v' and dan[k][i][1]!='香':
                if dan[k][i][0]=='v' and dan[k][i][1]=='龍':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='歩':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='馬':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='角':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                else:
                    ax.text(i+1.5,y+0.1,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
            elif dan[k][i][0]!='v' and dan[k][i][0]!='香':
                if dan[k][i][0]!='v' and dan[k][i][0]=='龍':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='歩':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='馬':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='角':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
                else:
                    ax.text(i+1.5,y-0.1,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
            else:
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='HGSeikaishotaiPRO')
        y-=1 
    #手数
    ax.text(5.5,0.6,'(指し手'+str(tesuu).replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４')\
            .replace('5','５').replace('6','６').replace('7','７').replace('8','８').replace('9','９')+'手)', ha='center',va='center'\
            ,family='MS Gothic')
    pdf.savefig(fig)
    pdf.close()

    
#######################################################
########　参考図盤面グラフィック作成用関数　　#########
########　pdfでグラフの描画データを出力   　　#########
########　保存先は「図面データ」　　　　　　　#########
#######################################################
#bod_tolist,kif_tolist関数からグラフを作成
def list_tograph_sanko(filename,
                 dan,
                 koute_mochigoma,
                 sente_mochigoma,
                 tesuu,
                 humenn=5,
                 sisizu='☗５五歩',
                 sente_name='民友',
                 koute_name='太郎'
                ):
    '''
    def list_tograph_sanko(filename,dan,koute_mochigoma,sente_mochigoma,
                 tesuu,humenn=5,sisizu='☗５五歩',sente_name='民友',koute_name='太郎'):
    ※要求する変数
    filename:対象のファイル
    dan     :盤面のリスト
    koute_mochigoma:後手の持ち駒
    sente_mochigoma:先手の持ち駒
    tesuu:手数
    humenn:第何譜の数字
    sisizu：指指図の指し手
    sente_name:先手の名前
    koute_name:後手の名前
    
    '''
    #先手後手の持ち駒の文字数を比較して基準の数を設定
    if len(koute_mochigoma)+len(koute_name)+2 > len(sente_mochigoma)+len(sente_name)+2:
        kijyun=len(koute_mochigoma)+len(koute_name)+2
    elif len(koute_mochigoma)+len(koute_name)+2 == len(sente_mochigoma)+len(sente_name)+2:
        kijyun=len(koute_mochigoma)+len(koute_name)+2
    else:
        kijyun=len(sente_mochigoma)+len(sente_name)+2
    #基準に合わせて図の比率rectと持ち駒の印字開始座標とフォント数を設定
    if kijyun<8:
        fontsize=6.3
        step=0.62
        sente_start=5.18
        koute_start=5.82
        rect=[0.11,0.06,0.8,0.8]
    elif kijyun==8:
        fontsize=6.5
        step=0.62
        sente_start=5.18
        koute_start=5.82
        rect=[0.11,0.06,0.8,0.8]
    elif kijyun>8:
        fontsize=6.3
        step=0.62
        sente_start=5.63
        koute_start=6.31
        rect=[0.13,0.06,0.8,0.8]
    #全体のフォント設定
    #plt.rcParams['pdf.fonttype']=42
    plt.rcParams['font.family'] = 'MS Mincho'
    plt.rcParams['font.size'] = 7
    #ファイル名の設定
    filename_2=filename.split('/')
    pdf=PdfPages('図面データ/参考図_'+filename_2[-1].replace('.bod','').replace('.kif','')+".pdf")
    #グラフの体裁設定
    fig = plt.figure() 
    fig = plt.figure(figsize=(1.5165263889, 1.4322236111))
    #fig = plt.figure(figsize=(5.6, 6.0))
    ax = fig.add_axes(rect)#([0.095,0.07,0.85,0.8])
    ax.set_xlim(1,10)
    ax.set_ylim(1,10)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    #罫線
    for i in range(1,11):
        ax.hlines(y=i, xmin=1, xmax=10,color='k',lw=0.3)
        ax.vlines(x=i, ymin=1, ymax=10,color='k',lw=0.3)
    #横番号
    ax.text(1.5, 10.35, '９', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(2.5, 10.35, '８', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(3.5, 10.35, '７', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(4.5, 10.35, '６', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(5.5, 10.35, '５', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(6.5, 10.35, '４', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(7.5, 10.35, '３', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(8.5, 10.35, '２', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(9.5, 10.35, '１', ha='center',va='center',rotation=0,fontsize=7)
    #縦番号
    ax.text(10.38, 9.5, '一', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 8.5, '二', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 7.5, '三', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 6.5, '四', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 5.5, '五', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 4.5, '六', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 3.5, '七', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 2.5, '八', ha='center',va='center',rotation=0,fontsize=7)
    ax.text(10.38, 1.5, '九', ha='center',va='center',rotation=0,fontsize=7)
    #盤上の点
    ax.scatter(4,7,color='k',s=1)
    ax.scatter(7,7,color='k',s=1)
    ax.scatter(4,4,color='k',s=1)
    ax.scatter(7,4,color='k',s=1)
    #持ち駒
    sente_mochigoma='☗'+str(sente_name)+' '+sente_mochigoma
    koute_mochigoma='☖'+str(koute_name)+' '+koute_mochigoma
    #先手持ち駒の描画
    senteX=0.6
    senteY=sente_start#5.3
    for sen in range(len(sente_mochigoma)):
        if sen<8:
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            senteY-=step
        elif sen==8:
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            senteY=sente_start-(len(sente_name)+2)*step
        elif sen>8:
            senteX=-0.1
            ax.text(senteX, senteY, str(sente_mochigoma[sen]), ha='center',va='center',rotation=0,fontsize=fontsize,family='MS Gothic')
            senteY-=step#0.4       
    #後手持ち駒の描写
    kouteX=0.6
    kouteY=koute_start#5.7
    for kou in range(len(koute_mochigoma)):
        if kou<8:
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            kouteY+=step#0.4
        elif kou==8:
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            kouteY=koute_start+(len(koute_name)+2)*step
        elif kou>8:
            kouteX=-0.1
            ax.text(kouteX, kouteY, str(koute_mochigoma[kou]), ha='center',va='center',rotation=180,fontsize=fontsize,family='MS Gothic')
            kouteY+=step#0.4
    #駒配置
    y=9.5
    for k in range(len(dan)):
        for i in range(len(dan[k])):
            if dan[k][i][0]=='v':
                moji=str(dan[k][i][1])
                rot=180
                style='bold'
            elif dan[k][i][0]=='・':
                moji=str(dan[k][i]).replace('・','')
                rot=0
                style='medium'
            else:
                moji=str(dan[k][i])
                rot=0
                style='medium'
            
            if dan[k][i][0]=='v' and dan[k][i][1]=='杏':
                ax.text(i+1.5,y,'成', ha='center',va='top',rotation=rot,fontsize='4.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y,'香', ha='center',va='bottom',rotation=rot,fontsize='4.5',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y+0.1,'香', ha='center',va='center',rotation=rot,fontsize='8',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='杏':
                ax.text(i+1.5,y,'香', ha='center',va='top',rotation=rot,fontsize='4.5',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y,'成', ha='center',va='bottom',rotation=rot,fontsize='4.5',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y-0.1,'香', ha='center',va='center',rotation=rot,fontsize='8',fontweight=1000,family='HGSeikaishotaiPRO')
                #ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3',fontweight=1000,family='MS Gothic')
                
            elif dan[k][i][0]=='v' and dan[k][i][1]=='圭':
                ax.text(i+1.5,y+0.15,'桂', ha='center',va='center',rotation=rot,fontsize='8',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='圭':
                ax.text(i+1.5,y-0.15,'桂', ha='center',va='center',rotation=rot,fontsize='8',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3',fontweight=1000,family='MS Gothic')
            
            elif dan[k][i][0]=='v' and dan[k][i][1]=='全':
                ax.text(i+1.5,y+0.15,'銀', ha='center',va='center',rotation=rot,fontsize='8',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y-0.45,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3',fontweight=1000,family='MS Gothic')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='全':
                ax.text(i+1.5,y-0.15,'銀', ha='center',va='center',rotation=rot,fontsize='8',fontweight=1000,family='HGSeikaishotaiPRO')
                ax.text(i+1.5,y+0.15,'ナ　リ', ha='center',va='bottom',rotation=rot,fontsize='3',fontweight=1000,family='MS Gothic')
            
            elif dan[k][i][0]=='v' and dan[k][i][1]!='香':
                if dan[k][i][0]=='v' and dan[k][i][1]=='龍':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='歩':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='馬':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='角':
                    ax.text(i+1.5,y+0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                else:
                    ax.text(i+1.5,y+0.1,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
            elif dan[k][i][0]!='v' and dan[k][i][0]!='香':
                if dan[k][i][0]!='v' and dan[k][i][0]=='龍':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='歩':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='馬':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='角':
                    ax.text(i+1.5,y-0.05,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
                else:
                    ax.text(i+1.5,y-0.1,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
            else:
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='9',fontweight=1000,family='HGSeikaishotaiPRO')
        y-=1 
        
    t2='（参考図は'+str(sisizu).replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４')\
    .replace('5','５').replace('6','６').replace('7','７').replace('8','８').replace('9','９')+'まで）'
    ax.text(5.5,11.1,t2, ha='center',va='center',family='MS Gothic')
    pdf.savefig(fig)
    pdf.close()
