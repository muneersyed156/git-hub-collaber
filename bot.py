import json

from connection import bot

def get_current_projects():
    list_projects=json.load(open("projects.json"))
    list_projects_message=""
    for i in range(len(list_projects["projects"])):
        list_projects_message+=str(i+1)+"."+list_projects["projects"][i]['project_name']+": "+",".join(list_projects["projects"][i]['collaborators'])+"\n"
    return(list_projects_message)

def update_projects(list_projects):
    try:
        with open("projects.json","w") as json_pointer:
            json.dump(list_projects,json_pointer)
        return(1)
    except Exception as e:
        return(0)

# # @bot.message_handler(commands=['start'])
# # def send_welcome(message):
# #     if(message.text=="/start"):
# #         bot.reply_to(message, "Welcome to Git-Hub-Collabaration...!\n Currently On going Projects in this group are ... \n {}".format(get_current_projects()))
# #     elif(message.text=="/edit"):
# #         bot.reply_to(message,"Editing the projects...!")
    
@bot.message_handler(commands=["edit"])
def edit_handler(message):
    text= "Please select the project number that you would like to edit"+"\n"+get_current_projects()
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, edit_reply_project_number_handler)

def edit_reply_project_number_handler(message):
    project_number=int(message.text)
    text="Which field would you like to modify?"+"\n"+"Choose one: 1). ProjectName"+"\n"+"2). collaborators"
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, edit_project_details,project_number)
    
def edit_project_details(message,project_number):
    text="Please enter the value"
    project_field=message.text
    sent_msg = bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(sent_msg, modify_project_file,project_number,project_field)
    

def modify_project_file(message,project_number,project_field):
    list_projects=json.load(open("projects.json"))
    if(project_field=="1"):
        list_projects["projects"][project_number-1]["project_name"]=message.text
        if(update_projects(list_projects)):
            bot.send_message(message.chat.id,"Edited Successfully.. =)")
            bot.send_message(message.chat.id,"The current projects are .."+"\n"+get_current_projects())
    elif(project_field=="2"):
        list_projects["projects"][project_number-1]["collaborators"]=message.text
        if(update_projects(list_projects)):
            bot.send_message(message.chat.id,"Edited Successfully.. =)")
            bot.send_message(message.chat.id,"The current projects are .."+"\n"+get_current_projects())
    else:
        bot.send_message(message.chat.id,"Something is Wrong ...!")
    
@bot.message_handler()
def send_welcome(message):
    print(message.text)

bot.infinity_polling()