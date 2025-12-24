import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

komafont={'玉':'0','金':'1','銀':'2','桂':'3','香':'4','飛':'5','角':'6','歩':'7','と':'a','全':'b','圭':'c','杏':'d','龍':'e','馬':'f'}

#######################################################
########　指了図盤面グラフィック作成用関数　　#########
########　pdfでグラフの描画データを出力   　　#########
#######################################################
#bod_tolist,kif_tolist関数からグラフを作成
def list_tograph_toryo(filename,
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
    savedir:保存先フォルダ
    
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
    pdf=PdfPages(savedir+'/指了図_'+filename_2[-1].replace('.bod','').replace('.kif','')+".pdf")
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
    ax.text(tate, 9.5, '一', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 8.5, '二', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 7.5, '三', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 6.5, '四', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 5.5, '五', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 4.5, '六', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 3.5, '七', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 2.5, '八', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    ax.text(tate, 1.5, '九', ha='center',va='center',rotation=0,fontsize=7,weight='bold')
    #盤上の点
    ax.scatter(4,7,color='k',s=1.5)
    ax.scatter(7,7,color='k',s=1.5)
    ax.scatter(4,4,color='k',s=1.5)
    ax.scatter(7,4,color='k',s=1.5)
    #持ち駒
    sente_mochigoma='☗'+str(sente_name)+' '+sente_mochigoma.replace("二","２").replace("三","３").replace("四","４").replace("五","５").replace("六","６").replace("七","７").replace("八","８").replace("九","９")
    koute_mochigoma='☖'+str(koute_name)+' '+koute_mochigoma.replace("二","２").replace("三","３").replace("四","４").replace("五","５").replace("六","６").replace("七","７").replace("八","８").replace("九","９")
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
                danmoji=str(dan[k][i][1])
                moji=komafont[danmoji]
                rot=180
                
            elif dan[k][i][0]=='・':
                moji=str(dan[k][i]).replace('・','')
                rot=0
                
            else:
                danmoji=str(dan[k][i])
                moji=komafont[danmoji]
                rot=0

            if dan[k][i][0]=='v' and dan[k][i][1]=='杏':
                moji=komafont['杏']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='杏':
                moji=komafont['杏']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
                
            elif dan[k][i][0]=='v' and dan[k][i][1]=='圭':
                moji=komafont['圭']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='圭':
                moji=komafont['圭']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
            
            elif dan[k][i][0]=='v' and dan[k][i][1]=='全':
                moji=komafont['全']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
            elif dan[k][i][0]!='v' and dan[k][i][0]=='全':
                moji=komafont['全']
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
            elif dan[k][i][0]=='v' and dan[k][i][1]!='香':
                if dan[k][i][0]=='v' and dan[k][i][1]=='龍':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='歩':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='馬':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='角':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]=='v' and dan[k][i][1]=='桂':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
                else:
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
            elif dan[k][i][0]!='v' and dan[k][i][0]!='香':
                if dan[k][i][0]!='v' and dan[k][i][0]=='龍':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='歩':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='馬':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='角':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
                elif dan[k][i][0]!='v' and dan[k][i][0]=='桂':
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10',fontweight=1000,family='syogi')
                else:
                    ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
            else:
                ax.text(i+1.5,y,moji, ha='center',va='center',rotation=rot,fontsize='10.5',fontweight=1000,family='syogi')
        y-=1 
    #手数
    ax.text(5.5,0.6,'(指し手'+str(tesuu).replace('0','０').replace('1','１').replace('2','２').replace('3','３').replace('4','４')\
            .replace('5','５').replace('6','６').replace('7','７').replace('8','８').replace('9','９')+'手)', ha='center',va='center'\
            ,family='MS Gothic')
    pdf.savefig(fig)
    pdf.close()
