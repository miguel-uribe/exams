# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 09:31:55 2016

@author: miguelurla
"""

import random
import numpy as np

## The exam generating function

def genExam(Examen,QDB,Themes,N,diffrange):
    diff=0;
    while(diff < N*diffrange[0] or diff > N*diffrange[1]):  #generate exams until the difficulty is reached
        Examen.questions=[]       
        questions=random.sample(QDB,len(QDB))
        n=0
        diff=0
        i=0
        while(n<N):
            if questions[i].chapterID in Themes:
                Examen.addQuestion(questions[i])
                n=n+1
                diff=questions[i].difficulty+diff
            i=i+1
    Examen.printExam()
    message='Generated an exam with difficulty'+'%.2f'%diff
    print(message)

## The exam generating function

def genExamwithList(Examen,QDB,qList):
    Examen.questions=[]
    questions=[]
    diff=0
    for question in QDB:
        if question.ID in qList:
            questions.append(question)
            diff=diff+question.difficulty
    rquestion=random.sample(questions,len(questions))
    for question in rquestion:
        Examen.addQuestion(question)
    Examen.printExam()
    message='Generated an exam with difficulty'+'%.2f'%diff
    print(message)



## The rounding formatting function
def roundformat(n,unit):
    if n==0:
        stringout='0'
    else:
        exp=int(np.floor(np.log10(np.abs(n))))
        value=n/10**exp
        if exp==0:
            stringout=r'$'+'%.2f'%n+'\,'+unit+r'$'
        elif exp==1:
            stringout=r'$'+'%.1f'%n+'\,'+unit+r'$'
        elif exp==-1:
            stringout=r'$'+'%.3f'%n+'\,'+unit+r'$'
        elif exp==2:
            stringout=r'$'+'%.0f'%n+'\,'+unit+r'$'
        else:
            stringout=r'$'+'%.2f'%value+r'\times 10^{'+'%d'%exp+r'}\,'+unit+r'$'
    return stringout        
        
class cAnswer:
    "This is the answer class, it contains a text and wether the answer is true or not"
    def __init__(self, text, true):
        self.text=text
        self.true=true

class cQuestion:
    """This is the question class, it contains the text, the variables and the options of each question element in the database"""
    n=0;   #The number of questions
    def __init__(self, chapterID,difficulty):
        self.answers=[]
        self.variables=[]
        self.values=[]
        self.ID=cQuestion.n
        self.chapterID=chapterID
        self.difficulty=difficulty
        self.diffProf=difficulty
        cQuestion.n=cQuestion.n+1
        self.double=False
        self.Ntest=0
        
    def setvalues(self):
        self.values=[]
        for i in range(len(self.variables)):
            self.values.append(random.choice(np.arange(self.variables[i][0],self.variables[i][1],self.variables[i][2])))
        
    def gettext(self):
        #Unsorting the answers
        ansaux=random.sample(self.answers,len(self.answers))
        qstring='\n'+r'\item '+self.text+'\n'
        if self.double==True:
            qstring=qstring+'\n'+r'\begin{multicols}{2}'+'\n'
        qstring=qstring+'\n'+r'\begin{enumerate}'+'\n'
        qstringans=qstring
        for ans in ansaux:
            qstring=qstring+r'\item '+ans.text+'\n'
            if ans.true:
                qstringans=qstringans+r'\item \underline{'+ans.text+r'}'+'\n'
            else:
                qstringans=qstringans+r'\item '+ans.text+'\n'
        qstring=qstring+r'\end{enumerate}'+'\n'
        qstringans=qstringans+r'\end{enumerate}'+'\n'
        if self.double==True:
            qstring=qstring+'\n'+r'\end{multicols}'+'\n'
            qstringans=qstringans+'\n'+r'\end{multicols}'+'\n'
        qstringans=qstringans+'ID: '+'%d'%self.ID+'.\qquad Diff:'+'%.2f'%self.difficulty
        return [qstring,qstringans]
        
    def setquestion(self):
        if len(self.variables):
            self.setvalues()
        self.setText()
        self.setAnswers()
        
    def incStat(self, results, ntest):
        if self.Ntest==0:
            self.Ntest=ntest
            self.difficulty=self.diffProf/3.+(2./3.)*results
            self.diffStat=results
        else:
            self.diffStat=1.*(self.diffStat*self.Ntest+ntest*results)/1./(self.Ntest+ntest)
            self.Ntest=self.Ntest+ntest
            self.difficulty=self.diffProf/3.+(2./3.)*self.diffStat


class cExam:
    "This is the exam class, each exam consists of an instance of this class"
    def __init__(self,filename,classname,examname,date):
        self.classname=classname
        self.examname=examname
        self.date=date
        self.filename=filename+'.tex'
        self.filenameanswers=filename+'_answers.tex'
        self.genintro()
        self.questions=[]
    
    def genintro(self):
        with open('Intro1.tex', 'r') as myfile:
            self.examtex=myfile.read()
        self.examtex=self.examtex+'\n'+self.classname+r'\\'+'\n'
        self.examtex=self.examtex+self.examname+r'\\'+'\n'
        self.examtex=self.examtex+r'Docente: Miguel Angel Uribe\\'+'\n'
        self.examtex=self.examtex+self.date+r'\\'+'\n'        
        with open('Intro2.tex', 'r') as myfile:
            self.examtex=self.examtex+myfile.read()
            self.examanswers=self.examtex
        
    def genbody(self):
        for question in self.questions:
            question.setquestion()
            [string,stringans]=question.gettext()
            self.examtex=self.examtex+string
            self.examanswers=self.examanswers+stringans
            
    def genoutro(self):
        with open('Outro1.tex', 'r') as myfile:
            string=myfile.read()
            self.examtex=self.examtex+string
            self.examanswers=self.examanswers+string
        self.examtex=self.examtex+'\n'+r'\end{document}'  
        self.examanswers=self.examanswers+'\n'+r'\end{document}'  
                
    def printExam(self):
        self.genintro()
        self.genbody()
        self.genoutro()
        f1=open(self.filename, 'w+')
        f2=open(self.filenameanswers, 'w+')
        print >>f1, self.examtex
        print >>f2, self.examanswers
        f1.close
        f2.close
    
    def addQuestion(self,question):
        self.questions.append(question)
        
        
            
        
                