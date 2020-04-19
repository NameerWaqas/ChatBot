from flask import Flask, render_template, request, redirect
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
from nltk import word_tokenize
from spellchecker import SpellChecker

app = Flask(__name__)

@app.route('/')
def handleHome():
    return render_template('index.html')

@app.route('/fetchvalue',methods=['GET','POST'])
def handelFetchValue():
    if request.method=='POST':
        data = request.form['message']
        mainList = word_tokenize(data)        
        spelledSent = ""
        spellCheck = SpellChecker()
        for word in mainList:
            spelledSent += str(spellCheck.correction(word))+" "
        try:
            resp = botMath.get_response(spelledSent)
        except:
            try:
                if mainList.count('time'):
                    resp = botTime.get_response(spelledSent)
                    return {'key':str(resp)}
                else:
                    try:
                        resp = botCustom.get_response(spelledSent)
                        if resp != 'nothing matched':
                            return {'key':str(resp)}
                        else:
                            return {'key':'Nothing to response, please try another way'}
                    except:
                        return {'key':'Nothing to response, please try another way'}
            except:
                return {'key':'Nothing to response, please try another way'}
        else:
            return {'key':str(resp)}
        
        
        
        
        
if __name__=="__main__":
    botMath = ChatBot('botMath',
                      logic_adapters=[
                          {
                              'import_path':'chatterbot.logic.MathematicalEvaluation'
                          }                          
                      ],
                        trainer = 'chatterbot.trainers.ListTrainer'
                      )
    botTime = ChatBot('botTime',
                      logic_adapters=[
                          {
                              'import_path':'chatterbot.logic.TimeLogicAdapter'
                          }
                      ],
               trainer = 'chatterbot.trainers.ListTrainer')
    botCustom = ChatBot('botCustom',
                        logic_adapters=[{
                            'import_path':'chatterbot.logic.BestMatch',
                            'default_response':'nothing matched',
                        }],
               trainer = 'chatterbot.trainers.ListTrainer'
                        ) 
    customDialogs =[[
        'Tell me about your self','I am a chat bot,here to provide you service.',
        'what services do you provide','I am responsible to give you information about my master.',
        'who is your master','Nameer Waqas'
        ],[
            'What is your name?','Nameer Bot','why are you here','I am a chat bot,here to provide you service.'            
            ],[
                'Where can i find the resume?','It is on the bottom of the page.'
                ],[
                    'What functions do you perform',
                    'I can perform alot of functions like,can tellyou about Nameer Waqas can do Math,Answer G.K questions and much more',
                    'What are the skills set of your master',
                    'They are mentioned on his LinkedIn account.You can find it on: https://www.linkedin.com/in/nameerwaqas'
                    ],[
                        'On which technology you are built',
                        'I built using Python programming language and a library called Chatter Bot',
                        'Thank you',
                        'You are welcome,Please give a view to the CV, attached at bottom of page.'                        
                    ],[
                        'Where is his resume?',
                        'It is at the bottom of page.Give it a look.'
                    ],[
                        'Where is his CV?',
                        'It is at the bottom of page.Give it a look.'
                    ],['What are his soft skills?',
                       'He is a proactive and highly motivated person that works with enthusiasm.'
                       ],[
                          'Will Artificial Intelligence over take the world?',
                          'AI is something that is made to work with humans not to rule humans.'
                           
                       ],[
                           'How  can i contact to your master?',
                           'You can send him E-mail.','Please give me his email',
                           'nameerwaqas321@gmail.com.Also you can find his CV attached to the bottom of page'
                       ],[
                           'give me some information about your master',
                           'He is studying computer science at University of Karachi.',
                           'What else do you know about him.',"He is aspiring data scientist and a ML enthusiast."
                           
                       ]]
    trainer = ListTrainer(botCustom)
    for dialog in customDialogs:
        trainer.train(dialog)
    trainer = ChatterBotCorpusTrainer(botCustom)
    trainer.train('chatterbot.corpus.english')
    app.run()
