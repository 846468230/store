
import  requests
import json

class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self,code,mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text":"【杨英光】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        response = requests.post(self.single_send_url,data=params)
        re_dict = json.loads(response.text)
        print(re_dict)
        return re_dict

if __name__ == "__main__":
    yun_pian = YunPian("79c7af6a0e03809ac9a2ca74b6363167")
    yun_pian.send_sms("2017","17551077746")