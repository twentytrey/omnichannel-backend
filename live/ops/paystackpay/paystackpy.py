from paystackapi.transaction import Transaction
import random,string

apikey="sk_live_f59a105218f513f8e60869703f091a758c8d56cf"
email="tinigraph@gmail.com"
amount=500
ref=''.join([random.choice(string.ascii_letters+string.digits) for n in range(16)])
Transaction
# response=Transaction.initialize(reference=ref,amount=amount,email=email)
# chargedetails=Transaction.charge(reference=ref,authorization_code=response["data"]["access_code"],email=email,amount=amount)
# print(chargedetails)