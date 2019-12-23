#you should have installed mysql-connector-python
#get the sql dictionary file and insert it on your own server 
#most of the things like sleep are added because i like the way it looks :)
import mysql.connector
from time import sleep
from difflib import get_close_matches
import os

def ask_for_input():
    print('Loading english dictionary!')
    sleep(0.5)
    print('#####################')
    word = input ( 'Please input a word:' ).capitalize()
    return word

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def translate_word(some_word):
    print('.................')
    print('Connecting to the SQL database!......',end=' ')
    sleep(0.5)
    print ( 'Translating........' )
    
    connection = mysql.connector.connect (host='ip_of_the_server', database='name_of_database', user='some_user',password='pass')
    cursor = connection.cursor ( )
    cursor.execute ( f"SELECT definition FROM entries.entries WHERE word = '{some_word}';" )
    records = cursor.fetchall ( )
    sleep(0.5)
    if records:
        print('Translated!')
        sleep ( 0.1 )
        cursor.close ( )
        connection.close ( )
        sleep(0.1)
        print('Connection closed!')
        print('..................')
        return records
    else:
        print('Word not found!',end=' ')
        sleep(0.6)
        print('Searching for the closest match.....')
        cursor.execute(f"SELECT word FROM entries.entries WHERE word LIKE '{some_word[:len(some_word)-1]}%';")
        records = cursor.fetchall()
        for x in range(len(records)):
            for y in range(len(records[x])):
                records.insert ( x, records[x][y] )
                records.pop(x+1)
        sleep(0.4)
        close = get_close_matches(some_word,records)[0]
        if close:
            print('Match found!')
        else:
            print('Nothing has been found!')
        sleep ( 0.1 )
        cursor.close ( )
        connection.close ( )
        sleep ( 0.1 )
        print ( 'Connection closed!' )
        print ( '..................' )
        return close

def print_all(transl):
    print('##############################\n')
    sleep(0.5)
    if type(transl) is list:
        for x in range(len(transl)):
            for y in range(len(transl[x])):
                print('Meaning '+str(x+1)+':', transl[x][y].replace('\n',''))
    elif type(transl) is str:
        print(f'Do you mean the word "{transl.lower()}"?')
    else:
        print('THERE IS NO SUCH WORD!\n')
    print('###############################')


def restart():
    print ( '------------------------------' )
    choice = input ( 'Type "y" to type another word or "n" to quit:' )
    if choice.lower () != 'y' and choice.lower ( ) != 'n':
        return restart ()
    if choice.lower () == 'y':
        print('Lets try againg!')
        sleep(0.3)
        return dictionary ()
    else:
        print('Thank you for using this app!')
        quit ( )




def dictionary():
    cls()
    word = ask_for_input()
    translated = translate_word(word)
    print_all(translated)
    restart()

dictionary()








