from flask import Flask,render_template,request 
import utility
app= Flask(__name__)

@app.route("/",methods=["GET","POST"])
def home():
    return render_template("home.html",ans_string="")

@app.route("/home" ,methods=["GET","POST"])
def home2():
    p=utility.get_text(request.form.get('query_string'))
    prob=p[0]
    r=p[1]
    r/=4

    prob1=utility.make_text(prob)
    
    prob2=utility.generate_summary(prob,int(r))
    ans_string=str(prob)
    return render_template("home.html",ans_string=ans_string,ans_string1=prob1,ans_string2=prob2)

if __name__=="__main__":
    app.run()
#https://www.youtube.com/watch?v=GEOioIBPlTE