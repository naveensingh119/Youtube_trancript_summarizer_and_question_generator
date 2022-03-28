from flask import Flask,render_template,request 
import utility
app= Flask(__name__)

@app.route("/",methods=["GET","POST"])
def home():
    return render_template("home.html",ans_string="")

@app.route("/home" ,methods=["GET","POST"])
def home2():
    prob=utility.get_text(request.form.get('query_string'))
    ans_string=str(prob)
    return render_template("home.html",ans_string=ans_string)

if __name__=="__main__":
    app.run()
#https://www.youtube.com/watch?v=GEOioIBPlTE