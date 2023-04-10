from fileinput import filename
import openai 

import pyperclip as pc



openai.api_key="apikey"
# completion=openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role":"user","content":'''summarise into 100 words\n
#     Afew years ago, a computer scientist named Yejin Choi gave a presentation at an artificial-intelligence conference in New Orleans. On a screen, she projected a frame from a newscast where two anchors appeared before the headline “cheeseburger stabbing.” Choi explained that human beings find it easy to discern the outlines of the story from those two words alone. Had someone stabbed a cheeseburger? Probably not. Had a cheeseburger been used to stab a person? Also unlikely. Had a cheeseburger stabbed a cheeseburger? Impossible. The only plausible scenario was that someone had stabbed someone else over a cheeseburger. Computers, Choi said, are puzzled by this kind of problem. They lack the common sense to dismiss the possibility of food-on-food crime.
# For certain kinds of tasks—playing chess, detecting tumors—artificial intelligence can rival or surpass human thinking. But the broader world presents endless unforeseen circumstances, and there A.I. often stumbles. Researchers speak of “corner cases,” which lie on the outskirts of the likely or anticipated; in such situations, human minds can rely on common sense to carry them through, but A.I. systems, which depend on prescribed rules or learned associations, often fail.
# By definition, common sense is something everyone has; it doesn’t sound like a big deal. But imagine living without it and it comes into clearer focus. Suppose you’re a robot visiting a carnival, and you confront a fun-house mirror; bereft of common sense, you might wonder if your body has suddenly changed. On the way home, you see that a fire hydrant has erupted, showering the road; you can’t determine if it’s safe to drive through the spray. You park outside a drugstore, and a man on the sidewalk screams for help, bleeding profusely. Are you allowed to grab bandages from the store without waiting in line to pay? At home, there’s a news report—something about a cheeseburger stabbing. As a human being, you can draw on a vast reservoir of implicit knowledge to interpret these situations. You do so all the time, because life is cornery. A.I.s are likely to get stuck.
# Oren Etzioni, the C.E.O. of the Allen Institute for Artificial Intelligence, in Seattle, told me that common sense is “the dark matter” of A.I. It “shapes so much of what we do and what we need to do, and yet it’s ineffable,” he added. The Allen Institute is working on the topic with the Defense Advanced Research Projects Agency (darpa), which launched a four-year, seventy-million-dollar effort called Machine Common Sense in 2019. If computer scientists could give their A.I. systems common sense, many thorny problems would be solved. As one review article noted, A.I. looking at a sliver of wood peeking above a table would know that it was probably part of a chair, rather than a random plank. A language-translation system could untangle ambiguities and double meanings. A house-cleaning robot would understand that a cat should be neither disposed of nor placed in a drawer. Such systems would be able to function in the world because they possess the kind of knowledge we take for granted.'''}]
# )
# print(completion.choices[0].message.content) 

UPLOAD_FOLDER = r'C:\\Users\\Acer\\Desktop\\reactjs\\summari'

ALLOWED_EXTENSIONS = {'txt'}

from flask import Flask, render_template, request,send_file,redirect,url_for,copy_current_request_context
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload',methods=["Get","Post"])
def upload_file(): 
   output=""
   if(request.method == 'POST' and request.form.get("input")!="" ):
       text=str(request.form.get("input"))
       percentage=int(request.form.get("words"))
       txt=text.split(" ")
       num_of_words=len(txt)
       to_compress=(percentage*num_of_words)/100
       completion=openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{"role":"user","content":f'''summarise into { to_compress} \n{text}'''}] ) 
       output=completion.choices[0].message.content



   if request.method == 'POST' and request.form.get("input")=="" :
      f = request.files['file'] 
      f.save(f"summari/{secure_filename(f.filename)}")  
      with open(f"summari/{secure_filename(f.filename)}","rb") as data:
         item=data.read() 
         item = item.decode('utf-8', 'ignore')
      
      percentage=int(request.form.get("words"))
      txt=item.split(" ")
      num_of_words=len(txt)
      to_compress=(percentage*num_of_words)/100
      completion=openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[{"role":"user","content":f'''summarise into { to_compress} \n{item}'''}] ) 
      output=completion.choices[0].message.content  
   pc.copy(output)

   
  

  
     

   
   return render_template('uploader.html',output=output)
  
@app.route("/download/<output>",methods=["Get","post"])	
def download(output): 
   with open("summari.txt","w") as f:
      f.writelines(output) 
      f.close()
   return send_file( "summari.txt",as_attachment=True)



@app.route("/clear",methods=["Get","post"])	
def clear(): 
   
   return redirect(url_for("upload_file"))


  

if __name__ == '__main__':
   app.run(debug = True)
