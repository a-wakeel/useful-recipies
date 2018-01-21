import requests
import time
import smtplib
from fake_useragent import UserAgent

FETCH_INTERVAL = 60  # interval of data being fetch from api
RATE_DIFFERENCE = 1  # percent difference between open buy orders
USER_EMAIL = 'user@email.com'  # your account email id here
USER_PASS = 'password'  # your account password (new generated pass in-case of two factor auth account)
RECIPT_EMAIL = ['mail1@mail.com', 'mail2@mail.com']  # recipients emails, add more in list


def send_mail(user_email, passwd, recipt_email, subject, body):
    """
    To send mail to specified email address
    TODO: Allow less secure apps option on your gmail account or make password for this
    app on accounts having two factor authentications

    :param user_email: user email address (to login)
    :param passwd: user email password or password generated by two factor auth accounts
    :param recipt_email: email/emails of recipients
    :param subject: subject of the email
    :param body: body of the email
    """
    print('* send mail to {recpt}'.format(recpt=recipt_email))

    mail_to = recipt_email if type(recipt_email) is list else [recipt_email]
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (user_email, ", ".join(mail_to), subject, body)

    try:
        mail_server = smtplib.SMTP("smtp.gmail.com", 587)
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.login(user_email, passwd)
        mail_server.sendmail(user_email, mail_to, message)
        mail_server.close()
        print('* mail sent successfully')
    except Exception as e:
        print(e.message)


def get_data():
    """
    Get markets data from the api in json format
    :return: return market summary data in json format
    """
    print('* getting data from bittrex')
    try:
        user_agent = UserAgent()
        headers = {'User-Agent': user_agent.random}
        res = requests.get('https://api.hitbtc.com/api/2/public/ticker', headers=headers)

        if res.status_code == requests.codes.ok:
            return res.json()
        else:
            return res.text
    except Exception as e:
        print(e.message)


def parse_data(data):
    """
    Parse jaon data set into a string
    :param data: jason data, dict data
    :return: string
    """
    parsed_data = "Market Name  :  % Vol Difference"
    string_list = [parsed_data]
    for item in data:
        data_str = "\n{market_name}  :  {diff}".format(market_name=item['MarketName'], diff=item['Difference'])
        string_list.append(data_str)

    parsed_data = " ".join(string_list)
    return parsed_data


def main():
    print('* starting script')

    while True:
        current_data = []
        market_data = get_data()
        time.sleep(FETCH_INTERVAL)
        updated_market_data = get_data()

        data_count = 0
        while data_count < len(market_data):
            latest_vol_value = updated_market_data[data_count]['volume']
            previous_vol_value = market_data[data_count]['volume']
            vol_difference = ((latest_vol_value - previous_vol_value)/previous_vol_value)*100

            if vol_difference >= RATE_DIFFERENCE:
                result = {'MarketName': updated_market_data[data_count]['symbol'],
                          'Difference': vol_difference}
                current_data.append(result)
            data_count += 1

        if len(current_data) > 0:
            send_mail(USER_EMAIL, USER_PASS, RECIPT_EMAIL, 'HIT-BTC Markets Differences', parse_data(current_data))


if __name__ == '__main__':
    main()
