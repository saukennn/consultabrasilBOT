import mercadopago
from pprint import pprint

def get_qr(value: float, mail: str, id_folder: str):
    sdk = mercadopago.SDK("APP_USR-7708466551412049-040420-63f77e142041b1596a3df062dafe9170-795310546")

    request_options = mercadopago.config.RequestOptions()
    # request_options.custom_headers = {
    #     'x-idempotency-key': id_folder
    # }

    payment_data = {
        "transaction_amount": value,
        "description": "Agendamento",
        "payment_method_id": "pix",
        "payer": {
            "email": mail
        },
        "notification_url": f"https://portalagendabrasil.store/{id_folder}"
    }

    payment_response = sdk.payment().create(payment_data, request_options)

    if payment_response["response"]["status"] == "pending":
        payment = payment_response["response"]["point_of_interaction"]["transaction_data"]
        response = {
            "qr_code_base64": payment["qr_code_base64"],
            "qr_code": payment["qr_code"]
        }

        return response

        
if __name__ == "__main__":
    response = get_qr(0.1, "mail@mail.com", "TEST3")
    print(response["qr_code"])