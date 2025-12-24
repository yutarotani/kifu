import subprocess,time,datetime
import os, tkinter, tkinter.filedialog, tkinter.messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont
from readBOD import bod_tolist as bod
from readKIF import kif_tolist as kif
from banmen import list_tograph as graph
from banmenShiryozu import list_tograph_toryo as toryo
from banmenSankozu import list_tograph_sanko as sanko

files=[]

fTyp = [('kifファイル','*.kif'),('bodファイル','*.bod')] 

with open(r'設定\初期フォルダ.txt','r') as r:
    for line in r:
        iDir = line

root = tkinter.Tk()
root.title(u"棋譜盤面EPS作成")
root.geometry("400x500")



def create(event):

    label_start=tkinter.Label(text=str(datetime.datetime.now())+':処理開始します')
    label_start.pack()

    output_file=''
    inputfile_2=files[0].split('/')
    print("下記ファイルの盤面EPSを作成します")

    saveDir = tkinter.filedialog.askdirectory(title="保存先を決めてください")

    print(inputfile_2[-1])
    #.bodの場合
    if ".bod" in files[0]:
        
        if EditBox_2.get()=="" or EditBox_3.get()=="" or combobox_syu.get()=="":
            label_bodC=tkinter.Label(text=u'※※図面上部の記載事項が入力されていません※※',width=60)
            label_bodC.pack()
            return
        elif EditBox_tesu.get()=="":
            label_bodC=tkinter.Label(text=u'※※何手目か入力されていません※※',width=60)
            label_bodC.pack()
        else:
            K=bod(files[0],EditBox_2.get())
            if combobox_syu.get()=="指始図":
                input_file = saveDir + "/"+  inputfile_2[-1].replace('.bod','')+'.pdf'
                output_file = saveDir +  "/" + inputfile_2[-1].replace('.bod','')+'.eps'
            elif combobox_syu.get()=="指了図":
                input_file = saveDir + '/指了図_' + inputfile_2[-1].replace('.bod','')+'.pdf'
                output_file = saveDir + '/指了図_' + inputfile_2[-1].replace('.bod','')+'.eps'
            elif combobox_syu.get()=="/参考図":
                input_file = saveDir + '/参考図_' + inputfile_2[-1].replace('.bod','')+'.pdf'
                output_file = saveDir + '/参考図_' + inputfile_2[-1].replace('.bod','')+'.eps'
    #.kifの場合
    elif ".kif" in files[0]:
        if EditBox_2.get()=="" or EditBox_3.get()=="" or combobox_syu.get()=="":
            label_kifC=tkinter.Label(text=u'※※図面上部の記載事項が入力されていません※※',width=60)
            label_kifC.pack()
            return
        elif  EditBox_tesu.get()=="":
            label_kifC=tkinter.Label(text=u'※※指了図の盤面を出力します※※',width=60)
            label_kifC.pack()
        try:
            K=kif(files[0],str(EditBox_tesu.get()))
        except IndexError:
            label_indexError=tkinter.Label(text=u'※※手数の指定が対象データの記載範囲を超えています※※',fg='red')
            label_indexError.pack()
            return
        if combobox_syu.get()=="指始図":
            input_file = saveDir + "/" + inputfile_2[-1].replace('.kif','')+'.pdf'
            output_file = saveDir + "/" + inputfile_2[-1].replace('.kif','')+'.eps'
        elif combobox_syu.get()=="指了図":
            input_file = saveDir + '/指了図_' + inputfile_2[-1].replace('.kif','')+'.pdf'
            output_file = saveDir + '/指了図_' + inputfile_2[-1].replace('.kif','')+'.eps'
        elif combobox_syu.get()=="参考図":
            input_file = saveDir + '/参考図_' + inputfile_2[-1].replace('.kif','')+'.pdf'
            output_file = saveDir + '/参考図_' + inputfile_2[-1].replace('.kif','')+'_参考図.eps'
        
    #sisizuを作成
    if combobox.get()=='先手':
        sisizu_1='☗'
    elif combobox.get()=='後手':
        sisizu_1='☖'
    sisizu_2=EditBox_3.get()
    Sisizu=sisizu_1+sisizu_2
    
    if combobox_syu.get()=="指始図":
        try:
            graph(
                filename=K[0],
                dan=K[1],
                koute_mochigoma=K[2],
                sente_mochigoma=K[3],
                tesuu=K[5],
                humenn=EditBox_2.get(),
                sisizu=str(Sisizu),
                sente_name=sentename.get(),
                koute_name=gotename.get(),
                savedir=saveDir
                )
        except(PermissionError):
            permissionError()
            return
    elif combobox_syu.get()=="指了図":
        try:
            toryo(
                filename=K[0],
                dan=K[1],
                koute_mochigoma=K[2],
                sente_mochigoma=K[3],
                tesuu=K[5],
                humenn=EditBox_2.get(),
                sisizu=str(Sisizu),
                sente_name=sentename.get(),
                koute_name=gotename.get(),
                savedir=saveDir
                )
        except(PermissionError):
            permissionError()
            return
    elif combobox_syu.get()=="参考図":
        try:
            sanko(
                filename=K[0],
                dan=K[1],
                koute_mochigoma=K[2],
                sente_mochigoma=K[3],
                tesuu=K[5],
                humenn=EditBox_2.get(),
                sisizu=str(Sisizu),
                sente_name=sentename.get(),
                koute_name=gotename.get(),
                savedir=saveDir
                )
        except(PermissionError):
            permissionError()
            return
    
    label_PDF=tkinter.Label(text=str(datetime.datetime.now())+':PDFファイル作成完了')
    label_PDF.pack()
    
    subprocess.run(["pdftops","-eps",input_file,output_file],shell=True)
    label_EPS=tkinter.Label(text=str(datetime.datetime.now())+':EPSファイル作成完了')
    label_EPS.pack()
    
    time.sleep(5)
    
    label_FIN=tkinter.Label(text=str(datetime.datetime.now())+':処理が終了しました')
    label_FIN.pack()

    return

