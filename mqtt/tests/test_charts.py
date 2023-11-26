from django.test import TestCase, Client
from mqtt.models import Topic, Values
from mqtt.views import home
from datetime import datetime
import pytz
from datetime import timedelta
import time as ttime

# None topic
# None value
# 1 value
# 2 value
# 3 value
# 5 value

# none + 1 value
# 1 value + none
# 1 value + none + 1 value

# none + 2 value
# 2 value + none
# 2 value + none + 2 value

class ChartsTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.topic1 = Topic.objects.create(name="/basement/kotel/water")
        self.topic2 = Topic.objects.create(name="/basement/kotel/smoke")
        self.topic3 = Topic.objects.create(name="/outside/temp")

        Values.objects.create(topic=self.topic1, value="20", date_pub=pytz.UTC.localize(datetime.now() - timedelta(minutes=60)))
        Values.objects.create(topic=self.topic2, value="10", date_pub=pytz.UTC.localize(datetime.now() - timedelta(minutes=60)))
        Values.objects.create(topic=self.topic3, value="30", date_pub=pytz.UTC.localize(datetime.now() - timedelta(minutes=60)))
        self.data1 = [[30.0,20.0,10.0], ['None', 'None', 'None'], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'],
        [30.0,20.0,10.0]]
        self.data2 = [[30.0,20.0,10.0], [3.0,2.0,1.0], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'],
        [3.0,2.0,1.0]]
        self.data3 = [[30.0,20.0,10.0], [3.0,2.0,1.0], [7.0, 5.0, 6.0], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'], 
        ['None', 'None', 'None'], ['None', 'None', 'None'], ['None', 'None', 'None'],
        [7.0, 5.0, 6.0]]

    def create_data(self, data, last_date):
        self.exp_data = [[{'type': 'date', 'label': 'Date'},
                        'temp', {'type': 'string', 'role': 'tooltip'},
                        'water', {'type': 'string', 'role': 'tooltip'},
                        'smoke', {'type': 'string', 'role': 'tooltip'}]]
        for n, data in enumerate(data):
            self.exp_data.append(['Date('+str(int(ttime.mktime((last_date + timedelta(minutes=5*n)).timetuple()))*1000)+ 
                ')', data[0], str((last_date + timedelta(minutes=5*n)).strftime("%b %d, %H:%M"))+
                "\noutside: " + str(data[0]), data[1],
                str((last_date + timedelta(minutes=5*n)).strftime("%b %d, %H:%M"))+"\nwater: " + str(data[1]), data[2],
                str((last_date + timedelta(minutes=5*n)).strftime("%b %d, %H:%M"))+"\nsmoke: " + str(data[2])
                ])


    def test_val1(self):

        last_date = pytz.UTC.localize(datetime.now() - timedelta(minutes=0))
        print("\n test_now_date:", last_date)
        self.create_data(self.data1, last_date)
        response = self.client.get(r'/1/')

        # for n, data in enumerate(self.exp_data):
        #     print("   DATA:", data, "\nRESPONS:", response.context["data_all"][n], "\n\n")

        self.assertEqual(len(response.context["data_all"]), len(self.exp_data))
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.exp_data, response.context["data_all"])

    # def test_val2(self):

    #     Values.objects.create(topic=self.topic1, value="2", date_pub=pytz.UTC.localize(datetime.now() + timedelta(minutes=65)))
    #     Values.objects.create(topic=self.topic2, value="1", date_pub=pytz.UTC.localize(datetime.now() + timedelta(minutes=65)))
    #     Values.objects.create(topic=self.topic3, value="3", date_pub=pytz.UTC.localize(datetime.now() + timedelta(minutes=65)))

    # #     last_date = pytz.UTC.localize(datetime.now() - timedelta(minutes=5))
    # #     self.create_data(self.data2, last_date)
    # #     response = self.client.get(r'/1/')
    # #     for n, data in enumerate(self.exp_data):
    # #         print("   DATA:", data, "\nRESPONS:", response.context["data_all"][n], "\n\n")

    # #     self.assertEqual(len(response.context["data_all"]), len(self.exp_data))
    # #     self.assertEqual(200, response.status_code)
    # #     self.assertEqual(self.exp_data, response.context["data_all"])

    # def test_val3(self):

    #     Values.objects.create(topic=self.topic1, value="5", date_pub=pytz.UTC.localize(datetime.now() + timedelta(minutes=70)))
    #     Values.objects.create(topic=self.topic2, value="6", date_pub=pytz.UTC.localize(datetime.now() + timedelta(minutes=70)))
    #     Values.objects.create(topic=self.topic3, value="7", date_pub=pytz.UTC.localize(datetime.now() + timedelta(minutes=70)))

    #     last_date = pytz.UTC.localize(datetime.now() - timedelta(minutes=0))
    #     self.create_data(self.data3, last_date)
    #     response = self.client.get(r'/1/')
    #     for n, data in enumerate(self.exp_data):
    #         print("   DATA:", data, "\nRESPONS:", response.context["data_all"][n], "\n\n")

    #     self.assertEqual(len(response.context["data_all"]), len(self.exp_data))
    #     self.assertEqual(200, response.status_code)
    #     self.assertEqual(self.exp_data, response.context["data_all"])