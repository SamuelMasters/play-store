/*
    Payment flow adapted from:
    https://stripe.com/docs/payments/accept-a-payment
    
    CSS copied from:
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

/* Style copied across from Stripe documentation */
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvertica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#AAB7C4'
        }
    },
    invalid: {
        color: '#DC3545',
        iconColor: '#DC3545'
    }
};
var card = elements.create('card', {
    style: style
});

card.mount('#card-element');

/* Below lines adapted from Boutique Ado project */
// Handle real time validation errors on #card-element
card.addEventListener('change', function (e) {
    var errorDiv = document.getElementById('card-errors');
    if (e.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${e.error.message}</span>
        `;
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle payment form submission
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    $('#submit-button').attr('disabled', true);

    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: $.trim(form.full_name.value),
                email: $.trim(form.email.value),
                phone_number: $.trim(form.phone_number.value),
                address:{
                    street_address1: $.trim(form.street_address1.value),
                    street_address2: $.trim(form.street_address2.value),
                    county: $.trim(form.county.value),
                    country: $.trim(form.country.value),
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone_number: $.trim(form.phone_number.value),
                address:{
                    street_address1: $.trim(form.street_address1.value),
                    street_address2: $.trim(form.street_address2.value),
                    county: $.trim(form.county.value),
                    postcode: $.trim(form.postcode.value),
                    country: $.trim(form.country.value),
                }
            }
        }
    }).then(function (result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            card.update({
                'disabled': false
            });
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});