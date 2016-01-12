#!/home/krzysztof/anaconda3/bin/python
import numpy as np
def macierz(nrow,ncol,liczba_bomb):
    wektor_pol=np.repeat(0,nrow*ncol)
    miejsca_bomb=np.random.choice(nrow*ncol,liczba_bomb,
                                  replace=False)
    wektor_pol[miejsca_bomb]=-1
    macierz_pol=np.reshape(wektor_pol,(-1,ncol))
    for i in np.arange(nrow):
        for j in np.arange(ncol):
            if macierz_pol[i,j]==-1:
                if(i-1)>=0:
                    if macierz_pol[i-1,j]!=-1:
                        macierz_pol[i-1,j]=macierz_pol[i-1,j]+1
                if(j-1)>=0:
                    if macierz_pol[i,j-1]!=-1:
                        macierz_pol[i,j-1]=macierz_pol[i,j-1]+1
                if(i+1)<nrow:
                    if macierz_pol[i+1,j]!=-1:
                        macierz_pol[i+1,j]=macierz_pol[i+1,j]+1
                if(j+1)<ncol:
                    if macierz_pol[i,j+1]!=-1:
                        macierz_pol[i,j+1]=macierz_pol[i,j+1]+1
                if((i-1)>=0)&((j-1)>=0):
                    if macierz_pol[i-1,j-1]!=-1:
                        macierz_pol[i-1,j-1]=macierz_pol[i-1,j-1]+1
                if((i-1)>=0)&((j+1)<ncol):
                    if macierz_pol[i-1,j+1]!=-1:
                        macierz_pol[i-1,j+1]=macierz_pol[i-1,j+1]+1
                if((i+1)<nrow)&((j-1)>=0):
                    if macierz_pol[i+1,j-1]!=-1:
                        macierz_pol[i+1,j-1]=macierz_pol[i+1,j-1]+1
                if((i+1)<nrow)&((j+1)<ncol):
                    if macierz_pol[i+1,j+1]!=-1:
                        macierz_pol[i+1,j+1]=macierz_pol[i+1,j+1]+1
    return macierz_pol
def call_func(func,arg1):
    return lambda: func(arg1)
