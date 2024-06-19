#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 14:02:05 2024

@author: jlab
"""

import requests

async def process_payment(reader_id, payment_intent_id):
    url = "http://your_domain.com/process-payment-intent"
    headers = {"Content-Type": "application/json"}
    data = {
        "reader_id": reader_id,
        "payment_intent_id": payment_intent_id
    }
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    process_error = response_data.get("error")
    reader_state = response_data.get("reader_state")
    return {"processError": process_error, "readerState": reader_state}

async def retrieve_reader(reader_id):
    url = f"http://your_domain.com/retrieve-reader?reader_id={reader_id}"
    response = requests.get(url)
    response_data = response.json()
    reader_state = response_data.get("reader_state")
    reader_error = response_data.get("error")
    return {"reader": reader_state, "readerError": reader_error}

async def cancel_reader_action(reader_id):
    url = "http://your_domain.com/cancel-reader-action"
    headers = {"Content-Type": "application/json"}
    data = {"reader_id": reader_id}
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    canceled_reader = response_data.get("reader_state")
    cancel_action_error = response_data.get("error")
    return {"canceledReader": canceled_reader, "cancelActionError": cancel_action_error}

async def simulate_payment(reader_id):
    url = "http://your_domain.com/simulate-payment"
    headers = {"Content-Type": "application/json"}
    data = {"reader_id": reader_id}
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    reader_state = response_data.get("reader_state")
    simulate_payment_error = response_data.get("error")
    return {"reader": reader_state, "simulatePaymentError": simulate_payment_error}

# Function to create payment intent
async def create_payment_intent(amount):
    url = "http://your_domain.com/create-payment-intent"
    headers = {"Content-Type": "application/json"}
    data = {"amount": amount}
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    payment_intent_id = response_data.get("payment_intent_id")
    payment_error = response_data.get("error")
    return {"paymentIntentId": payment_intent_id, "paymentError": payment_error}

# Function to retrieve payment intent
async def retrieve_payment_intent(payment_intent_id):
    url = f"http://your_domain.com/retrieve-payment-intent?payment_intent_id={payment_intent_id}"
    response = requests.get(url)
    response_data = response.json()
    payment_intent = response_data.get("payment_intent")
    payment_error = response_data.get("error")
    return {"paymentIntent": payment_intent, "paymentError": payment_error}

# Function to capture payment intent
async def capture_payment_intent(payment_intent_id):
    url = "http://your_domain.com/capture-payment-intent"
    headers = {"Content-Type": "application/json"}
    data = {"payment_intent_id": payment_intent_id}
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()
    captured_payment_intent = response_data.get("payment_intent")
    capture_error = response_data.get("error")
    return {"capturedPaymentIntent": captured_payment_intent, "captureError": capture_error}