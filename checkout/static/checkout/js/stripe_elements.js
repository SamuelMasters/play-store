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
    // 
    $('#submit-button').attr('disabled', true);
    console.log("Submit button disabled...") // debug
    var saveInfo = Boolean($('#id-save-info').attr('checked'));
    var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    var postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    }

    var url = '/checkout/cache_checkout_data/';
    $.post(url, postData).done(function () {

        console.log("DEBUG: about to attempt stripe.confirmCardPayment...") // debug
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: $.trim(form.full_name.value),
                    email: $.trim(form.email.value),
                    // phone: $.trim(form.phone_number.value),
                    address: {
                        line1: $.trim(form.street_address1.value),
                        line2: $.trim(form.street_address2.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                    },
                },
            },
            shipping: {
                name: $.trim(form.full_name.value),
                // phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    state: $.trim(form.county.value),
                    postal_code: $.trim(form.postcode.value),
                    country: $.trim(form.country.value),
                }
            },
        }).then(function(result) {
            console.log("DEBUG: .then after .confirmCardPayment triggered...") // debug
            if (result.error) {
                console.log("DEBUG: An error occured on .confirmCardPayment") // debug
                console.log(result.error) // debug
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
                console.log("Submit button re-enabled...") // debug
                $('#submit-button').attr('disabled', false);
            } else {
                console.log("DEBUG: no result.error found...") // debug
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function() {
        console.log("DEBUG: .fail triggered...") // debug
        location.reload();
    })

});