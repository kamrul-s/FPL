from django.shortcuts import render
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
# Create your views here.
def updateresult(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    return render(request,'updateresult.html')
def admininsert(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    return render(request,'admininsert.html')
def loginasadminpage(request):
    count = []
    email = request.POST['email']
    password = request.POST['pass']
    #password = make_password(password)
    cursor = connection.cursor()
    if(cursor):
        if password != '':
            query = "SELECT PASSWORD FROM ADMIN_USERS WHERE EMAIL = %s"
            cursor.execute(query,[email])
            count = cursor.fetchall()
            if(len(count)<1) :
                return render(request,'adminlogin.html')
            encodpass=(''.join(map(str,count[0])))
            if check_password(password,encodpass):
                    adminuser=request.session['adminuser'] = email
                    return render(request,'admininsert.html')
            return render(request,'adminlogin.html')
    cursor.close()
def userlogin(request):
    if 'adminuser'  in request.session:
        del request.session['adminuser']
    return render(request,'index.html')
def addadmin(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    return render(request,'addadmin.html')
def insertplayer(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    count = []
    Fname = request.POST['Fname']
    Lname = request.POST['Lname']
    countr = request.POST['country']
    playpos = request.POST['playpos']
    Tname = request.POST['Tname']
    prc = request.POST['price']
    cursor = connection.cursor()
    query = "SELECT * FROM TEAM_INFO WHERE TEAM_NAME = %s"
    cursor.execute(query,[Tname])
    count = cursor.fetchall()
    cursor.close()
    if(len(count)<1) :
        return render(request,'admininsert.html')
    else :
        cursor = connection.cursor()
        query = "SELECT MAX(PLAYER_ID) FROM PLAYER_INFO"
        cursor.execute(query)
        count = cursor.fetchall()
        cursor.close()
        pid=1
        if(len(count)>=1) :
            str1 = (''.join(map(str,count[0])))
            pid=int(str1)+1
        cursor = connection.cursor()
        query3="INSERT INTO PLAYER_INFO(PLAYER_ID, FIRST_NAME, LAST_NAME, COUNTRY, PLAYING_POSITION, PRICE, TEAM_NAME) VALUES (%s, %s, %s ,%s, %s ,%s, %s)"
        cursor.execute(query3,[pid, Fname, Lname, countr, playpos, prc, Tname])
        connection.commit()
        cursor.close()
        return render(request,'admininsert.html')
def insertschedule(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    gweek=request.POST['gweek']
    fnum=request.POST['fnum']
    rname=request.POST['rname']
    hteam=request.POST['hteam']
    ateam=request.POST['ateam']
    dtim=request.POST['dtim']
    count=[]
    cursor = connection.cursor()
    query2 = "SELECT * FROM TEAM_INFO WHERE TEAM_NAME = %s"
    cursor.execute(query2,[hteam])
    count = cursor.fetchall()
    cursor.close()
    if(len(count)<1) :
        return render(request,'admininsert.html')
    cursor = connection.cursor()
    query3 = "SELECT * FROM TEAM_INFO WHERE TEAM_NAME = %s"
    cursor.execute(query3,[ateam])
    count = cursor.fetchall()
    cursor.close()
    if(len(count)<1) :
        return render(request,'admininsert.html')
    cursor = connection.cursor()
    query4="INSERT INTO FIXTURE_INFO(GAMEWEEK_ID, FIXTURE_NO, SCHEDULE, REFREE_NAME, HOME_TEAM, AWAY_TEAM) VALUES(%s, %s, TO_DATE(%s, 'YYYY-MM-DD-MI-HH24'), %s, %s, %s);"
    cursor.execute(query4,[gweek,fnum,dtim,rname,hteam,ateam])
    connection.commit()
    cursor.close()
    return render(request,'admininsert.html')
def updateteamresult(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    count=[]
    hteam=request.POST['hteam']
    ateam=request.POST['ateam']
    hscore=request.POST['hscore']
    ascore=request.POST['ascore']

    cursor = connection.cursor()
    sqlquery = 'SELECT NVL(GAMEWEEK_ID,0), NVL(FIXTURE_NO,0) FROM FIXTURE_INFO WHERE HOME_TEAM=%s AND AWAY_TEAM=%s'
    cursor.execute(sqlquery,[hteam,ateam])
    result = cursor.fetchall()
    cursor.close()
    gweek=0
    fnum=0
    for r in result:
        gweek = r[0]
        fnum = r[1]

    cursor = connection.cursor()
    exfix=cursor.callfunc('EXISTFIX', int,[gweek,fnum])
    cursor.close()
    if(exfix==1):
        cursor = connection.cursor()
        query5="UPDATE FIXTURE_INFO SET HOME_TEAM_SCORE = %s, AWAY_TEAM_SCORE=%s WHERE GAMEWEEK_ID = %s AND FIXTURE_NO= %s"
        cursor.execute(query5,[hscore,ascore,gweek,fnum])
        connection.commit()
        cursor.close()
    else:
        messages.warning(request, 'Please insert fixture First')
    return render(request,'updateresult.html')
def updateplayerstat(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    count=[]
    Lname = request.POST['Lname']
    playpos = request.POST['playpos']
    Tname = request.POST['Tname']
    hteam=request.POST['hteam']
    ateam=request.POST['ateam']
    pmin=request.POST['pmin']
    gscore=request.POST['gscore']
    assist=request.POST['assist']
    gcon=request.POST['gcon']
    ycard=request.POST['ycard']
    rcard=request.POST['rcard']

    cursor = connection.cursor()
    sqlquery = 'SELECT NVL(GAMEWEEK_ID,0), NVL(FIXTURE_NO,0) FROM FIXTURE_INFO WHERE HOME_TEAM=%s AND AWAY_TEAM=%s'
    cursor.execute(sqlquery,[hteam,ateam])
    result = cursor.fetchall()
    cursor.close()
    gweek=0
    fnum=0
    for r in result:
        gweek = r[0]
        fnum = r[1]

    cursor = connection.cursor()
    sqlquery = 'SELECT NVL(PLAYER_ID,0) FROM PLAYER_INFO WHERE TEAM_NAME=%s AND LAST_NAME=%s AND PLAYING_POSITION=%s'
    cursor.execute(sqlquery,[Tname,Lname,playpos])
    result = cursor.fetchall()
    cursor.close()
    pid=0
    for r in result:
        pid = r[0]

    count=[]
    cursor = connection.cursor()
    exfix=cursor.callfunc('EXISTFIX', int,[gweek,fnum])
    cursor.close()
    if(exfix==0 or (not(hteam==Tname or ateam ==Tname)) or pid==0):
        messages.warning(request, 'Please Insert Right Info')
        return render(request,'updateresult.html')
    cursor = connection.cursor()
    query6 = 'SELECT HOME_TEAM,AWAY_TEAM FROM FIXTURE_INFO WHERE GAMEWEEK_ID=%s AND FIXTURE_NO=%s'
    cursor.execute(query6,[gweek,fnum])
    result = cursor.fetchall()
    cursor.close()
    hometeam=''
    awayteam=''
    for r in result:
        hometeam=r[0]
        awayteam=r[1]
    cursor = connection.cursor()
    query7 = "SELECT * FROM PLAYER_INFO WHERE (TEAM_NAME IN (%s,%s)) AND PLAYER_ID=%s"
    cursor.execute(query7,[hometeam, awayteam,pid])
    count = cursor.fetchall()
    cursor.close()
    if(len(count)<1):
        messages.warning(request, 'Please enter valid player id')
        return render(request,'updateresult.html')
    cursor = connection.cursor()
    query8 = "SELECT * FROM FIXTURE_STAT WHERE  PLAYER_ID=%s"
    cursor.execute(query8,[pid])
    count = cursor.fetchall()
    cursor.close()
    if(len(count)==0):
        cursor = connection.cursor()
        query9="INSERT INTO FIXTURE_STAT(PLAYER_ID, GAMEWEEK_ID, FIXTURE_NO, PLAYED_MINUTES, GOAL_SCORED, ASSISTS, GOAL_CONCEDED, YELLOW_CARD, RED_CARD) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query9,[pid,gweek,fnum,pmin,gscore,assist,gcon,ycard,rcard])
        connection.commit()
        cursor.close()
    else :
        cursor = connection.cursor()
        query10="UPDATE FIXTURE_STAT SET PLAYED_MINUTES=%s, GOAL_SCORED=%s, ASSISTS=%s, GOAL_CONCEDED=%s, YELLOW_CARD=%s, RED_CARD=%s WHERE (PLAYER_ID=%s AND GAMEWEEK_ID=%s AND FIXTURE_NO=%s)"
        cursor.execute(query10,[pmin,gscore,assist,gcon,ycard,rcard,pid,gweek,fnum])
        connection.commit()
        cursor.close()
    return render(request,'updateresult.html')
def adminadd(request):
    if 'adminuser' not in request.session:
        return render(request,'adminlogin.html')
    new_user = False
    count = []
    email = request.POST['email']
    password = request.POST['pass']
    confpass = request.POST['confpass']
    cursor = connection.cursor()
    sql = "SELECT * FROM USER_INFO WHERE EMAIL = %s"
    cursor.execute(sql,[email])
    count = cursor.fetchall()
    cursor.close()
    if len(count) == 0 or count is None:
        new_user = True
    if new_user== True:
        if(password == confpass):
            password = make_password(password)
            cursor = connection.cursor()
            query2 = "INSERT INTO ADMIN_USERS(EMAIL,PASSWORD) VALUES(%s,%s)"
            cursor.execute(query2,[email,password])
            connection.commit()
            cursor.close()
        else:
            messages.warning(request,"Username or Password is incorrect")
    else:
        messages.warning(request, "Already has an acoount")
    return render(request,'addadmin.html')
def pick_gweekshow(request):
    gweek=request.POST['gweek']
    cursor = connection.cursor()
    query = 'SELECT FIXTURE_NO, HOME_TEAM, AWAY_TEAM, SCHEDULE FROM FIXTURE_INFO WHERE GAMEWEEK_ID= %s'
    cursor.execute(query,[gweek])
    result = cursor.fetchall()
    cursor.close()
    fixtures=[]
    for r in result:
        fixno=r[0]
        Hteam=r[1]
        Ateam=r[2]
        sdl=r[3]
        Gamweek=gweek
        row = {'Gamweek':Gamweek,'fixno':fixno,'Hteam':Hteam,'Ateam':Ateam,'sdl':sdl}
        fixtures.append(row)
    return render(request,'showfixture.html',{'fixtures':fixtures})
def showfix(request):
    return render(request,'showfixture.html')
