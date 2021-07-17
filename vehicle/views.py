from io import BytesIO
from logging import RootLogger
import re
import bcrypt

from datetime import datetime
from django.contrib.messages.api import error, success
from django.db.models.expressions import Exists
from django.http.response import HttpResponse
from django.shortcuts import redirect, render 
from .models import image, userreg ,fineupl,transupl
from django.contrib import messages 
from validate_email import  validate_email
from bcrypt import hashpw, checkpw
from django.contrib.auth import authenticate,login,logout
import qrcode.image.svg 
import qrcode
from django.views.generic import TemplateView
from .excp import handle_file
from django.core.files import File
import base64
from django.contrib.auth.hashers import make_password ,check_password

# from .forms import update_img
# from  .excp import tharun


from operator import itemgetter

# def logout(request):
#     print("logout called")
#     request.session['uname'] = ""
#     return login(request) , admin(request)
    # return render(request, 'in.html') 
     

# print(make_password('1234'))
# print(check_password('1234','argon2$argon2id$v=19$m=102400,t=2,p=8$bFVVVkoza3hzWGFZYWo0bjY2V25vVA$rCSCwOzY2ub8K+oVlgtQ0Q'))
def login(request):
 
    if request.method=="POST":
        try:
            userfetch=userreg.objects.get(uname=request.POST['uname'])
            print("uname=",userfetch)
            print("password=",userfetch.pwd)
            request.session['uname']=userfetch.uname
            request.session['id']=userfetch.id 
            request.session['vnumb']=userfetch.vnumb 

            if userfetch:
               flag = check_password(request.POST['pwd'],userfetch.pwd)
               uname = userfetch.uname and request.session['id']
               if flag and uname:
                 return render(request,'loged.html')
               else:
                   messages.success(request,' invalid  password  ')
            
            
              
              
            
            
            
        except userreg.DoesNotExist as e:
            
            messages.success(request,' invalid  username ')
    request.session['uname'] = ""
    return  render(request, 'in.html') 
              
    
def linking(request):
    if request.session['uname'] == "":
        messages.success(request,' login first ')
        return login(request)
        
    else :
        return render(request,'loged.html')
    

    

def userregistration(request):
    
    print("0")
    if request.method=='POST':
        
        if request.POST.get('uname') and request.POST.get('pwd') and request.POST.get('email') and request.POST.get('phone'):
            error_message= None
            print("1")
            if len(request.POST.get('uname'))<7:
                error_message = "uname must be greater than 7 character "
                print("2")
            elif userreg.objects.filter(uname=request.POST.get('uname')).exists() :
                error_message =" username already exist "  
            elif len(request.POST.get('pwd'))<7:
                error_message =" password must be greater than 7 character!"
                print("3")
            elif not validate_email(request.POST.get('email')):
                 error_message =" invalid email id "
            elif userreg.objects.filter(email=request.POST.get('email')).exists() :
                  error_message ="  email id already exist"   
            elif len(request.POST.get('phone'))!=10: 
                error_message =" invalid phone nbr "
                print("4")   
            if not error_message:
                    saverecord=userreg()
                    saverecord.uname=request.POST.get('uname')
                    saverecord.pwd=make_password(request.POST.get('pwd'))
                    saverecord.email=request.POST.get('email')
                    saverecord.phone=request.POST.get('phone')
                    print(saverecord.pwd)

                    

         
                    saverecord.save()
                    messages.success(request,'user created sucessfully')
                    return render(request,'home.html')
            else:
                    return   render(request,'home.html' , {'error' : error_message})

        
        
         
    else:
         return   render(request,'home.html')   


def forgotpw(request):
    if request.method=="POST":
        messages.success(request,'Username and Password sent to your email sucessfully')
        return render(request, 'forgotpw.html')
    else:
        return render(request,'forgotpw.html')    

