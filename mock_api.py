import random
from datetime import datetime, timedelta

def blockCard(customer_id, reason="lost_or_stolen"):
    last4 = str(customer_id)[-4:] if customer_id else "XXXX"
    return {"status": "success", "message": f"Your card ending with {last4} has been blocked."}

def unblockCard(customer_id):
    last4 = str(customer_id)[-4:] if customer_id else "XXXX"
    return {"status": "success", "message": f"Your card ending with {last4} has been unblocked."}

def updateEmail(customer_id, email):
    return {"status": "success", "message": f"Your email has been updated to {email}."}

def requestCreditLimit(customer_id, requested_limit):
    return {"status": "queued", "message": f"Your request for increase to ₹{requested_limit} has been submitted and will be processed in 48 hours."}

def rescheduleDelivery(customer_id, delivery_date):
    return {"status": "success", "message": f"Your delivery has been rescheduled to {delivery_date}."}

def updateDeliveryAddress(customer_id, address):
    return {"status": "success", "message": f"Your delivery address has been updated to: {address}."}

def convertToEMI(customer_id, txn_id, tenure):
    emi = max(1, round(random.uniform(100, 5000)/tenure))
    return {"status": "success", "message": f"Transaction {txn_id} converted to {tenure} months EMI. Estimated EMI: ₹{emi} per month."}

def cancelEMI(customer_id, emi_id):
    return {"status": "success", "message": f"EMI {emi_id} has been cancelled successfully."}

def downloadStatement(customer_id, month, year):
    url = f"https://mock.statements/paygennie/{customer_id}/{month}{year}.pdf"
    return {"status": "success", "message": f"Here is your statement: {url}", "download_link": url}

def emailStatement(customer_id, month, email):
    return {"status": "success", "message": f"Statement for {month} has been emailed to {email}."}

def doPayment(customer_id, amount):
    receipt = f"R{random.randint(10000,99999)}"
    return {"status": "success", "message": f"Payment of ₹{amount} is successful. Receipt: {receipt}", "receipt": receipt}

def enableAutopay(customer_id, type_):
    return {"status": "success", "message": f"Autopay enabled for {type_}."}

def disableAutopay(customer_id):
    return {"status": "success", "message": "Autopay disabled."}

def raiseDispute(customer_id, txn_id, reason):
    return {"status": "success", "message": f"Dispute raised for {txn_id}. We will contact you within 24 hours."}

def requestChargeback(customer_id, txn_id):
    return {"status": "success", "message": f"Chargeback request initiated for {txn_id}."}

def requestFeeWaiver(customer_id, fee_type):
    return {"status": "submitted", "message": f"Waiver request for {fee_type} has been submitted. It may take up to 7 days."}

def setupPaymentPlan(customer_id, plan):
    dates = ", ".join([ (datetime.now() + timedelta(days=7*i)).strftime("%d %b") for i in range(1,4)])
    return {"status": "success", "message": f"A payment plan has been created: pay {plan} on {dates}."}

def updateMobile(customer_id, mobile):
    return {"status": "success", "message": f"Your mobile number has been updated to {mobile}."}

def requestCardReplacement(customer_id):
    date = (datetime.now() + timedelta(days=3)).strftime("%d %b %Y")
    return {"status": "success", "message": f"Replacement card will be dispatched. Expected dispatch: {date}."}