def fileset(event):
    file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
    EditBox_1.delete(0, tkinter.END)
    EditBox_1.insert(tkinter.END,file)
    files.clear()
    files.append(file)
    return 

def permissionError():
    label_permissionError1=tkinter.Label(text=str(datetime.datetime.now()),fg='red')
    label_permissionError2=tkinter.Label(text='※※※同名のPDFファイルを開いていますので閉じるか、※※※\n※※※開いていない場合は少し待って※※※\n※※※再度作成ボタンを押してください※※※',fg='red')
    label_permissionError1.pack()
    label_permissionError2.pack()
    return


#上部注意書き１ラベル
label_0 = tkinter.Label(text=u'図面に起こしたい棋譜データを選択してください',width=60)
label_0.pack()
#ファイル名エントリー
EditBox_1 = tkinter.Entry(width=60)
EditBox_1.pack()

#ファイル選択ボタン
Button_1 = tkinter.Button(text=u'ファイル選択', width=25)
Button_1.bind("<Button-1>",fileset)
Button_1.pack()

#図の種類をきく
label_syu = tkinter.Label(text=u'図面の種類を選択してください',width=60)
label_syu.pack()

module_syu = ('指始図', '指了図','参考図')
combobox_syu = ttk.Combobox(root, values=module_syu)
combobox_syu.current(0) 
combobox_syu.pack()

#上部注意書き１ラベル
label_1 = tkinter.Label(text=u'第何譜か数字で入力してください',width=60)
label_1.pack()

#上部注意書き１エントリー
EditBox_2 = tkinter.Entry(width=60)
EditBox_2.pack()

#上部注意書き１ラベル
label_tesu = tkinter.Label(text=u'何手目か数字で入力してください',width=60)
label_tesu.pack()

#上部注意書き１エントリー
EditBox_tesu = tkinter.Entry(width=60)
EditBox_tesu.pack()

#先手名前
sentelabel = tkinter.Label(text=u'図面に表示する先手の名前を入力してください',width=60)
sentelabel.pack()
#先手名前エントリー
sentename = tkinter.Entry(width=60)
sentename.pack()

#後手名前
gotelabel = tkinter.Label(text=u'図面に表示する後手の名前を入力してください',width=60)
gotelabel.pack()
#先手名前エントリー
gotename = tkinter.Entry(width=60)
gotename.pack()

#先手後手を選択
module = ('先手', '後手')
combobox = ttk.Combobox(root, values=module)
combobox.current(0) 
combobox.pack()

#上部注意書き２ラベル
label_2 = tkinter.Label(text=u'始指図の指し手を入力してください',width=60)
label_2.pack()

#上部注意書き２エントリー
EditBox_3 = tkinter.Entry(width=60)
EditBox_3.pack()

#図面に起こすボタン
Button_2 = tkinter.Button(text=u'PDF、EPSファイルを作成', width=25)
Button_2.bind("<Button-1>",create)
Button_2.pack()

root.mainloop()