def services(request):
        if request.session['uname'] == "":
           messages.success(request,' login first ')
           return login(request)
        
        else :
            data=userreg.objects.get(id=request.session['id']) 
            vno=data.vnumb
            go=" "
            print(vno)
            if (request.session['vnumb'])!="":
                messages.success(request,'VEHICLE NUMBER ALREADY UPLADED')
                return render(request,'services.html',{'vnom':vno,'go':go}) 
            else :
                 sdata = " "
                 
                 print ("showing ")
                 return render(request,'services.html',{'show': sdata}) 
          
def fine(request):
    if request.session['uname'] == "":
        messages.success(request,' login first ')
        return login(request)
        
    else :
        dis=userreg.objects.get(id=request.session['id'])
        
        dta=dis.vnumb
        print(dta)
        oba=fineupl.objects.filter(vnumber=dta)
        c=0
        for x in oba.all():
         z=int(x.fineamt)  
         c=z+c  
        print(c)
        if c == 0 :
         messages.success(request,' your vehicle has no fine record ')
         
         return render(request,'fine.html') 
        else :
             return render(request,'fine.html',{'fine':oba,'total':c,'dis':dis})  
def status(request):
    error=None
    if request.session['uname'] == "":
        messages.success(request,' login first ')
        return login(request)
        
    else :
        data=userreg.objects.get(id=request.session['id']) 
        dt=data.status
        print(dt)
        if dt == "rejected":
           rj=" dd "
           error="your documents has been rejected please reupload all the documents  "
           return render(request,'status.html',{'error':error,'rj':rj})
        elif dt == "pending":
           
           error="your documents is in pending state   "
           return render(request,'status.html',{'error':error})
        elif dt == "verified":
            messages.success(request,' your documents have been verified you can generate QR ')
            return render(request,'status.html') 
        else:
            return render(request,'status.html')        
def trans(request):
    if request.session['uname'] == "":
        messages.success(request,' login first ')
        return login(request)
        
    else :
        if request.method =='POST':
           transr=transupl()
           transr.images=request.FILES['imat'] 
           transr.vehicleno=str(request.session['vnumb'])
           transr.type=request.POST['goods']
           x=datetime.now()
           date1 = x.strftime("%d/%m/%Y %H:%M")
           transr.date=date1
           transr.save()
        elif transupl.objects.filter(vehicleno=request.session['vnumb']).exists():
             acd=transupl.objects.filter(vehicleno=request.session['vnumb']) 
             return render(request,'trans.html',{'trans':acd}) 
        acd=transupl.objects.filter(vehicleno=request.session['vnumb']) 
               
        return render(request,'trans.html',{'trans':acd}) 
                
def admin(request):

    request.session['uname']=0
    
    if request.method=="POST":
        if request.POST.get('uname') and request.POST.get('pwd'):
            if (request.POST.get('uname'))=='admin'and (request.POST.get('pwd'))=='1234':
                  request.session['uname']=1
                  
                  return redirect('admn')
            else:
                 messages.success(request,' invalid  username you are not Admin !!')
    return render(request,'admin.html') 
                
def admn(request):
    if request.method =="POST":
        if request.POST.get('search'):
        
           print(request.POST['search'])
           sch=userreg.objects.filter(uname=request.POST['search']) 
           admn.sch=str(sch)
           print(admn.sch)
           return render(request,'admin-lg.html',{'data':sch})
        elif admn.sch == "":
            messages.success(request,' NO records found !!')
            return render(request,'admin-lg.html')
        else:
                 
                 data=userreg.objects.filter(status='pending') 
                 return render(request,'admin-lg.html',{'data':data})    
    else:
            
          data=userreg.objects.filter(status='pending')
          return render(request,'admin-lg.html',{'data':data}) 
           
            

# def write_f(data,filename):
#     with open(filename,'wb') as file:
#         file.write(data)

def adminlgd(request):
     
     if request.session['uname'] == 1:
     
        
        return admn(request)
            
        
     else:
        print("fg")   
        messages.success(request,' login first ')
        return admin(request)