def call_func2(func,arg1,arg2,arg3):
    return lambda: func(arg1,arg2,arg3)
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
import numpy as np
import os
class Saper(QtGui.QWidget):
    
    def __init__(self):
       
        super(Saper, self).__init__()
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        self.menu_bar=QtGui.QMenuBar(self)
        file_menu=self.menu_bar.addMenu('File')
        help_menu=self.menu_bar.addMenu('Help')
        exit_action=QtGui.QAction('Exit',self)
        options_action=QtGui.QAction('Options',self)
        about_action=QtGui.QAction('About',self)
        file_menu.addAction(options_action)
        file_menu.addAction(exit_action)
        help_menu.addAction(about_action)
        exit_action.triggered.connect(self.close)
        about_action.triggered.connect(self.helpTrigger)
        options_action.triggered.connect(self.OptionTrigger)
        self.nrow=9
        self.ncol=9
        self.liczba_bomb=10
        self.tworz_tbl(self.nrow,self.ncol,self.liczba_bomb)
        self.setGeometry(200, 200,1000,1000)
        self.setWindowTitle('Saper')
        self.show() 
    def tworz_tbl(self,nrow,ncol,liczba_bomb):
        if ('self.lbl' in locals())|('self.lbl' in globals()):
            for m in range(len(self.lbl)):
                if ('self.buttons' in locals())|('self.buttons' in globals()):
                    if self.buttons[m]!=None:
                        self.grid.removeWidget(self.buttons[m])
                        self.buttons[m].deleteLater()
                        self.buttons[m]=None
                if ('self.lbl_czy' in locals())|('self.lbl_czy' in globals()):
                    if  self.lbl_czy[m]!=None:
                        self.grid.removeWidget(self.lbl_czy[m])
                        self.lbl_czy[m].deleteLater()
                        self.lbl_czy[m]=None
        self.macierz_pol=macierz(nrow,ncol,liczba_bomb)
        self.licznik=liczba_bomb
        self.licznik_prawd=0
        self.lbl_bombs = QtGui.QLabel('l.bomb '+str(self.licznik))
        self.grid.addWidget(self.lbl_bombs,0,ncol-1)
        positions = [(p,q) for p in range(nrow) for q in range(ncol)]
        self.buttons=[None]*nrow*ncol
        self.lbl=[None]*nrow*ncol
        self.lbl_czy=[None]*nrow*ncol
        for position in positions:
            i=position[0]
            j=position[1]
            self.buttons[(i)*ncol+j] = QtGui.QPushButton('')
            self.lbl[(i)*ncol+j] = QtGui.QLabel(str(self.macierz_pol[i,j]))
            self.buttons[(i)*ncol+j].clicked.connect(call_func2(self.myfunc,position,ncol,nrow))
            self.buttons[(i)*ncol+j].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.buttons[(i)*ncol+j].customContextMenuRequested.connect(call_func2(self.buttonClicked,position,ncol,nrow))
            self.grid.addWidget(self.buttons[(i)*self.ncol+j],i+1,j+1)
    def helpTrigger(self):
        super(Example, self).__init__()
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        self.helps1 = QtGui.QLabel('Klasyczny saper')
        self.helps2 = QtGui.QLabel('Do wykrycia okreslona liczba bomb')
        self.helps3 = QtGui.QLabel('Liczby w polach okreslaja ile bomb w sasiedztwie')
        self.helps4 = QtGui.QLabel('Prawym oznaczamy czy bomba, lewym odkrywamy pola')
        
        self.grid.addWidget(self.helps1,0,0)
        self.grid.addWidget(self.helps2,1,0)
        self.grid.addWidget(self.helps3,2,0)
        self.grid.addWidget(self.helps4,3,0)
        self.setGeometry(200,200,200,200)
        self.setWindowTitle('Help')
        self.show() 
    def OptionTrigger(self):
        self.opt=Options()
        if self.opt.exec_():
            self.ustpoz(self.opt.krotka)
    def ustpoz(self,position):
        self.tworz_tbl(position[0],position[1],position[2])
        self.update()
    def buttonClicked(self,position,ncol,nrow):
        i=position[0]
        j=position[1]
        sender=self.sender()
        word=sender.text()
        if QtGui.qApp.mouseButtons() & QtCore.Qt.RightButton:
            self.grid.removeWidget(self.buttons[(i)*ncol+j])
            self.buttons[(i)*ncol+j].deleteLater()
            if word=='':
                self.buttons[(i)*ncol+j] = QtGui.QPushButton('bomb')
                self.licznik=self.licznik-1
                self.grid.removeWidget(self.lbl_bombs)
                self.lbl_bombs.deleteLater()
                self.lbl_bombs = QtGui.QLabel('l.bomb '+str(self.licznik))
                self.grid.addWidget(self.lbl_bombs,0,ncol-1)
                if self.lbl[(i)*ncol+j].text()=='-1':
                    self.licznik_prawd=self.licznik_prawd+1
                if self.licznik_prawd==self.liczba_bomb:
                    self.lbl_wygr = QtGui.QLabel('You win!!!')
                    self.lbl_wygr.setFont(QtGui.QFont('SansSerif',30))
                    self.grid.addWidget(self.lbl_wygr,0,4,0,4)
            if word=='bomb':
                self.buttons[(i)*ncol+j] = QtGui.QPushButton('?')
                self.licznik=self.licznik+1
                self.grid.removeWidget(self.lbl_bombs)
                self.lbl_bombs.deleteLater()
                self.lbl_bombs = QtGui.QLabel('l.bomb '+str(self.licznik))
                self.grid.addWidget(self.lbl_bombs,0,self.ncol-1)
                if self.lbl[(i)*ncol+j].text()=='-1':
                    self.licznik_prawd=self.licznik_prawd-1
            if word=='?':
                self.buttons[(i)*ncol+j] = QtGui.QPushButton('')    
            self.buttons[(i)*ncol+j].clicked.connect(call_func2(self.myfunc,position,ncol,nrow))
            self.buttons[(i)*ncol+j].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.buttons[(i)*ncol+j].customContextMenuRequested.connect(call_func2(self.buttonClicked,position,ncol,nrow))
            self.grid.addWidget(self.buttons[(i)*ncol+j],i+1,j+1)
    def myfunc(self,position,ncol,nrow):
        i=position[0]
        j=position[1]
        def ktore_zero(i,j,lista):
            if (self.macierz_pol[i,j]>0)|(self.macierz_pol[i,j]==-1):
                lista.append((i,j))
                return lista
            if self.macierz_pol[i,j]==0:
                lista.append((i,j))
                if((i-1)>=0) & ((i-1,j) not in lista):
                    lista=ktore_zero(i-1,j,lista)
                if((j-1)>=0)&((i,j-1) not in lista):
                    lista=ktore_zero(i,j-1,lista)
                if((i+1)<nrow)&((i+1,j) not in lista):
                    lista=ktore_zero(i+1,j,lista)
                if((j+1)<ncol)&((i,j+1) not in lista):
                    lista=ktore_zero(i,j+1,lista)
                if(((i-1)>=0)&((j-1)>=0))&((i-1,j-1) not in lista):
                    lista=ktore_zero(i-1,j-1,lista)    
                if(((i-1)>=0)&((j+1)<ncol))&((i-1,j+1) not in lista):
                    lista=ktore_zero(i-1,j+1,lista) 
                if(((i+1)<nrow)&((j-1)>=0))&((i+1,j-1) not in lista):
                    lista=ktore_zero(i+1,j-1,lista) 
                if(((i+1)<nrow)&((j+1)<ncol))&((i+1,j+1) not in lista):
                    lista=ktore_zero(i+1,j+1,lista) 
                return lista
        lista=[]
        lista=ktore_zero(i,j,lista)
        for elements in lista:
            k=elements[0]
            l=elements[1]
            if self.buttons[(k)*ncol+l]!=None:
                self.grid.removeWidget(self.buttons[(k)*ncol+l])
                self.buttons[(k)*ncol+l].deleteLater()
                self.grid.addWidget(self.lbl[(k)*ncol+l],k+1,l+1)
                self.lbl_czy[(k)*ncol+l]=1
                self.buttons[(k)*ncol+l]=None 
        if self.lbl[(i)*ncol+j].text()=='-1':
            self.lbl_przeg = QtGui.QLabel('Game Over')
            self.lbl_przeg.setFont(QtGui.QFont('SansSerif',30))
            self.grid.addWidget(self.lbl_przeg,0,4,0,4)
            for lbls in self.lbl:
                if lbls.text()=='-1':
                    if self.buttons[self.lbl.index(lbls)]!=None:
                        self.grid.removeWidget(self.buttons[self.lbl.index(lbls)])
                        self.buttons[self.lbl.index(lbls)].deleteLater()
                        self.lbl_czy[self.lbl.index(lbls)]=1
                        self.grid.addWidget(self.lbl[self.lbl.index(lbls)],np.floor(self.lbl.index(lbls)/ncol)+1,self.lbl.index(lbls)-np.floor(self.lbl.index(lbls)/9)*9+1)
                        self.buttons[self.lbl.index(lbls)]=None 
class Options(QtGui.QDialog):
    def __init__(self):
        super(Options, self).__init__()
        self.krotka=(16,16,40)
        self.grid = QtGui.QGridLayout()
        self.setLayout(self.grid)
        self.opis = QtGui.QLabel('Ustaw wielkosc planszy')
        self.small = QtGui.QPushButton('9x9')
        self.medium = QtGui.QPushButton('16x16')
        self.high = QtGui.QPushButton('16x30')
        self.medium.clicked.connect(call_func(self.dajkrotke,(16,16,40)))
        self.small.clicked.connect(call_func(self.dajkrotke,(9,9,10)))
        self.high.clicked.connect(call_func(self.dajkrotke,(16,30,99)))
        self.grid.addWidget(self.opis,0,0)
        self.grid.addWidget(self.small,1,1)
        self.grid.addWidget(self.medium,1,2)
        self.grid.addWidget(self.high,1,3)
        self.setGeometry(200,200,200,200)
        self.setWindowTitle('Options')
        self.show()
    def dajkrotke(self,krotka):
        self.krotka=krotka
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Saper()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

