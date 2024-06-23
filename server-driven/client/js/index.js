document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const amount = urlParams.get('total_amount');
  const res = await fetch("/list-readers");
  const { readers, error: readerError } = await res.json();
  if (readerError) {
    handleError(readerError);
  }

  if (readers.length) {
    addMessage(`Retrieved Terminal readers.`);
  } else {
    addMessage(`No Terminal readers returned. Add readers to your Stripe account.`)
  }

  const readerSelect = document.getElementById('reader-select');
  readers.forEach(el => {
    const readerOption = document.createElement('option');
    readerOption.value = el.id;
    readerOption.text = `${el.label} (${el.id})`;
    readerSelect.append(readerOption);
  });


    // Select the input element
    const amountDefault = document.getElementById('amount');
    // Set a default value
    amountDefault.value = amount;

  const form = document.getElementById('confirm-form');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    form.querySelector('button').disabled = true;

    const amountInput = amount; // parseInt(document.querySelector('#amount').value, 10);

    // Create Payment Intent
    const { paymentIntentId, paymentError } = await createPaymentIntent(amountInput);
    if (paymentError) {
      handleError(paymentError);
      form.querySelector('button').disabled = false;
      return;
    }
    addMessage(`Created PaymentIntent for ${amountInput}.`);

    // Hand off to reader
    const readerId = document.querySelector("#reader-select").value;
    addMessage(`Reader ID:  ${readerId}.`);
    const { processError } = await processPayment(readerId, paymentIntentId);
    if (processError) {
      handleError(processError);
      form.querySelector('button').disabled = false;
      return;
    }
    addMessage(`Payment ID:  ${paymentIntentId}.`);
    window.location.replace(`/reader?reader_id=${readerId}&payment_intent_id=${paymentIntentId}&amount=${amountInput}`);
  });
});

async function processPayment(readerId, paymentIntentId) {
  const res = await fetch("/process-payment-intent", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      reader_id: readerId,
      payment_intent_id: paymentIntentId,
    }),
  });
  const { error: processError, reader_state: readerState } = await res.json();
  return { processError, readerState };
}
