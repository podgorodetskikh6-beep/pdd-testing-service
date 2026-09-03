# class  Question:
#     def __init__(self, text, variants,answer,image):
#         self.text=text
#         self.answer=answer
#         self.variants=variants
#         self.image=image
#     def check(self,user_answ):
#         return user_answ == self.answer
# class Users:
#     def __init__(self,name,results):
#         self.name=name
#         self.results=results
#     #def get_best_result(self):
#         #return 'Текущий лучший результат:', max(self.results)
# class Test:
#     def __init__(self,quests):
#         self.quests=quests
#         self.score=0
#         self.current_ind=0
#     def get_question(self):
#         return self.quests[self.current_ind]
#     def next_question(self):
#         self.current_ind += 1
#     def answer(self,user_answ):
#         question=self.get_question()
#         if question.check(user_answ):
#             self.score+=1
#         self.next_question()
#     def is_finished(self):
#         return self.current_ind >= len(self.quests)
#     def result(self):
#         print('результат теста:', self.score)
#         print('всего вопросов в тесте:', len(self.quests))
#
# from tkinter import *
# from tkinter import ttk
# import json
#
# def load_question(path): #загрузка файлов с вопросами
#     with open(path,'r', encoding='utf-8') as f:
#         data=json.load(f)
#     questions=[]
#     for e in data['questions']:
#         q=Question(e["text"],
#             e["variants"],
#             e["answer"],
#             e["image"]
#         )
#         questions.append(q)
#
#     return questions
#
# questions= load_question('ticket1.json')
# test1=Test(questions)
# text_q=test1.get_question().text
# print(text_q)
# q=test1.get_question()
# for i,v in enumerate(q.variants,1):
#     print(f"{i}. {v}")
# test1.answer('1')
# test1.result()
#
# root=Tk()
# root.title("Тест ПДД")
# root.geometry('500x700')
# lab1=Label(text='Имя:')
# entry1=Entry(root,bg='light blue',bd=4,font='Ariel 14')
# lab1.pack()
# entry1.pack()
# root.mainloop()
#
#
#
#
#