def uplfine(request):
     
     if request.session['uname'] == 1:
        if request.method=='POST':
            saverecord=fineupl()
            saverecord.vnumber=request.POST.get('veno')
            saverecord.cased=request.POST.get('des')
            saverecord.fineamt=request.POST.get('fine')
            x=datetime.now()
            date1 = x.strftime("%d/%m/%Y %H:%M")
            print(date1)
            saverecord.date=date1
            saverecord.save()
        return render(request,'uploadfine.html') 
        
     else:
        print("fg")   
        messages.success(request,' login first ')
        return admin(request)  
def uplcase(request):
     if request.session['uname'] == 1:
        
        return render(request,'uploadcase.html')
     else:
           
        messages.success(request,' login first ')
        return admin(request)               
def generate(request):
    data1=userreg.objects.get(id=request.session['id'])
    vn=data1.vnumb
    dt=data1.status
    print(dt)
    if request.session['uname'] == "":
        messages.success(request,' login first ')
        return login(request)
    else:
        if dt == "pending":
           error="your documents QR cannot be genetared it is in pending state " 
           return render(request,'generate.html',{'error':error}) 
        elif dt =="rejected" :
            error="your documents QR cannot be genetared your document has been rejected " 
            return render(request,'generate.html',{'error':error})     
        elif fineupl.objects.filter(vnumber=request.session['vnumb']).exists():
            error="your documents QR cannot be genetared  pay fine for vehicle "+str(vn)
            return render(request,'generate.html',{'error':error}) 
        else :
         data=userreg.objects.get(id=request.session['id']) 
         vno1=data.status
         data1=image.objects.filter(ide=request.session['id'])
         a=[]
         for dat in data1.all():
           a.append(dat.ima_filename+"="+str(vno1))
         print(a)
         im =qrcode.make(a)
         im.save("data/test.jpg")
        
        
        
        return render(request,'generate.html',{'re':im}) 

def dock(request):
    error_message=None
    kkk=" dff "
    data=userreg.objects.get(id=request.session['id'])
    dt=data.status  
    if dt == "rejected":
        erg=" "
        return render(request,'dock.html',{'erg':erg})
    elif image.objects.filter(ide=request.session['id']).exists() :     
            view=" documents already uploaded "
            return render(request,'dock.html',{'view':view})

    else:
          if request.method == "POST":
              print("hihi")
                 
              saverecord=userreg()        
              rc(request)
              lic(request)
              emi(request)
              ins(request)
              saverecord.status= userreg.objects.filter(id=request.session['id']).update(status="pending")
              
            #  
              
        #   if saverecord.ima==request.FILES['ima']:
              
              
                   
              
              

              

               
         
              error_message=" DOCUMENTS succesfully uploaded "
              
              return render(request,'dock.html',{'error':error_message}) 
              
    if request.session['uname'] == "":
        messages.success(request,' login first ')
        return login(request)
        
    else :
         return render(request,'dock.html',{'kk': kkk}) 
def reupload(request):
     rmr=image.objects.filter(ide=request.session['id']).delete()
     print("hihi")
     if request.method == "POST":
        print("hihi")
                 
        saverecord=userreg()        
        rc(request)
        lic(request)
        emi(request)
        ins(request)
        errr="  "
        saverecord.status= userreg.objects.filter(id=request.session['id']).update(status="pending") 
        error_message=" DOCUMENTS succesfully reuploaded "
        return render(request,'dock.html',{'error':error_message}) 
     else :
          errr=rmr
          print("removed")
          return render(request,'dock.html',{'kk':errr}) 
             
def viewing(request):
    if image.objects.filter(ide=request.session['id']).exists() :
       view="   "
       data=image.objects.filter(ide=request.session['id'])
       print("imas")
       return render(request,'dock.html',{'data': data,'view':view})
    else :
        messages.success(request,"no files uploaded ")
        return render(request,'dock.html') 
       
