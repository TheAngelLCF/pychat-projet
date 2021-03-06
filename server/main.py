# Main file on Server
import background as bg
import os
import sys
from datetime import datetime
from time import time

class Server:
    def __init__(self, database: str, logs: bool):
        self.__database = database
        self.__logs = logs
        self.__owner_account = ['0000000000']
        self.clear_folder('./receive/')
        self.clear_folder('./send/')
        
    def clear_folder(self, folder: str):
        for elt in os.listdir(folder):
            os.remove(folder + elt)
        
    def set_database(self, database): self.__database = database
    def set_logs(self, logs): self.__logs = logs
    
    def fonction(self, cmd: str, args: tuple, author: str):
        returned = None
        if(cmd == 'make_client'):
            returned = bg.make_client(args[0], args[1], args[2])
        elif(cmd == 'good_login'):
            returned = bg.good_login(args[0], args[1])
        elif(cmd == 'get_id'):
            returned = bg.get_id(args[0], args[1])
        elif(cmd == 'make_channel'):
            returned = bg.make_channel(args[0], args[1], author=author)
        elif(cmd == 'stop'):
            idd = bg.get_id(author)
            if(idd in self.__owner_account):
                returned = 'stop_all_the_server'
            
        
        return returned
    
    def converte_file(self, name_of_files: str):
        dico = {'return_name': '',
                'author': '',
                'commande': '',
                'args': []}
        
        with open('receive/' + name_of_files, 'r', encoding='UTF-8') as file:
            dico['return_name'] = file.readline()[:-1]
            dico['author'] = file.readline()[:-1]
            temps = file.readline()
            
        command = ''
        args = []
        arg = ''
        x = True
        
        for elt in temps:
            if(x):
                if(elt == '|'): x = False
                else: command += elt
            else:
                if(elt == '/'):
                    args.append(arg)
                    arg = ''
                else:
                    arg += elt
        args.append(arg)
        dico['commande'] = command
        dico['args'] = tuple(args)
        os.remove('receive/' + name_of_files)
        return dico
    
    def create_send_file(self, file_name: str, reponse: any):
        with open('send/' + file_name , 'a', encoding='UTF-8') as file:
            file.write(str(reponse))
        return True
        
        
    def run(self):
        print('D??marrage du serveur !')
        start = time()
        x = True
        while x:
            now = time()
            if(start + 0.5 < now):
                start = now
                files_getted = os.listdir('receive')
                if(files_getted != []):
                    for files in files_getted:
                        print('Quelques choses de trouv?? a ' + str(datetime.now()))
                        dico_file = self.converte_file(files)
                        returned = self.fonction(dico_file['commande'], dico_file['args'], dico_file['author'])
                        if(returned =='stop_all_the_server'): x = False
                        elif(self.create_send_file(dico_file['return_name'], returned)): pass
                        else: print('Erreur avec le fichier ' + dico_file['return_name'])
                        
if __name__ == '__main__' or input('MDP ==> ') == 'bp2022pjt':
    server = Server('db_server.db', True)
    server.run()