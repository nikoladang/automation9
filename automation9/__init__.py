import names
import requests
from guerrillamail import GuerrillaMailSession

class Automation9(object):
    def __init__(self):
        pass
        
    def random_username(self, sex='female', no_of_digits=3):
        import random
        digits = random.randrange(100,1000) # interger from 100 to 999
        #first_name = names.get_first_name(gender=sex)
        fullname = names.get_full_name(gender=sex)
        return fullname.replace(" ","") + str(digits)

    def custom_guerrilla_mail_session(self, **kwargs):
        """
        get new email -> read the content -> click link
        """
        aSession = GuerrillaMailSession()
        aSession.get_session_state()
        aSession.set_email_address(kwargs['username'])
        return aSession

    def generate_register_info(self, password="!Admin987", mailService="Guerrilla"):
        _username = self.random_username()
        if mailService == "Guerrilla":
            _mailSession = self.custom_guerrilla_mail_session(username=_username)
            _email_address = _mailSession.email_address
        return {
            'email': _email_address,
            'username': _username,
            'password': password,
            'mailSessionID' : _mailSession.session_id,
            }

    def MAIL_get_verification_link(self, mailSessionID=None, subjectPattern=None, linkPattern=r"", mailService="Guerrilla", timeout=10):
        import re
        if mailService == "Guerrilla":
            _mailSession = GuerrillaMailSession(mailSessionID)
            if timeout:
                from datetime import datetime
                start_time = datetime.now()
            while True:
                for mail in _mailSession.get_email_list():
                    if subjectPattern in mail.subject:
                        fetch_mail = _mailSession.get_email(mail.guid)
                        body = fetch_mail.body
                        m = re.search(linkPattern, body)
                        if m:
                            link = m.group('veri_link')
                            print("LINK FOUND: "+link)
                            return link
                time.sleep(2)
                if timeout:
                    current_time = datetime.now()
                    interval = current_time - start_time
                    if interval > timeout:
                        print("{{MAIL_get_verification_link}} TIMEOUT!!!")
                        return None
        return None

    def screenshot_captcha(self, webDriver, element, path):
        from selenium.webdriver import ActionChains
        from PIL import Image
        action_chain = ActionChains(webDriver)
        action_chain.move_to_element(element)
        action_chain.perform()
        loc, size = element.location_once_scrolled_into_view, element.size
        left, top = loc['x'], loc['y']
        width, height = size['width'], size['height']
        box = (int(left), int(top), int(left + width), int(top + height))
        webDriver.save_screenshot(path)
        image = Image.open(path)
        captcha = image.crop(box)
        captcha.save(path, 'PNG')

    @staticmethod
    def wait_between(a, b):
        import time
        from random import uniform
        rand=uniform(a, b) 
        time.sleep(rand)

    def test(q=*):
        pass
    
if __name__ == "__main__":
    auto = Automation9()
    auto.test()
    pass
##    print(session.email_address)
##    print(session.get_email_list()[0].guid)
##    mail_body = aSession.get_email(1).body
