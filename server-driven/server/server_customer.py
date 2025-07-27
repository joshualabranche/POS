#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 13:36:27 2024

@author: jlab
"""

import stripe
import os
import json

from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
stripe.api_key = os.getenv('STRIPE_TEST_KEY')
stripe.api_version = "2020-08-27"
# For sample support and debugging, not required for production
stripe.app_info = {
    "name": "stripe-samples/terminal/server-driven",
    "version": "0.0.1",
    "url": "https://github.com/stripe-samples"
}

static_dir = str(os.path.abspath(os.path.join(os.getenv("STATIC_DIR"))))
app = Flask(__name__,
            static_folder=static_dir,
            static_url_path="",
            template_folder=static_dir)

order = {}

@app.route("/", methods=['GET'])
def home():
    return render_template('/html/kiosk.html')

@app.route("/process", methods=['GET'])
def process():
    return render_template('/html/index.html')

@app.route("/reader", methods=['GET'])
def reader():
    return render_template('/html/reader.html')

@app.route("/success", methods=['GET'])
def success():
    return render_template('/html/success.html')

@app.route("/canceled", methods=['GET'])
def cancel():
    return render_template('/html/canceled.html')

@app.route("/list-readers", methods=['GET'])
def list_readers():
    """
    List all Terminal Readers. You can optionally pass a limit or Location ID to further filter the Readers. See the documentation [0] for the full list of supported parameters.

    [0] https://stripe.com/docs/api/terminal/readers/list
    """
    try:
        readers = stripe.terminal.Reader.list()
        readers_list = readers.data
        return jsonify({'readers': readers_list})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/create-payment-intent", methods=['POST'])
def create_payment_intent():
    """
    Create a PaymentIntent with the amount, currency, and a payment method type.
    For in-person payments, you must pass "card_present" in the payment_method_types array and set the capture_method to "manual".

    See the documentation [0] for the full list of supported parameters.

    [0] https://stripe.com/docs/api/payment_intents/create
    """
    try:
        amount = request.get_json().get('amount') + '00'
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            payment_method_types=["card_present"],
            capture_method="manual")
        return jsonify({'payment_intent_id': payment_intent.id})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/retrieve-payment-intent", methods=['GET'])
def retrieve_payment_intent():
    """
    Retrieves a PaymentIntent by ID.
    """
    try:
        payment_intent_id = request.args.get("payment_intent_id")
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return jsonify({"payment_intent": payment_intent})
    except Exception as e:
        return jsonify({"error": {"message": str(e)}})


@app.route("/process-payment-intent", methods=['POST'])
def process_payment_intent():
    """
    Hands-off a PaymentIntent to a Terminal Reader.
    This action requires a PaymentIntent ID and Reader ID.

    See the documentation [0] for additional optional
    parameters.

    [0] https://stripe.com/docs/api/terminal/readers/process_payment_intent
    """
    try:
        request_json = request.get_json()
        payment_intent_id = request_json.get('payment_intent_id')
        reader_id = request_json.get('reader_id')

        reader_state = stripe.terminal.Reader.process_payment_intent(
            reader_id,
            payment_intent=payment_intent_id,
        )
        return jsonify({'reader_state': reader_state})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/simulate-payment", methods=['POST'])
def simulate_terminal_payment():
    """
    Simulates a user tapping/dipping their credit card
    on a simulated reader.

    This action requires a Reader ID and can be configured
    to simulate different outcomes using a card_present dictionary.
    See the documentation [0][1] for details.

    [0] https://stripe.com/docs/api/terminal/readers/present_payment_method
    [1] https://stripe.com/docs/terminal/payments/collect-payment?terminal-sdk-platform=server-driven#simulate-a-payment
    """
    try:
        reader_id = request.get_json().get('reader_id')
        reader_state = stripe.terminal.Reader.TestHelpers.present_payment_method(reader_id)
        return jsonify({'reader_state': reader_state})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/retrieve-reader", methods=['GET'])
def retrieve_reader():
    """
    Retrieves a Reader.
    """
    try:
        reader_id = request.args.get("reader_id")
        reader_state = stripe.terminal.Reader.retrieve(reader_id)
        return jsonify({"reader_state": reader_state})
    except Exception as e:
        return jsonify({"error": {"message": str(e)}})


@app.route("/capture-payment-intent", methods=['POST'])
def capture_payment_intent():
    """
    Captures a PaymentIntent that been completed but uncaptured.
    This action only requires a PaymentIntent ID but can be configured
    with additional parameters.

    [0] https://stripe.com/docs/api/payment_intents/capture
    """
    try:
        payment_intent_id = request.get_json().get('payment_intent_id')
        payment_intent = stripe.PaymentIntent.capture(payment_intent_id)
        return jsonify({'payment_intent': payment_intent})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route("/cancel-reader-action", methods=['POST'])
def cancel_action():
    """
    Cancels the Reader action and resets the screen to the idle state.
    This can also be use to reset the Reader's screen back to the idle state.

    It only returns a failure if the Reader is currently processing a payment
    after a customer has dipped/tapped or swiped their card.

    Note: This doesn't cancel in-flight payments.
    """
    try:
        reader_id = request.get_json().get('reader_id')
        reader_state = stripe.terminal.Reader.cancel_action(reader_id)
        return jsonify({'reader_state': reader_state})
    except Exception as e:
        return jsonify({'error': {'message': str(e)}}), 400


@app.route('/config', methods=['GET'])
def get_config():
    return jsonify({'publishableKey': os.getenv('STRIPE_PUBLISHABLE_KEY')})


@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']
    print(data_object)

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')


    return jsonify({'status': 'success'})


@app.route("/order", methods=['GET', 'PUT'])
def retrieve_order_info():
    if request.method == 'GET':          
        try:
            # do stuff to get data
            return jsonify(order)
        except Exception as e:
            return jsonify({"error": {"message": str(e)}})
    elif request.method == 'PUT':
        try:
            new_request = request.get_json()
            print(new_request)
            if "remove_order" in new_request.keys():
                count = -1
                for orders in order:
                    count += 1
                    if orders["id"]==new_request["remove_order"]:
                        order.pop(count)                   
            else:
                order.append(new_request)
            return jsonify(order)
        except Exception as e:
            return jsonify({'error': {'message': str(e)}}), 400


if __name__ == '__main__':
    app.run(port=4242, debug=True)