def rc(request):
 
              saverecord=image()
              saverecord.ima=request.FILES['ima']
              Rc="RC"+str(request.session['id'])
              saverecord.ima_filename=Rc
              saverecord.ide=request.session['id']
              if image.objects.filter(ima_filename=Rc).exists() :
                messages.success(request,'RC file exist')
              else: 
                  saverecord.save()
                  print("1")
                  
                  return(request) 
def ins(request):
        #   fdfdffdfd
              saverecord=image()
              saverecord.ima=request.FILES['ima1']
              insurance="INSURANCE"+str(request.session['id'])
              saverecord.ima_filename=insurance
              saverecord.ide=request.session['id']
              if image.objects.filter(ima_filename=insurance).exists() :
                messages.success(request,' INSURANCE file exist')
              else:
                  saverecord.save()
                  print("2") 
                  
                  return(request)           
def lic(request):
    
              saverecord=image()
              saverecord.ima=request.FILES['ima2']
              insurance="LICENCE"+str(request.session['id'])
              saverecord.ima_filename=insurance
              saverecord.ide=request.session['id']
              if image.objects.filter(ima_filename=insurance).exists() :
                messages.success(request,' LICENCE file exist')
              else: 
              
                 saverecord.save() 
                 print("3") 
                 return(request)    
def emi(request):
    
              saverecord=image()      
              saverecord.ima=request.FILES['ima3']
              emission="EMISSION"+str(request.session['id'])
              saverecord.ima_filename=emission
              saverecord.ide=request.session['id']
              if image.objects.filter(ima_filename=emission).exists() :
                  messages.success(request,'EMISSION file exist')
              else:
                
                 saverecord.save()
                 print("4")
                 return(request)

def vnumber(request):
    data=userreg.objects.get(id=request.session['id'])
    vno=data.vnumb
    inn=" " 
    error_message=None
    if request.method=='POST':
        
            if userreg.objects.filter(vnumb=request.POST.get('v-no')).exists():
                error_message="CHECK UR V-NO !!"
                return render(request,'services.html',{'error':error_message,'vnom':vno})
            else:
                 if data.vnumb == "":
                     userreg.objects.filter(id=request.session['id']).update(vnumb=request.POST.get('v-no'))
                     
                     messages.success(request,'V-NUMBER UPLOADED ')
                     return render(request,'services.html',{'vnom':vno,'inn':inn}) 
                
                 else:
                    messages.success(request,'NOT REQUIRED')
                    return render(request,'services.html',{'vnom':vno})
    else : 
         if data.vnumb == "":        
           return render(request,'services.html',{'vnom':vno})
def udata(request,unam):
    print(unam)
    file = userreg.objects.get(uname=unam)
    udata.unam=file.id
    if request.session['uname'] == "":
           messages.success(request,' login first ')
           return login(request)
    else:      
     file = userreg.objects.get(uname=unam) 
     print(file.id) 
     udata.unam=file.id
     veri=image.objects.filter(ide=file.id) 
     rej= image.objects.filter(ide=file.id)          
     return render(request,'admin-lg.html',{'file':file,'veri':veri,'rej':rej}) 
def verify(request):
       saverecord=userreg()  
       saverecord.status= userreg.objects.filter(id=udata.unam).update(status="verified")
       print("verified")
       print(udata.unam)
       return  admn(request)
def reject(request):
       saverecord=userreg()  
       saverecord.status= userreg.objects.filter(id=udata.unam).update(status="rejected")
       print("rejected")
       print(udata.unam)
       return  admn(request)
def payfine(request):
     x="  "
     return render(request,'fine.html',{'card':x})    
def clrfine(request):
     fineupl.objects.filter(vnumber=request.session['vnumb']).delete()     
     messages.success(request,'fine payment successful you can generate QR ')
     return render(request,'fine.html') 






