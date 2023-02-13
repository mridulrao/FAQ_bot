from code import interact
import queue
from urllib import response
from django.shortcuts import render, HttpResponse

#for AJAX GET query
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .godel_large import get_query, get_more_query 
from .DialoGPT import get_general_responce


# Create your views here.
class FAQBot:
    def __init__(self):
        self.query = ''
        self.responce = ''
        self.validity = ''
        self.query_list = []
        self.bag_of_words = ['graphic', 'era', 'deemed','university','culmination','hard','work','visionary','founder,','Prof.','(Dr.)','Kamal',
                            'ghanshala,','dream','change','destiny','thousands','youth','quality','holistic','education.',
                            '1993,','embarked','mission','transform','higher','education','landscape','Doon','Valley','twenty-nine',
                            'thousand','rupees','pocket','loads','determination','heart.','vision','gained','concrete','shape','1996',
                            'form','graphic','era','institute','technology','(GEIT).In','2008,','institute','accorded','status','deemed','University',
                            'section','3','UGC','act,','1956','vide','notification','F.9-48/2007-U.3','(A)','dated','August','14,','2008','approved','Ministry','Human',
                            'Resource','Development,','Government','India.','2015,','accredited','NAAC','grade','‘A.’',
                            'July','2022,','conferred','All-India','Rank','64','Engineering','Category,','India','Rank','65',
                            'Management','Category,','India','Rank','74','University','Category','MHRD','NIRF','(National','Institutional','Ranking','Framework)',
                            'Rankings','retained','position','consecutively','third','year','amongst','top','100','universities','India.',
                            'premier','university','acquired','transnational','dimensions','student','exchange','knowledge-sharing',
                            'programs','many','foreign','universities','acclaimed','honored','international','forums',
                            'brilliance','upholding','highest','standards','education.','taken','big','initiative','engineering','programs','getting','partnerships','Tata','Technologies','IBM',
                            'create','next','age','engineering','professionals','industry','collaborations.','hosts','Technology','Business','Incubator',
                            'provides','support','technology-based','entrepreneurship.','present,','Graphic','Era','Deemed','University','innumerable','students','rolls,',
                            'pursuing','education','different','disciplines,','ranging','engineering,','science,','business,','management,',
                            'commerce,','hospitality','humanities','social','sciences.','alumni','Graphic','Era','encountered','worldwide','marquee','brands','like',
                            'Apple,','Google,','Microsoft,','HSBC,','name','few,','service','nation','wings','Armed','Forces.','geu','stands','tall','leading',
                            'university','Uttarakhand','ranked','amongst','top','75','Universities','country','abode','learning','excellence,',
                            'setting','new','benchmarks','parameters','assessment','like','teaching','learning','research','graduation','outcome',
                            'outreach','industrial', 'presence','more', 'Indian','Institutions', 'higher', 'education.']

    def append_query_list(self, query):
        self.query_list.append(query)

    def check_general_query(self, query):
        words = query.split()
        for word in words:
            if word.lower() in self.bag_of_words:
                return True
        return False

    
        
interact = FAQBot()


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def get_ques(request):
    if is_ajax(request=request) and request.method == 'POST':
        if 'query' in request.POST:
            interact.query = request.POST['query']
            print(interact.query)
        elif 'validity' in request.POST:
            interact.validity = request.POST['validity']
        else:
            print("Check the data passed in AJAX POST request")

    elif is_ajax(request = request) and request.method == 'GET':
        if interact.validity == 'Useful':
            print("Glad I could help")
            interact.validity = ''
            return JsonResponse({'context' : 'Glad I could help', 'remark' : 'useful'})
        elif interact.validity == 'Not Useful':
            print("Looking for more answers")
            bot_responce = get_more_query(interact.query)
            print(bot_responce)
            query_flag = True
            interact.validity = ''
            return JsonResponse({'context' : bot_responce, 'remark' : 'not_useful', 'query_flag' : query_flag})
        else:
            print("Looking for answer of query " + interact.query)
            if interact.check_general_query(interact.query):
                bot_responce = get_query(interact.query)
                query_flag = True
            else:
                bot_responce = get_general_responce(interact.query)
                query_flag = False
            if interact.responce != '':
                interact.append_query_list(interact.responce)
            interact.responce = bot_responce
            print(bot_responce)
            return JsonResponse({'context' : bot_responce, 'query_flag' : query_flag})      
    else:
        print("Request was not AJAX")
    return render(request, 'process_query/index.html')


