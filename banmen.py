import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

komafont={'玉':'0','金':'1','銀':'2','桂':'3','香':'4','飛':'5','角':'6','歩':'7','と':'a','全':'b','圭':'c','杏':'d','龍':'e','馬':'f'}

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
                 savedir,
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
    save_dir:保存先フォルダ
    
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
    pdf=PdfPages(savedir+'/'+filename_2[-1].replace('.bod','').replace('.kif','')+".pdf")
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
    ax.text(tate, 9.5, '一', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 8.5, '二', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 7.5, '三', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 6.5, '四', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 5.5, '五', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 4.5, '六', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 3.5, '七', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 2.5, '八', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    ax.text(tate, 1.5, '九', ha='center',va='center',rotation=0,fontsize=8,weight='bold')
    #盤上の点
    ax.scatter(4,7,color='k',s=2)
    ax.scatter(7,7,color='k',s=2)
    ax.scatter(4,4,color='k',s=2)
    ax.scatter(7,4,color='k',s=2)
    
    #持ち駒の描画
    #持ち駒の文字列を「☗佐藤　飛金二銀桂香歩三」のような形に整形する
    sente_mochigoma='☗'+str(sente_name)+' '+sente_mochigoma.replace("二","２").replace("三","３").replace("四","４").replace("五","５").replace("六","６").replace("七","７").replace("八","８").replace("九","９")
    koute_mochigoma='☖'+str(koute_name)+' '+koute_mochigoma.replace("二","２").replace("三","３").replace("四","４").replace("五","５").replace("六","６").replace("七","７").replace("八","８").replace("九","９")
    
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
                danmoji=str(dan[k][i][1])
                moji=komafont[danmoji]
                #回転の角度を設定する
                #ここでは文字列に「ｖ」が含まれるため180度回転
                rot=180
                #style='bold'
            #danの駒文字が「・」の場合
            elif dan[k][i][0]=='・':
                #mojiの中身を「''」として実際には描画を飛ばすようにする
                moji=str(dan[k][i]).replace('・','')
                rot=0
                #style='medium'
            #その他はそのまま変数に格納
            else:
                danmoji=str(dan[k][i])
                moji=komafont[danmoji]
                rot=0
                #style='medium'
            
            #グラフへの描画
            #実際にテキストをグラフへ描画する
            #フォントは「family='HGSeikaishotaiPRO'」としており「HG正楷書体-PRO」を使用
            
            #例外：成香車
            if dan[k][i][0]=='v' and dan[k][i][1]=='杏':
                moji=komafont['杏']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='杏':
                moji=komafont['杏']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            
            #例外：成桂馬
            elif dan[k][i][0]=='v' and dan[k][i][1]=='圭':
                moji=komafont['圭']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='圭':
                moji=komafont['圭']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            
            #例外：成銀
            elif dan[k][i][0]=='v' and dan[k][i][1]=='全':
                moji=komafont['全']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='全':
                moji=komafont['全']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            
            #例外：香、龍、歩、馬、角
            #これらはフォントの都合上、縦が枠からは飛び出してしまうので、例外としてｙ座標を調整して描画する
            #後手側の駒の場合
            elif dan[k][i][0]=='v' and dan[k][i][1]!='香':
                if dan[k][i][0]=='v' and dan[k][i][1]=='龍':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='歩':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='馬':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='角':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                else:
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            #先手側の駒の場合
            elif dan[k][i][0]!='v' and dan[k][i][0]!='香':
                if dan[k][i][0]!='v' and dan[k][i][0]=='龍':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='歩':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='馬':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='角':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
                else:
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
            
            #それ以外の駒の描写(香)
            else:
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='13.5',fontweight=1000,family='syogi')
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
